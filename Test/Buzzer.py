import machine

import time

pwm = machine.PWM(machine.Pin(5))
pwm.duty_u16(32768)     # set duty to 50%

print(pwm)



while True:
    pwm.freq(1000)
    pwm.duty_u16(20000)
    time.sleep(1)
    pwm.duty_u16(0)
    time.sleep(1)


