


import usocket as socket
from machine import Pin, SPI, I2C, Timer
from HPT import HPT
from SCD41 import SCD41
from ssd1306 import SSD1306_I2C
import network, rp2, time, utime, math, neopixel

###################Configuration#########################
NAME = "HPTsen0"
visual = 30 # the time the display is on
alarmLimit = [350, 200, 1500] # Limits for the alarm
dim = 10 # The times the led would be dimmed
PORT = 52171  # The port used by the server
###################DON'T CHANCE##########################

timer=Timer(-1)
timer.init(period=60000, mode=Timer.PERIODIC, callback=lambda t:saveData())   #initializing the timer

#Pin assignment
led = Pin(25, Pin.OUT)
pwm = machine.PWM(machine.Pin(5))
reset = machine.Pin(22, machine.Pin.OUT, machine.Pin.PULL_DOWN)
button = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
ledPin = neopixel.NeoPixel(Pin(23), 1)
#Set initial led color
ledPin[0] = (0, 0, 0)
ledPin.write()
#Reset display
reset.on()
reset.off()
reset.on()
#Setting Initial buzzer status
pwm.duty_u16(0)

# Initialisation libraries
i2c = I2C(1, scl=machine.Pin(3), sda=machine.Pin(2))
spi=SPI(0,2_000_000, mosi=Pin(19),miso=Pin(16),sck=Pin(18))
nic = network.WIZNET5K(spi,Pin(17),Pin(20)) #spi,cs,reset pin
hpt = HPT(i2c)
scd41 = SCD41(i2c)

# variable declaration
stored = []
sensor = [0x00, 0x00, 0x00, 0x00]
dataM = [0, 0, 0, 0, 0]
dataS = [0, 0, 0, 0, 0]

tempA, humiA, vocA, noxA, co2A = 0, 0, 0, 0, 0
startB, delay, switch, buz1, buz2 = 0, 1, 0, 0, 0
averageC, timingS, displayV, flip, blinkS = 0, 0, 0, False, True
startM, oled, timeOut= True, 0, 0
HOST, MAC ="NONE", "NONE"
    
######################################################### Search i2c devices    
def scanI2C(i2c):
    global sensor
    print('Scan i2c bus...')
    devices = i2c.scan()

    if len(devices) == 0:
        print("No i2c device !")
    else:
        print('i2c devices found:',len(devices))
        for device in devices:  
            print("Decimal address: ",device," | Hexa address: ",hex(device), type(device))
            if device == 0x3C or device == 0x3D:
                sensor [0] = device
            elif device == 0x44:
                sensor[1] = device
            elif device == 0x59:
                sensor[2] = device
            elif device == 0x62:
                sensor[3] = device

######################################################### Draw a circle on the display
def circle(x,y,r,color = 1,fill=0):       #A circular function
    if(fill==0):
        for i in range(x-r,x+r+1):
            oled.pixel(i,int(y-math.sqrt(r*r-(x-i)*(x-i))),color)
            oled.pixel(i,int(y+math.sqrt(r*r-(x-i)*(x-i))),color)
        for i in range(y-r,y+r+1):
            oled.pixel(int(x-math.sqrt(r*r-(y-i)*(y-i))),i,color)
            oled.pixel(int(x+math.sqrt(r*r-(y-i)*(y-i))),i,color)
    else:
        for i in range(x-r,x+r+1):
            a=int(math.sqrt(r*r-(x-i)*(x-i)))
            oled.vline(i,y-a,a*2,color)

        for i in range(y-r,y+r+1):
            a=int(math.sqrt(r*r-(y-i)*(y-i)))
            oled.hline(x-a,i,a*2,color)

######################################################### Led functie
def LED(arg):
    global led, dim
    if (arg == "red"):
        red, green, blue = [255/dim, 0, 0]
    elif (arg == "orange"):
        red, green, blue = [255/dim, 255/dim, 0]
    elif (arg == "green"):
        red, green, blue = [0, 255/dim, 0]
    elif (arg == "blue"):
        red, green, blue = [0, 0, 255/dim]
    elif (arg == "off"):
        red, green, blue = [0, 0, 0]
    
    if flip:
        ledPin[0] = (0, 0, 0)
    else:
        ledPin[0] = (int(round(red, 0)), int(round(green, 0)), int(round(blue, 0)))
    ledPin.write()
         

