from machine import Pin, Timer        #importing pin, and timer class
from HPT import HPT
from SCD41 import SCD41
import time, machine

i2c = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2))
hpt = HPT(i2c)
scd41 = SCD41(i2c)

scd41.periodic_measurement()

data = [0, 0, 0]
co2 = 0
file = open("data.csv", "w")

def save():
    global co2, data
    TIMX = time.localtime()
    if TIMX[1] < 10:
        month = "0" + str(TIMX[1])
    else:
        month = "0" + str(TIMX[1])  
    if TIMX[2] < 10:
        day = "0" + str(TIMX[2])
    else:
        day = "0" + str(TIMX[2])
        
    if TIMX[3] < 10:
        hour = "0" + str(TIMX[3])
    else:
        hour = str(TIMX[3])
    if TIMX[4] < 10:
        minute = "0" + str(TIMX[4])
    else:
        minute = str(TIMX[4]) 
    if TIMX[5] < 10:
        second = "0" + str(TIMX[5])
    else:
        second = str(TIMX[5])
    
    TIMD = day + "-" + month + "-" + str(TIMX[0])
    TIMT = hour + ":" + minute + ":" + second
    TIME = TIMD + " " + TIMT
    
    temp, humi = hpt.sensorData(0xFD)
    
    if (scd41.data_ready_status):
            while(co2 == 0):
                data = scd41.read_measurement()
                co2 = data[2]
    else:
        co2 = 0
    print (temp, humi, co2, "done")
    file.write(str(TIME) + ";" + str(temp) + ";" + str(humi) + ";" + str(co2) + "\n")
    file.flush()

start = 0
led = Pin(25, Pin.OUT)    # GPIO14 as led output
led.value(0)              # LED is off
timer=Timer(-1)
save()
timer.init(period=6000, mode=Timer.PERIODIC, callback=lambda t:save())   #initializing the timer


