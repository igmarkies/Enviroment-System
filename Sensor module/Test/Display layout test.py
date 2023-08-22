from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf, time
import array

button = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)

DEBUG = 1
display = 1000
delay = 0
width = 128
height = 64
state = 0
maxDelay = 556 # 30 sec is ongeveer 556, 1 min is ongeveer 1160
run = 0

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

fb = framebuf.FrameBuffer(bytearray(
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc0\x00\x00\x00\x00\x00\x00\x1f\xf4\x00\x00\x00\x00\x00\x03\x3b\x3c\xe0\x00\x00'
    b'\x00\x00\x0d\x1b\x6e\xf8\x00\x00\x00\x00\x05\xcb\xee\x50\x00\x00\x00\x00\xb9\x9b\xec\xc6\x80\x00\x00\x03\x9a\xfb\xef\xa6\xa0\x00'
    b'\x00\x01\x46\xfb\xef\xb0\x60\x00\x00\x0d\xbe\x79\xef\x3f\x68\x00\x00\x00\x9f\x79\xef\x7e\xdc\x00\x00\x30\xdf\x39\xcf\x7d\x9e\x00'
    b'\x00\x5b\xef\xb9\xce\x79\xcd\x00\x00\xef\xe7\x9d\xce\xf3\xfb\x80\x00\xf3\xf3\x9d\xcc\xf7\xf7\xc0\x01\x19\xf3\x9c\xcc\xe7\xce\x40'
    b'\x03\xbc\xf9\xcc\x98\xcf\x9e\x60\x03\xfe\x3c\xcc\x99\x8f\x3f\xe0\x06\xff\x1c\x44\x99\x9e\x7f\x90\x07\x3f\x8e\x60\x03\x38\xfe\x70'
    b'\x00\x4f\xc6\x00\x00\x31\xf9\xf0\x00\x73\xe1\x00\x00\x63\xe3\xc0\x09\xf8\x78\x00\x00\x07\x8f\x9c\x1c\xfe\x1c\x00\x00\x0c\x3f\xfc'
    b'\x0e\xff\x84\x00\x00\x10\x7f\xf8\x18\x3f\xc0\x00\x00\x01\xff\x0c\x1f\x83\xf0\x0f\xfc\x07\xe0\x7c\x01\xf0\x00\x1f\xfc\x04\x07\xf0'
    b'\x13\xfe\x00\x18\x04\x00\x3f\xc6\x01\xff\xe0\x1c\x04\x03\xff\xe0\x3f\xff\xf0\x1e\x04\x07\xff\xfe\x10\x00\x00\x1f\x04\x00\x00\x06'
    b'\x3f\xe0\x00\x1f\x84\x00\x01\xfe\x3f\xff\xf0\x1f\xc4\x03\xff\xfe\x0b\xff\x80\x1f\xe4\x00\xff\xd0\x01\xfc\x00\x1f\xfc\x00\x1f\xc4'
    b'\x0f\xe0\x38\x0f\xf8\x06\x03\xec\x1e\x07\xf0\x01\xc0\x03\xf8\x3c\x10\xff\xc0\x00\x00\x00\xff\x84\x0f\xff\x0c\x00\x00\x18\x7f\xfc'
    b'\x1c\xfc\x38\x00\x00\x0e\x1f\xfc\x05\x78\xf1\x00\x00\x47\x87\x80\x01\xe3\xe3\x00\x00\x63\xf3\xe0\x03\x8f\xc6\x20\x02\x31\xfc\xf0'
    b'\x06\x3f\x8e\x64\x11\x1c\xff\x30\x01\xff\x3c\xc4\x99\x9e\x7f\xc0\x03\x9e\x78\xcc\x99\xcf\x3d\xe0\x00\x1c\xf9\xcc\xcc\xcf\x9c\x60'
    b'\x01\x99\xf3\x9c\xcc\xe7\xef\x00\x00\x37\xf7\x9d\xcc\xf3\xf7\x80\x00\x6d\xe7\xbd\xce\x7b\xfb\x80\x00\x1c\xcf\x39\xce\x79\xdc\x00'
    b'\x00\x3c\xdf\x39\xcf\x7c\xce\x00\x00\x1d\xbf\x79\xef\x3e\xe0\x00\x00\x03\x6e\x79\xef\xbf\x60\x00\x00\x03\x76\xfb\xef\xb3\x20\x00'
    b'\x00\x00\xf6\xfb\xef\x9b\x80\x00\x00\x00\xe5\xdb\xe8\x99\x80\x00\x00\x00\x2d\x9b\xec\x1c\x00\x00\x00\x00\x0f\x9b\x2c\x38\x00\x00'
    b'\x00\x00\x01\xbb\x3e\x20\x00\x00\x00\x00\x00\x1f\xf4\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    64, 64, framebuf.MONO_HLSB)


i2c = I2C(id = 1, scl = Pin(3), sda = Pin(2), freq = 200000)

oled = SSD1306_I2C(width, height, i2c, 0X3D)
while 1:
    cTime = time.gmtime()
    hour = cTime[3]
    minute = cTime[4]
    second = cTime[5]
    if display == 1 or display == maxDelay -1:
        print(cTime)
    
    if button.value() == 0:
        oled.poweron()
        display = 0
        delay = 0
        state = 1
    elif display >= maxDelay:
        oled.poweroff()
        state = 0
    elif display < maxDelay and state == 2:
        display += 1
        time.sleep_us(10)
############################################################## State 1          
    if state == 1:
        oled.fill(0)
        oled.blit(fb,32,0) #print UU logo
        oled.show()
        delay += 1
        
        if DEBUG:
            print (delay)
        
        if delay == 10:
            delay = 0
            state = 2
############################################################## State 2           
    elif state == 2:
        if DEBUG:
            print (display)
#################################### Time in formate
        if hour < 10:
            hourString = "0" + str(hour)
        else:
            hourString = str(hour)
        if minute < 10:
            minString = "0" + str(minute)
        else:
            minString = str(minute)
        if second < 10:
            secString = "0" + str(second)
        else:
            secString = str(second)
#################################### Data on oled display            
        oled.fill (0)
        oled.text ("Sensor room 1", 0, 0)
        oled.text ("Time:", 0, 12)
        oled.text (hourString, 40, 12)
        oled.text (":", 54, 12)
        oled.text (minString, 60, 12)
        oled.text (":", 74, 12)
        oled.text (secString, 80, 12)
        oled.text ("Temp:", 0, 24)
        oled.text ("C", 80, 24)
        oled.text ("Humi:", 0, 36)
        oled.text ("%RH", 80, 36)
        oled.text ("ID:", 0, 50)
        oled.show()
  