######################################################### Connecting to the network (W5100 ethernet interface)
def w5x00_init():
    global spi, nic, PORT
    LED("red")
    MAC = ""
    count = 0
    NC = False
    macS = [0, 0, 0, 0, 0, 0]
    nic.active(True)
    while not nic.isconnected():
        time.sleep(1)
        print ("-----")
        count += 1
        if (count == 9):
            NC = True
            timeOut = time.time()
            LED("red")
            break
        else:
            NC = False
            
        #print(nic.regs())
    if NC:
        ip = 0
        MAC = 0
        LED("off") 
    else:
        LED("red")
        ip,sn,gw,dns = nic.ifconfig()
        mac = nic.config('mac')
        #nic.ifconfig((ip,sn,gw,dns))
        print('IP      : ', ip)
        print('Subnet  : ', sn)
        print('Gateway : ', gw)
        print('DNS     : ', dns)
        print('MAC     : ', mac)
        for i in range (6):
            if (mac[i] < 10):
                macS[i] = "0" + str(hex(mac[i])[2:])
            else:
                macS[i] = str(hex(mac[i])[2:])
        MAC = macS[0] + ":" + macS[1] + ":" + macS[2] + ":" + macS[3] + ":" + macS[4] + ":" + macS[5]
        print(MAC)
    if NC:
        ip = 0
        MAC = 0
    return ip, MAC



