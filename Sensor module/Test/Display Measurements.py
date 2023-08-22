from HPT import HPT
from ssd1306 import SSD1306_I2C
import framebuf, time, machine, array, math

state = 0
width = 128
height = 64
temp = 20.36
humi = 25.25
CO2 = 1200
i = 0
count = 0
show = 0
showo = 1
macW = 0
macS = 0
# file=open("data.csv","w")
############################################################# Pin assignment

reset = machine.Pin(22, machine.Pin.OUT, machine.Pin.PULL_DOWN)
button = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
reset.on()
reset.off()
reset.on()
############################################################# Library INIT
i2c = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2))
hpt = HPT(i2c)
oled = SSD1306_I2C(width, height, i2c, 0X3D)
print ("setup done")
############################################################# Functions
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

oled.poweron()

while 1:
#     print("While")
#     if button.value() == 0 and state == 2 :
#         count = 0
#     elif button.value() == 0:
#         count = 0
#         state = 1
#     print (button.value())
    if hpt.delay(1):
        temp, humi = hpt.sensorData(0x2236)
        print(temp)
        count += 1
#         
#     if state == 0:
#         oled.poweroff()
#         
#         
#     elif state == 1:
    
        #reset.on()
    tim = hpt.time()
                

#         if count == 30:
#             count = 0
#             state = 0
#             oled.poweroff()    
    oled.fill(0)
    oled.contrast(255)

    oled.text ("HPTsen1", 0, 0)
    oled.text ("Temp:", 0, 11)
    oled.text (str(temp), 40, 11)
    circle(84, 33, 2)
    oled.text ("C", 88, 11)
    oled.text ("Humi:", 0, 22)
    oled.text (str(humi), 40, 22)
    oled.text ("%RH", 80, 22)
    if (sensor [2] == 0x59):
        oled.text ("CO2 :", 0, 33)
        oled.text (str(CO2), 40, 33)
        oled.text ("ppm", 80, 33)
        oled.text ("CO2 :", 0, 44)
        oled.text (str(CO2), 40, 44)
        oled.text ("ppm", 80, 44)
        
    if (sensor[3] == 0x62):
        oled.text ("CO2 :", 0, 55)
        oled.text (str(CO2), 40, 55)
        oled.text ("ppm", 80, 55)
    print("done", i)
    oled.show()
    time.sleep_ms(500)
