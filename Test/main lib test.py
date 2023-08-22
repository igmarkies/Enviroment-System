from HPT import HPT
from SCD41 import SCD41
from ssd1306 import SSD1306_I2C
import machine, time, struct, math
ronde = 0
rtc = machine.RTC()
rtc.datetime((2023, 4, 6, 2, 11, 20, 0, 0))

Timer = machine.Timer()
timer=machine.Timer(-1)
file = open("data test lib.csv", "w")
timR = 0
dateR = 0
temp = 0
rh = 0
co2 = 0
co2S = False

def save(date, timeS, TEMP, RH, CO2):
    #print (time.localtime(), "done")
    date = str(date)
    timeS = str(timeS)
    TEMP = str(TEMP)
    TEMP = TEMP.replace(".", ",")
    RH = str(RH)
    RH = RH.replace(".", ",")
    CO2 = str(CO2)
    file.write(date + ";" + timeS + ";" + TEMP + ";" + RH + ";" + CO2 + "\n")
    file.flush()

reset = machine.Pin(22, machine.Pin.OUT, machine.Pin.PULL_DOWN)
#button = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
reset.on()
reset.off()
reset.on()

i2c = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2), freq = 100000)
hpt = HPT(i2c)
scd = SCD41(i2c)
oled = SSD1306_I2C(128, 64, i2c, 0X3D)
timer.init(period=600000, mode=Timer.PERIODIC, callback=lambda t:save(dateR, timR, temp, rh, co2))

if co2S:
    scd.periodic_measurement()

def circle(x,y,r,color = 1,fill=0):       #A circular function
    if(fill==0):
        for i in range(x-r,x+r+1):
            oled.pixel(i,int(y-math.sqrt(r*r-(x-i)*(x-i))),color)
            oled.pixel(i,int(y+math.sqrt(r*r-(x-i)*(x-i))),color)
        for i in range(y-r,y+r+1):
            oled.pixel(int(x-math.sqrt(r*r-(y-i)*(y-i))),i,color)
            oled.pixel(int(x+math.sqrt(r*r-(y-i)*(y-i))),i,color)
    else:
        for i in range(x-r,x+r+1):
            a=int(math.sqrt(r*r-(x-i)*(x-i)))
            oled.vline(i,y-a,a*2,color)

        for i in range(y-r,y+r+1):
            a=int(math.sqrt(r*r-(y-i)*(y-i)))
            oled.hline(x-a,i,a*2,color)

while 1:
    tim = time.localtime()
    dateR = str(tim[2]) + "-" + str(tim[1]) + "-" + str(tim[0])
    timR = str(tim[3]) + ":" + str(tim[4]) + ":" + str(tim[5])
    #print (dateR, timR)
    #SHT41
    temp, rh = hpt.sensorData(0xFD)
    
    #SCD41
    if co2S:
        if scd.data_ready_status():
            data = scd.read_measurement()
            co2 = data[2]
    else:
        co2 = 0
        
    print ("temp:", round(temp, 2), "RH:", round(rh, 2), "co2:", round(co2, 0))
        
    oled.fill(0)
    oled.contrast(255)
    oled.text ("Temp:", 0, 33)
    oled.text (str(temp), 40, 33)
    circle(84, 33, 2)
    oled.text ("C", 88, 33)
    oled.text ("Humi:", 0, 44)
    oled.text (str(rh), 40, 44)
    oled.text ("%RH", 80, 44)
    oled.text ("CO2 :", 0, 55)
    oled.text (str(co2), 40, 55)
    oled.text ("ppm", 80, 55)
    oled.show()
    if ronde == 0:
        save(dateR, timR, temp, rh, co2)
        ronde = 1
    time.sleep(5)
