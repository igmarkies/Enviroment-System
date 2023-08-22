import machine
import time
button = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)

while True:
    print(button.value())
    #button = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)
    if not button.value():
        print('Button pressed!')
    else:
        print('Button not pressed!')
    time.sleep_ms(500)