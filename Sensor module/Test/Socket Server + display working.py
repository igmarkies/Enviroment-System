import usocket as socket
from machine import Pin,SPI
from ssd1306 import SSD1306_I2C
import framebuf, array, math
import network
import rp2
import time, utime

reset = machine.Pin(22, machine.Pin.OUT, machine.Pin.PULL_DOWN)
reset.on()
reset.off()
reset.on()

i2c = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2))
oled = SSD1306_I2C(128, 64, i2c, 0X3D)
print ("display setup done")
led = Pin(25, Pin.OUT)
PORT = 52171  # The port used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
oled.poweroff()
led.value(0)

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
    return ip
    
    
    
def main():
    HOST = w5x00_init()
    if HOST != 0:
        led.value(1)
    oled.poweron()
    oled.text (str(HOST), 0, 0)
    oled.show()
    s.bind((HOST, PORT))
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
            if data == (b'Request data'):
                dSend = (b'')
            else:
                data = (b'Hey')
            conn.sendall(data)

if __name__ == "__main__":
    main()
