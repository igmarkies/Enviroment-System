############################################################################
#Software: Sensor module main software
#Creator: Ian Markies
#Version: 1.4
#Description:
#    This software is the main software for the sensormodules V2.7
#    This code handles the ethernet communication, data collection and display
############################################################################

import usocket as socket
from machine import Pin, SPI, I2C, Timer, RTC
from HPT import HPT
from SCD41 import SCD41
from ssd1306 import SSD1306_I2C
import network, rp2, time, utime, math, neopixel, machine
import ustruct as struct

###################Configuration#########################
NAME = "HPTsen2"
visual = 30 # the time the display is on
alarmLimit = [350, 200, 1500] # Limits for the alarm
dim = 10 # The RGB LED dim value (255/10)
flashData = True
###################DON'T CHANCE##########################
timer=Timer(-1)
timer.init(period=60000, mode=Timer.PERIODIC, callback=lambda t:saveData())   #initializing the timer (60000)

# file = open(fileName, "w")

reset = machine.Pin(22, machine.Pin.OUT, machine.Pin.PULL_DOWN)
button = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
led = neopixel.NeoPixel(Pin(23), 1)
led[0] = (0, 0, 0)
led.write()
reset.on()
reset.off()
reset.on()

i2c = I2C(1, scl=machine.Pin(3), sda=machine.Pin(2))
hpt = HPT(i2c)
scd41 = SCD41(i2c)
spi=SPI(0,2_000_000, mosi=Pin(19),miso=Pin(16),sck=Pin(18))
nic = network.WIZNET5K(spi,Pin(17),Pin(20)) #spi,cs,reset pin

stored = []
dataM = [0, 0, 0, 0, 0]
dataS = [0, 0, 0, 0, 0]



tempA, humiA, vocA, noxA, co2A = 0, 0, 0, 0, 0
PORT = 52171  # The port used by the server

pwm = machine.PWM(machine.Pin(5))
pwm.duty_u16(0)
startB, delay, switch, buz1, buz2 = 0, 1, 0, 0, 0
averageC, timingS, displayV, flip, blinkS = 0, 0, 0, False, True
HOST, MAC = "NONE", "NONE"
startM, init, alarmS = True, 0, 0
temp, humi, voc, nox, co2 = -1, -1, -1, -1, -1
    
######################################################### Search i2c devices    
sensor = [0x00, 0x00, 0x00, 0x00]
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
            
oled = SSD1306_I2C(128, 64, i2c, sensor[0])
oled.fill(0)
oled.blit(hpt.logo(), 32, 0) #print UU logo
oled.show()

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

######################################################### RGB LED function
def LED (arg):
    global led
    
    if (arg == "Off"):
        red, green, blue = [0, 0, 0]
        
    elif (arg == "Red"):
        red, green, blue = [255, 0, 0]
    elif (arg == "Green"):
        red, green, blue = [0, 255, 0]
    elif (arg == "Blue"):
        red, green, blue = [0, 0, 255]
        
    elif (arg == "Yellow"):
        red, green, blue = [255, 255, 0]
    elif (arg == "Magenta"):
        red, green, blue = [255, 0, 255]
    elif (arg == "Cyan"):
        red, green, blue = [0, 255, 255]
    else:
        red, green, blue = [0, 0, 0]
        print("Color not found")
        
    led[0] = (int(round((red/dim), 0)), int(round((green/dim), 0)), int(round((blue/dim), 0)))
    led.write()
            
######################################################### Connecting to the network (W5100 ethernet interface)
def w5100s():
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
            LED ("Red")
            break
        else:
            NC = False
            
        #print(nic.regs())
    if NC:
        ip = 0
        MAC = 0
        LED ("Red") 
    else:
        LED ("Off")
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
        getTime()
    if NC:
        ip = "NONE"
        count = 0
    return ip, MAC

