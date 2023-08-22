import usocket as socket
from machine import Pin, SPI, I2C
from HPT import HPT
from SCD41 import SCD41
from ssd1306 import SSD1306_I2C
import network, rp2, time, utime

###################Configuration#########################
NAME = "HPTsen0"
button = 0
alarmLimit = [350, 200, 1500]
###################DON'T CHANCE##########################

reset = machine.Pin(22, machine.Pin.OUT, machine.Pin.PULL_DOWN)
button = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
reset.on()
reset.off()
reset.on()

i2c = I2C(1, scl=machine.Pin(3), sda=machine.Pin(2))
oled = SSD1306_I2C(128, 64, i2c, 0X3D)
hpt = HPT(i2c)
scd41 = SCD41(i2c)

stored = []
led = Pin(25, Pin.OUT)
PORT = 52171  # The port used by the server

pwm = machine.PWM(machine.Pin(5))
pwm.duty_u16(0)
tim = 0

led.value(0)
for i in range (10):
    stored.append(["HPTsen25, 123456789, -40.00, 0, 0, 0, 0"])
    
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
                print (state)
                if (dis == 3):
                    print ("Disconnected")
                    conn.close()
                    s.close()
                    state = 1
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
                        state = 3
                        dataC += 1
                    elif (dataR == b'ACK'):
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
        print("No connection")

def alarm(button):
    dura = hpt.buttonHold(button.value(), time.time())
    print (dura)
    if (dura >= 3):
        button = 1
    
    if (button == 1):
        dur = 10
    else:
        dur = 1
    VOC, NOx, co2 = 0, 500, 1600
    if (sensor[3] == 0x62):
        if (data_ready_status):
            data = scd41.read_measurement()
            co2 = data[2]
    if (sensor [2] == 0x59):
        VOC, NOx = 40, 1		#replace with SPG41 measurement and ga index algirithm

    if (co2 > alarmLimit[2]):
        print ("CO2 is too HIGH", co2)
        buzzer(1000, dur, tim)
    if (NOx > alarmLimit[1]):
        print ("NOx is too HIGH")
        buzzer(1500, dur, tim)
    if (VOC > alarmLimit[0]):
        print ("VOC is too HIGH")
        buzzer(2000, dur, tim)
    if (co2 < alarmLimit[2] and NOx < alarmLimit[1] and VOC < alarmLimit[0]):
        pwm.duty_u16(0)
        button = 0
    


def buzzer (freq, blink, tim):
    pwm.freq(freq)
    
    if (hpt.delay(blink)):
        pwm.duty_u16(20000)
    if (hpt.delay(1)):
        pwm.duty_u16(0)

def main():
    HOST = w5x00_init()
    o = 2600
    while 1:
        dataComm(HOST, PORT)
        alarm(button)
        
        #time.sleep(1)
        
    
    
                        

if __name__ == "__main__":
    main()
 