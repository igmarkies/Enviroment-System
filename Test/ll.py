import machine, neopixel, time

n = 1
p = 21
red = 0
green = 0
blue = 0
direr = 0
direg = 0
direb = 0
start = 0

led = neopixel.NeoPixel(machine.Pin(23), 1)
while True:
    
    if start == 0:
        direr = 1
        direg = 0
        direb = 0
        if red == 254:
            start = 1
    elif start == 1:
        direr = 0
        direg = 1
        direb = 0
        if green == 254:
            start = 2
    elif start == 2:
        direr = 0
        direg = 0
        direb = 1
        if blue == 254:
            start = 3   
    elif start == 3:
        direr = -1
        direg = 0
        direb = 0
        if red == 1:
            start = 4
    elif start == 4:
        direr = 0
        direg = -1
        direb = 0
        if green == 1:
            start = 5
    elif start == 5:
        direr = 0
        direg = 0
        direb = -1
        if blue == 1:
            start = 0
    
    red += direr
    green += direg
    blue += direb
    
    led[0] = (red, green, blue)
    led.write()
    
    print("red:", red, "green:", green, "blue:", blue)
    time.sleep_ms(10)
