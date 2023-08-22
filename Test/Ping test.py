from usocket import socket
from machine import Pin,SPI
import uping
import network
import rp2
import time, utime

led = Pin(25, Pin.OUT)

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
    try:
        mac = str(mac[1], 'UTF-8')
    except:
        print("can't convert")
    #nic.ifconfig((ip,sn,gw,dns))
    print('IP      : ', ip)
    print('Subnet  : ', sn)
    print('Gateway : ', gw)
    print('DNS     : ', dns)
    print('MAC     : ', mac)
    print(hex(mac[5]))
    
    
    
def main():
    w5x00_init()
    
    while True:
        led.value(1)
        time.sleep(1)
        led.value(0)
        time.sleep(1)
        trans, recv = uping.ping("google.com")
        print("transmit:", trans, "receive:", recv)

if __name__ == "__main__":
    main()