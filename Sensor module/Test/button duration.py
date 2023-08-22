from HPT import HPT
import machine
import time
print("setup")
print("Hallo")

i2c = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2))
hpt = HPT(i2c)
button = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)

print ("Start")
while 1:
    time.sleep_ms(100)
    dura = hpt.buttonHold(button.value(), time.time())
    if (dura > 2.5):
        print("bigger then")
    elif (dura < 2.5):
        print("less then")
    
