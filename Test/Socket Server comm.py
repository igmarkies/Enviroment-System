import usocket as socket
from machine import Pin,SPI
import network
import rp2
import time, utime

led = Pin(25, Pin.OUT)
PORT = 52171  # The port used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
led.value(0)
state = 0
cData = 0

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
    for i in range (6):
        print(hex(mac[i]))
    return ip, mac
    
    
    
def main():
    saved = 1
    HOST, MAC = w5x00_init()
    if HOST != 0:
        led.value(1)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    if conn:
        cont = 0
        dis = 0
        print(f"Connected by {addr}")
        while conn:
            if state == 0:
                if cont == 0:
                    dRecv = conn.recv(1024)
                    print ("Data:", dRecv)
                    if not dRecv:
                        dis += 1
                else:
                    if dRecv == (b'Request data'):
                        dSend = b'Amount, ' + bytearray(str(saved))
                        cont = 1
                    else:    
                        dSend = (b'NACK')
                        dis += 1
                        cont = 0
                conn.sendall(dSend)
                if cont == 1:
                    dRecv = s.recv(1024)
                    if dRecv == b'ACK':
                        dis = 0
                        state = 1
                    else:
                        dis += 1
                        dRecv = b'Request data'
                    
            if state == 1:
                dSend = ["HPT_S1", time.time(), 20.23, 65,98, 0, 0]
                conn.sendall(byteraary(dSend))
                
                dRecv = s.recv(1024)
                if dRecv == b'ACK':
                    if cData == saved
                        dSend = b'END'
                        conn.sendall(dSend)
                        s.close()
                    else:
                        cData += 1
                        dSend = b'NEXT'
                        conn.sendall(dSend)
                else:
                    dis += 1
                
            #dis = 3
            if (dis == 3):
                print("end connection")
                s.close()
                break

if __name__ == "__main__":
    main()
