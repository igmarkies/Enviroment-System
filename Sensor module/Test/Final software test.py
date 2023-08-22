import usocket as socket
from machine import Pin, SPI, I2C, Timer
from HPT import HPT
from SCD41 import SCD41
from ssd1306 import SSD1306_I2C
import network, rp2, time, utime

###################Configuration#########################
NAME = "HPTsen0"
button = 0
alarmLimit = [350, 200, 1500]
###################DON'T CHANCE##########################
timer=Timer(-1)
timer.init(period=60000, mode=Timer.PERIODIC, callback=lambda t:saveData())   #initializing the timer

reset = machine.Pin(22, machine.Pin.OUT, machine.Pin.PULL_DOWN)
button = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
reset.on()
reset.off()
reset.on()

i2c = I2C(1, scl=machine.Pin(3), sda=machine.Pin(2))
hpt = HPT(i2c)
scd41 = SCD41(i2c)

stored = []
dataS = [0, 0, 0, 0, 0]


tempA, humiA, vocA, noxA, co2A = 0, 0, 0, 0, 0
led = Pin(25, Pin.OUT)
PORT = 52171  # The port used by the server

pwm = machine.PWM(machine.Pin(5))
pwm.duty_u16(0)
startB, delay, switch, buz1, buz2 = 0, 1, 0, 0, 0
averageC = 0

led.value(0)
    
#########################################################Search i2c devices    
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
            
#########################################################Connecting to the network (W5100 ethernet interface)
def w5x00_init():
    spi=SPI(0,2_000_000, mosi=Pin(19),miso=Pin(16),sck=Pin(18))
    nic = network.WIZNET5K(spi,Pin(17),Pin(20)) #spi,cs,reset pin
    nic.active(True)
    while not nic.isconnected():
        time.sleep(1)
        print ("-----")
        #print(nic.regs())
    
    ip,sn,gw,dns = nic.ifconfig()
    mac = nic.config('mac')
    #nic.ifconfig((ip,sn,gw,dns))
    print('IP      : ', ip)
    print('Subnet  : ', sn)
    print('Gateway : ', gw)
    print('DNS     : ', dns)
    print('MAC     : ', mac)
    for i in range (6):
        print(hex(mac[i]))
    return ip



##########################################################Datacommunication with the main module
def dataComm(HOST, PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    oled.fill(0)
    oled.contrast(125)
    oled.text(str(HOST), 0, 0)
    oled.show()
    try:

        s.settimeout(1)			# don't make smaller, any smaller and the communication will fail
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        if conn:
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
                        break
                    else:
                        state = 5
                        dis += 1
    except:
        s.close()
        #print("No connection")

def alarm():

    VOC, NOx, co2 = 0, 500, 1400
    if (sensor[3] == 0x62):
        if (data_ready_status):
            data = scd41.read_measurement()
            co2 = data[2]
    if (sensor [2] == 0x59):
        VOC, NOx = 40, 1		#replace with SPG41 measurement and ga index algirithm

    if (co2 > alarmLimit[2]):
        print ("CO2 is too HIGH", co2)
        buzzer()
    if (NOx > alarmLimit[1]):
        print ("NOx is too HIGH")
        buzzer()
    if (VOC > alarmLimit[0]):
        print ("VOC is too HIGH")
        buzzer()
    if (co2 < alarmLimit[2] and NOx < alarmLimit[1] and VOC < alarmLimit[0]):
        pwm.duty_u16(0)
        StartB = 0
    
#########################################Buzzer function
def buzzer ():
    global startB, delay, switch, buz1, buz2
    print("Buzzer", delay)
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

def saveData():
    
    global sensor, averageC, dataS
    print ("saving data", averageC)
    if (sensor[1] == 0x44):
        temp, humi = hpt.sensorData(0xFD)
        print (temp, humi)
        dataS[0] += temp
        dataS[1] += humi
    else:
        dataS[0] = 0
        dataS[1] = 0
        
    if (sensor[2] == 0x59):
        voc = 100
        nox = 1
        dataS[2] += voc
        dataS[3] += nox
    else:
        dataS[2] = 0
        dataS[3] = 0
        
    if (sensor[3] == 0x62):
        co2 = read_measurement()
        dataS[4] += co2
    else:
        dataS[4] = 0
    
    if averageC == 9:
        for d in range (5):
            dataS[d] = dataS[d] / 10
        print("Storing data")
        TIME = 000000000000
        data = [NAME, TIME, round(dataS[0], 2), round(dataS[1], 2),
                int(round(dataS[2], 0)), int(round(dataS[3], 0)), int(round(dataS[4], 0))]
        print (data)
        stored.append(data)
        tempA, humiA, vocA, noxA, co2A = 0, 0, 0, 0, 0
        averageC = 0
    else:
        averageC += 1
    
def main():
    HOST = w5x00_init()
    while 1:
        dataComm(HOST, PORT)
        alarm()
                               

if __name__ == "__main__":
    main()
 