########################################################## Datacommunication with the main module
def dataComm(HOST, PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    oled.fill(0)
    oled.contrast(125)
    try:
        print("data Communication")
        s.settimeout(1)			# don't make smaller, any smaller and the communication will fail
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        if conn:
            LED("Orange")
            print(f"Connected by {addr}")
            state = 1
            dis = 0
            dataC = 0
            while (True):
                if (dis == 3):
                    conn.close()
                    s.close()
                    state = 1
                    print ("Disconnected")
                    LED(0, 0, 0, 0)
                    break
                
                elif (state == 1):
                    dataR = conn.recv(1024)
                    print("State 1 receive: ", dataR)
                    if not dataR:
                        break
                    else:
                        if dataR == (b'Request data'):
                            print (len(stored))
                            conn.sendall("Amount: "+ str(len(stored)))
                            state = 2
                        else:
                            conn.sendall(b'NACK')
                            dis += 1
                    
                elif (state == 2):
                    dataR = conn.recv(1024)
                    print("State 2 receive: ", dataR)
                    if (dataR == b'ACK'):
                        dis = 0
                        state = 3
                    elif (dataR == b'DIS'):
                        dis = 3
                    else:
                        state = 1
                        dis += 1
                        
                elif (state == 3):
                    data = stored[dataC]
                    print(data, type(data))
                    dataT = str(data)
                    print(dataT, type(dataT))
                    conn.sendall(dataT)
                    state = 4
                    
                
                elif (state == 4):
                    dataR = conn.recv(1024)
                    print("State 4 receive: ", dataR)
                    
                    if (dataR == b'NEXT'):
                        del stored[dataC]
                        state = 3
                        dataC += 1
                    elif (dataR == b'ACK'):
                        del stored[dataC]
                        state = 5
                    else:
                        state = 3
                        dis += 1
                
                elif (state == 5):
                    conn.sendall(b'END')
                    dataR = conn.recv(1024)
                    print("State 5 receive: ", dataR)
                    if (dataR == b'END'):
                        conn.close()
                        s.close()
                        state = 1
                        LED(0, 0, 0, 0)
                        break
                    else:
                        state = 5
                        dis += 1
    except:
        LED("off")
        s.close()
        #print("No connection")

########################################################## Alarm for a too high VOC/NOx/CO2
def alarm(dataS):
    temp, humi, VOC, NOx, CO2 = dataS

    if (CO2 > alarmLimit[2]):
        LED("magenta")
        print ("CO2 is too HIGH", co2)
        buzzer()
    if (NOx > alarmLimit[1]):
        LED("magenta")
        buzzer()
    if (VOC > alarmLimit[0]):
        LED("magenta")
        print ("VOC is too HIGH")
        buzzer()
    if (CO2 < alarmLimit[2] and NOx < alarmLimit[1] and VOC < alarmLimit[0]):
        pwm.duty_u16(0)
        LED("off")
        StartB = 0
    
#########################################Buzzer function
def buzzer ():
    global startB, delay, switch, buz1, buz2
    print("Buzzer delay:", delay)
    pwm.freq(1000)
    dura = hpt.buttonHold(button.value(), time.time())
    if (dura > 2.5):
        delay = 900
        
    if (startB == 0):
        print("buzzer start")
        buz1 = time.time()
        buz2 = 0
        startB = 1
        
        
    if (time.time() > buz1+delay and switch == 0):
        print("buzzer on")
        pwm.duty_u16(20000)
        buz2 = time.time()
        switch = 1
        
    elif (time.time() > buz2+1 and switch == 1):
        print("buzzer off")
        pwm.duty_u16(0)
        buz1 = time.time()
        switch = 0
########################################################## Function to save the data
def saveData():
    global sensor, averageC, dataS
    
    LED("green")
    print ("saving data", averageC)
    dataS = measure()
    print (dataS)
    if averageC == 9:
        for d in range (5):
            dataM[d] = dataS[d] / 10
        print("Storing data")
        TIMX = time.localtime()
        
        TIMD = str(TIMX[2]) + "-" + str(TIMX[1]) + "-" + str(TIMX[0])
        TIMT = str(TIMX[3]) + ":" + str(TIMX[4]) + ":" + str(TIMX[5])
        TIME = TIMD + " " + TIMT
        data = [NAME, TIME, round(dataS[0], 2), round(dataS[1], 2),
                int(round(dataS[2], 0)), int(round(dataS[3], 0)), int(round(dataS[4], 0))]
        print (data)
        stored.append(data)
        dataS = [0, 0, 0 ,0, 0]
        averageC = 0
    else:
        averageC += 1
    alarm(dataS)
    LED("off")

########################################################## Display the sensor data in the display
def display():
    global timingS, displayV, HOST, MAC,visual
    
    dur = hpt.buttonHold(button.value(), time.time())
    if (dur > 0.5 and dur < 4.5):
        oled.poweron()
        timingS = time.time()
        displayV = 1
    elif (dur > 4.5):
        oled.poweron()
        timingS = time.time()
        displayV = 2    
        
    if ((time.time() - timingS) >= 30):
        oled.poweroff()
        oled.fill(0)
        displayV = 0
        LED("off")
        
    if (displayV == 1):
        LED("green")
        temp, humi, voc, nox, co2 = measure()
        oled.fill(0)
        oled.contrast(125)
        oled.text (NAME, 0, 0)
        oled.text ("Temp:", 0, 11)
        oled.text (str(temp), 40, 11)
        circle(84, 11, 2)
        oled.text ("C", 88, 11)
        oled.text ("Humi:", 0, 22)
        oled.text (str(humi), 40, 22)
        oled.text ("%RH", 80, 22)
        if (sensor [2] == 0x59):
            oled.text ("VOC :", 0, 33)
            oled.text (str(voc), 40, 33)
            oled.text ("ppm", 80, 33)
            oled.text ("NOx :", 0, 44)
            oled.text (str(nox), 40, 44)
            oled.text ("ppm", 80, 44)
            
        if (sensor[3] == 0x62):
            oled.text ("CO2 :", 0, 55)
            oled.text (str(co2), 40, 55)
            oled.text ("ppm", 80, 55)

            
    elif (displayV == 2):
        LED("off")
        oled.text (NAME, 0, 0)
        oled.text ("IP adress:", 0, 11)
        oled.text (str(HOST), 10, 22)
        oled.text ("MAC adress:", 0, 33)
        oled.text (str(MAC)[:9], 10, 44)
        oled.text (str(MAC)[9:], 30, 55)
    oled.show()       
    
########################################################## Getting sensor data
def measure():
    global startM
    
    if (sensor[3] == 0x62 and startM):
        scd41.periodic_measurement()
        startM = False
    temp, humi = hpt.sensorData(0xFD)
    if (temp == "ERROR" or humi == "ERROR"):
        LED("blue")
        keep = 1
    else:
        keep = 0
    
    if (sensor[2] == 0x59):
        voc, nox = 0, 0 # replace with SPG41 data read
    else:
        voc, nox = 0, 0
        
    if (sensor[3] == 0x62):
        if (scd41.data_ready_status):
            if (hpt.delay(5)):
                dataco = scd41.read_measurement()
                co2 = dataco[2]
    else:
        co2 = 0
        
    return temp, humi, voc, nox, co2

########################################################## Function for measuring the sensor data
def scanI2C(i2c):
    global sensor
    print('Scan i2c bus...')
    devices = i2c.scan()

    if len(devices) == 0:
        print("No i2c device !")
    else:
        print('i2c devices found:',len(devices))
        for device in devices:  
            print("Decimal address: ",device," | Hexa address: ",hex(device), type(device))
            if device == 0x3C or device == 0x3D:
                sensor [0] = device
            elif device == 0x44:
                sensor[1] = device
            elif device == 0x59:
                sensor[2] = device
            elif device == 0x62:
                sensor[3] = device
                
########################################################## Display initialisation
def displayInit(i2c):
    global sensor, oled
    oled = SSD1306_I2C(128, 64, i2c, sensor[0])
    oled.fill(0)
    oled.blit(hpt.logo(), 32, 0) #print UU logo
    oled.show()
                
########################################################## Main function
def main():
    global HOST, MAC, i2c, timeOut
    scanI2C(i2c)
    displayInit(i2c)
    while 1:
        print(HOST)
        if (HOST == "NONE"):
            LED("red")
            if ((time.time()-timeOut) >= 60):
                HOST, MAC = w5x00_init()
        else:
            dataComm(HOST, PORT)
        display()
                               

if __name__ == "__main__":
    main()
 