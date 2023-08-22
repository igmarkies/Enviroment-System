import socket as socket
from machine import Pin,SPI, I2C
from HPT import HPT
import network
import rp2
import time, utime

bad_chars = ['[', ']', "'", '"', ", "]
i2c = I2C(1, scl=machine.Pin(3), sda=machine.Pin(2), freq = 100000)
hpt = HPT(i2c)
led = Pin(25, Pin.OUT)
PORT = 52171  # The port used by the server
tryCon = 0
Try = 0 
#W5x00 chip init
def w5x00_init():
    tryCon = 0
    spi=SPI(0,2_000_000, mosi=Pin(19),miso=Pin(16),sck=Pin(18))
    nic = network.WIZNET5K(spi,Pin(17),Pin(20)) #spi,cs,reset pin
    nic.active(True)
    wait = "Trying to connect "
    while not nic.isconnected():
        time.sleep(1)
        tryCon += 1
        print (wait, "Try:", tryCon)
        #print(nic.regs())
    
    ip,sn,gw,dns = nic.ifconfig()
    mac = nic.config('mac')
    #nic.ifconfig((ip,sn,gw,dns))
    print('IP      : ', ip)
    print('Subnet  : ', sn)
    print('Gateway : ', gw)
    print('DNS     : ', dns)
    print('MAC     : ', mac)
    #print(hex(mac[5]))
    return ip
    
    
    
def main():
    HOST = w5x00_init()
    name = 0x01
#     Temp = 21.45
#     Humi = 54.64
    VOC, NOx, CO2 = 0,0,0
    while 1:
        print (HOST)
        Temp, Humi = hpt.sensorData(0xFD)
        cTime = time.time()
        arr = [name, cTime, Temp, Humi, VOC, NOx, CO2]
        arr = str(arr)
        arr = ''.join((filter(lambda i: i not in bad_chars, arr)))
        print(arr)
        #print(type (arr))

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            s.settimeout(1)
            s.listen()
            conn, addr = s.accept()
            if conn:
                print(f"Connected by {addr}")
                while True:
                    s.settimeout(1)
                    data = conn.recv(1024)
                    print ("Data:",str(data, 'utf8'), end = '')
                    print ("\n")
                    if data == (b'Request data'):
                        data = str(arr)
                        print("data:", data, type(data))
                        conn.sendall(data)
                        s.settimeout(10000)
                    elif data ==(b'ACK'):
                        conn.close()
                        s.close()
                        break
                    else:
                        conn.sendall(data)
        except:
            try:
                conn.close()
                s.close()
            except:
                print("nothing to close")
            print("no connection")
                

if __name__ == "__main__":
    main()
