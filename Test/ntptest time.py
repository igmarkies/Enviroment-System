import machine
import utime as time
from machine import Pin, RTC, SPI
from ssd1306 import SSD1306_I2C
import network,rp2
import usocket as socket
import ustruct as struct

host = '185.216.161.42'
NTP_DELTA = 2208988852
reset = machine.Pin(14, machine.Pin.OUT, machine.Pin.PULL_DOWN)
#button = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
reset.on()
reset.off()
reset.on()

i2c = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2))
oled = SSD1306_I2C(128, 64, i2c, 0X3D)

def w5x00_init():
    spi=SPI(0,2_000_000, mosi=Pin(19),miso=Pin(16),sck=Pin(18))
    nic = network.WIZNET5K(spi,Pin(17),Pin(20)) #spi,cs,reset pin
    nic.active(True) 
    while not nic.isconnected():
        time.sleep(1)
        print('.')
    ip,sm,gw,ns = nic.ifconfig()
    print('IP      : ', ip)
    print('Subnet  : ', sm)
    print('Gateway : ', gw)
    print('DNS     : ', ns)

def main():
    w5x00_init()
    rtc=RTC()
    val = 946684800 # jan 1, 2000 00:00:00
    oled.poweron()
    tm = time.gmtime(val)
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
    print("Local time before synchronization：%s" %str(time.localtime()))
    oled.text (str(time.localtime()), 0, 0)
    gettime()
    print("Local time after synchronization ：%s" %str(time.localtime()))
    oled.text (str(time.localtime()), 0, 10)
    oled.text (str(time.gmtime()), 0, 20)
    oled.show()

def gettime():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo("3.nl.pool.ntp.org", 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    res = s.sendto(NTP_QUERY, addr)
    msg = s.recv(48)
    val = struct.unpack("!I", msg[40:44])[0]
    print (val)
    val -= NTP_DELTA
    tm = time.gmtime(val)
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6], tm[3] + 2, tm[4], tm[5], 0))

if __name__ == "__main__":
    main()
