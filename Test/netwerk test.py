import usocket as socket
from machine import Pin,SPI
import network
import rp2
import time, utime, ntptime

led = Pin(25, Pin.OUT)
PORT = 52171  # The port used by the server
spi=SPI(0,2_000_000, mosi=Pin(19),miso=Pin(16),sck=Pin(18))
nic = network.WIZNET5K(spi,Pin(17),Pin(20)) #spi,cs,reset pin
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(0)
ip, mac, run = 0, 0, 0

#W5x00 chip init
def w5x00_init():
    tryCon = 0
    nic.active(False)
    nic.active(True)#------------------------------------------------------om deze regel gaat hij niet opnieuw kijken voor een verbinding
    wait = "Trying to connect "
    while not nic.isconnected():
        time.sleep(1)
        tryCon += 1
        print (wait, "Try:", tryCon)
        if (tryCon > 10):
            print ("Could not connect to the internet")
            tryCon = 0
            return 0, 0
            break
    if nic.isconnected():
        ip,sn,gw,dns = nic.ifconfig()
        mac = nic.config('mac')
        print('IP      : ', ip)
        print('Subnet  : ', sn)
        print('Gateway : ', gw)
        print('DNS     : ', dns)
        print('MAC     : ', end=" ")
        for i in range(6):
            if (int(mac[i]) < 10):
                a = "0" + str(hex(mac[i]))
            else:
               a = str(hex(mac[i])) 
            print(a, end="/")
        print(" ")
        #print(hex(mac[5]))
        return ip, mac   
    
    
def main():
    while True:
        connect = nic.status()
        print("connection:", connect)
        if (connect != 2):
            ip, mac = w5x00_init()
            run = 0
        else:
            print("Start socket")
            s.bind((ip, PORT))
            s.listen()
            conn, addr = s.accept()
            if conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    else:
                        print (str(data, 'utf8'), end = '')
                    if data == (b'Hello!'):
                        data = (b'Goodbye!')
                    else:
                        data = (b'Hey')
                    conn.sendall(data)
                    conn.close()
                time.sleep_ms(250)
        


if __name__ == "__main__":
    main()
