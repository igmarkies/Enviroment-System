import machine, neopixel, time

led = neopixel.NeoPixel(machine.Pin(23), 1)


def LED (red, green, blue, blink):
    global flip, blinkS, led
    if (blink != 0):
        if blinkS:
            startBlink = time.time()
        if ((time.time() - startBlink) >= blink):
            flip = not flip
    else:
        flip = False
    
    if flip:
        led[0] = (0, 0, 0)
    else:
        led[0] = (red, green, blue)
    led.write()
    
LED (255, 0, 0, 0)