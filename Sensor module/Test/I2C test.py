import machine, ssd1306
reset = machine.Pin(22, machine.Pin.OUT)
reset.on()
reset.off()
reset.on()
i2c = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2))
oled = ssd1306.SSD1306_I2C(128, 64, i2c, 0x3d)

x = 8
direct = 0
while x > -1:
    oled.fill(0)
    oled.contrast(255)
    oled.text("Hello World", 0, 0)
    oled.text("IT WORKS!!!", 0, x)
    oled.show()
    if direct == 0:
        x = x + 1
    else:
        x = x - 1
    if x == 58:
        direct = 1
    elif x == 8:
        direct = 0
    