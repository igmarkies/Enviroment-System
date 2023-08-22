import machine, ssd1306, time
i2c = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2))
oled = ssd1306.SSD1306_I2C(128, 64, i2c, 0x3D)
button = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
dReset = machine.Pin(22, machine.Pin.OUT)
dReset.value(1)
dReset.value(0)
dReset.value(1)
DEBUG = 1
timeOn = 500
display = timeOn
x = 12
direct = 0

while 1:
    if button.value() == 0:
        oled.poweron()
        display = 0
        
        oled.fill(0)
        oled.contrast(255)
        oled.text("Hello World", 0, 0)
        oled.text("IT WORKS!!!", 0, x)
        oled.show()
    if DEBUG:
        print ("Row counter:", x)
        print ("Power-on counter:", display)
        print ("button state", button.value())
        
    if display == timeOn:
        oled.poweroff()
        x = 12
        display += 1
    elif display < timeOn:
        display += 1
        if direct == 0:
            x = x + 1
        else:
            x = x - 1
        if x == 58:
            direct = 1
        elif x == 12:
            direct = 0
        