########################################################## Datacommunication with the main module
def dataComm(HOST, PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    oled.fill(0)
    oled.contrast(125)
    try:
        s.settimeout(1)			# don't make smaller, any smaller and the communication will fail
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        if conn:
            for b in range (len(stored)):
                print(b+1, "/", len(stored), ":", stored[b])
            LED ("Yellow")
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
                    LED ("Off")
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
                    for b in range (len(stored)):
                        print(1, "/", len(stored), ":", stored[b])
                    data = stored[0]
#                     print(data, type(data))
                    dataT = str(data)
#                     print(dataT, type(dataT))
                    conn.sendall(dataT)
                    state = 4
                    
                
                elif (state == 4):
                    dataR = conn.recv(1024)
                    print("State 4 receive: ", dataR)
                    
                    if (dataR == b'NEXT'):
                        print("deleting:", stored[0])
                        del stored[0]
                        print(dataC)
                        state = 3
                    elif (dataR == b'ACK'):
                        del stored[0]
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
                        LED ("Off")
                        break
                    else:
                        state = 5
                        dis += 1
    except:
        LED ("Off")
        s.close()
        #print("No connection")

########################################################## Alarm for a too high VOC/NOx/CO2
def alarm(dataS):

    global alarmS
    temp, humi, VOC, NOx, CO2 = dataS

    if (CO2 > alarmLimit[2]):
        LED ("Magenta")
        print ("CO2 is too HIGH", co2)
        oled.poweron()
        oled.fill(0)
        oled.contrast(125)
        oled.text ("CO2 to high!", 0, 11)
        oled.text ("Ventilate the", 0, 33)
        oled.text ("room", 0, 44)
        buzzer("start")
        alarmS = 1
    if (NOx > alarmLimit[1]):
        LED ("Magenta")
        print ("NOx is too HIGH")
        oled.poweron()
        oled.fill(0)
        oled.contrast(125)
        oled.text ("NOx to high!", 0, 11)
        oled.text ("Ventilate the", 0, 33)
        oled.text ("room", 0, 44)
        buzzer("start")
        alarmS = 1
    if (VOC > alarmLimit[0]):
        LED ("Magenta")
        print ("VOC is too HIGH")
        oled.poweron()
        oled.fill(0)
        oled.contrast(125)
        oled.text ("VOC to high!", 0, 11)
        oled.text ("Ventilate the", 0, 33)
        oled.text ("room", 0, 44)
        buzzer("start")
        alarmS = 0
    if (CO2 < alarmLimit[2] and NOx < alarmLimit[1] and VOC < alarmLimit[0]):
        if (alarmS == 1):
            oled.fill(0)
            oled.poweroff()
            alarmS = 0
        buzzer("stop")
        LED ("Off")
        StartB = 0
    
#########################################Buzzer function
def buzzer (arg):
    global startB, delay, switch, buz1, buz2
    pwm.freq(1000)
    dura = hpt.buttonHold(button.value(), time.time())
    
    if (dura > 2.5):
        delay = 900
        
    if (startB == 0 and arg == "start"):
        print("buzzer start")
        buz1 = time.time()
        buz2 = 0
        delay = 1
        switch = 0
        startB = 1

    if(arg == "stop"):
        startB = 0
        switch = 2
        pwm.duty_u16(0)
        
        
    if (time.time() > buz1+delay and switch == 0):
        pwm.duty_u16(20000)
        buz2 = time.time()
        switch = 1
        
    elif (time.time() > buz2+delay and switch == 1):
        pwm.duty_u16(0)
        buz1 = time.time()
        switch = 0
########################################################## Function to save the data
def saveData():
    global sensor, averageC, dataS
    LED ("Blue")
    print ("saving data", averageC)
    dataB = measure()
    print (dataB)
    for v in range (5):
        dataS[v] += dataB[v]
    print (averageC, ":", dataS)
    
    if averageC == 9:
        for d in range (5):
            dataM[d] = dataS[d] / 10
        print("Storing data")
        TIMX = time.localtime()
        if TIMX[1] < 10:
            month = "0" + str(TIMX[1])
        else:
            month = str(TIMX[1])  
        if TIMX[2] < 10:
            day = "0" + str(TIMX[2])
        else:
            day = str(TIMX[2])
            
        if TIMX[3] < 10:
            hour = "0" + str(TIMX[3])
        else:
            hour = str(TIMX[3])
            
        if TIMX[4] < 10:
            minute = "0" + str(TIMX[4])
        else:
            minute = str(TIMX[4])
            
        if TIMX[5] < 10:
            second = "0" + str(TIMX[5])
        else:
            second = str(TIMX[5])
        
        TIMD = day + "-" + month + "-" + str(TIMX[0])
        TIMT = hour + ":" + minute + ":" + second
        TIME = TIMD + " " + TIMT
        data = [NAME, TIME, round(dataM[0], 2), round(dataM[1], 2),
                int(round(dataM[2], 0)), int(round(dataM[3], 0)), int(round(dataM[4], 0))]
        print (data)
    
        LED("Green")
        stored.append(data)     
        
        dataS = [0, 0, 0 ,0, 0]
        averageC = 0
    else:
        averageC += 1
        
    alarm(dataB)
    LED ("Off")

########################################################## Display the sensor data in the display
def display():
    global timingS, displayV, HOST, MAC,visual, temp, humi, voc, nox,co2
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
        displayV = 0
        oled.poweroff()
        oled.fill(0)
        
    if (displayV == 1):
        oled.fill(0)
        oled.contrast(125)
        oled.text (NAME, 0, 0)
        oled.text ("Temp:", 0, 11)
        oled.text (str(temp), 40, 11)
        circle(84, 11, 2)
        oled.text ("C", 88, 11)
        oled.text ("Humi:", 0, 22)
        oled.text (str(humi), 40, 22)
        oled.text ("%RH", 82, 22)
        if (sensor [2] == 0x59):
            oled.text ("VOC :", 0, 33)
            oled.text (str(voc), 40, 33)
            oled.text ("ppm", 82, 33)
            oled.text ("NOx :", 0, 44)
            oled.text (str(nox), 40, 44)
            oled.text ("ppm", 82, 44)
            
        if (sensor[3] == 0x62):
            oled.text ("CO2 :", 0, 55)
            oled.text (str(co2), 40, 55)
            oled.text ("ppm", 82, 55)
        oled.show()
            
    elif (displayV == 2):
        LED("Off")
        oled.text (NAME, 0, 0)
        oled.text ("IP adress:", 0, 11)
        oled.text (HOST, 10, 22)
        oled.text ("MAC adress:", 0, 33)
        oled.text (MAC[:9], 10, 44)
        oled.text (MAC[9:], 30, 55)
        oled.show()       
    
########################################################## Function for measuring the sensor data
def measure():
    global startM, temp, humi, voc, nox, co2
    LED("Blue")
    sco2 = 0
    if (sensor[3] == 0x62 and startM):
        scd41.periodic_measurement()
        startM = False
    if (sensor[1] == 0x44):
        temp, humi = hpt.sensorData(0xFD)
        if (temp == "ERROR" or humi == "ERROR"):
            LED("Cyan")
    
    if (sensor[2] == 0x59):
        voc, nox = 0, 0 # replace with SPG41 data read
    else:
        voc, nox = 0, 0
        
    if (sensor[3] == 0x62):
        if (scd41.data_ready_status):
            while(sco2 == 0):
                dataco = scd41.read_measurement()
                sco2 = dataco[2]
            co2 = sco2
    else:
        co2 = -1
    LED("Off")
    return temp, humi, voc, nox, co2

########################################################## Function to het the time over the network
def getTime():
    print("Local time before synchronization：%s" %str(time.localtime()))
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    NTP_DELTA = 2208988852
    addr = socket.getaddrinfo('185.216.161.42', 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    res = s.sendto(NTP_QUERY, addr)
    msg = s.recv(48)
    val = struct.unpack("!I", msg[40:44])[0]
    val -= NTP_DELTA
    tm = time.gmtime(val)
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6], tm[3] + 2, tm[4], tm[5], 0))
    print("RTC is set")
    print("Local time after synchronization ：%s" %str(time.localtime()))

########################################################## Main funtion
def main():
    global HOST, MAC
    color = ["Red", "Yellow", "Green", "Cyan", "Blue", "Magenta", "Off"]
    timStart = time.time()
    v = 0
    while 1:
        buzzer("start")
        LED(color[v])
        
        if time.time() - timStart >= 2:
            v += 1
            timStart = time.time()
        
        if v > 6:
            buzzer("stop")
            break
    
    while 1:
        if (HOST == "NONE"):
            print("connect")
            LED("Red")
            HOST, MAC = w5100s()
        else:
            dataComm(HOST, PORT)
        display()
                               

if __name__ == "__main__":
    main()
 