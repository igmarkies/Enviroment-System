import usocket as socket
from machine import Pin,SPI
from HPT import HPT
import network
import rp2
import time, utime
import json

led = Pin(25, Pin.OUT)
HOST = "131.211.88.97"  # The server's hostname or IP address
PORT = 52171  # The port used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#W5x00 chip init
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
    
    
    
def main():
    w5x00_init()
    name = "Sensor 1"
    Temp = 21.68
    Humi = 54.64
    arr = [name, time.time(), Temp, Humi]
    data = "Sensor 1"
    arr = str(arr)
    #data = json.dumps(arr)
    s.connect((HOST, PORT))
    send = s.write(arr)
    print (send)
#     for byte in arr:
#         send = s.write(byte)
#         if byte != data [-1]:
#             s.sendall(',')
#         else:
#             s.sendall('\n')
    data = s.recv(2048)
    print (data)
    if data == b'ack':
        s.write (data)
        s.close()
if __name__ == "__main__":
    main()
