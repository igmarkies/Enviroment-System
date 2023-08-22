from HPT import HPT as hpt
from ssd1306 import SSD1306_I2C
import machine, time, struct, math

Timer = machine.Timer()
timer=machine.Timer(-1)
file = open("data.csv", "w")
temp = 0
rh = 0
co2 = 0

def save(TEMP, RH, CO2):
    print (time.localtime(), "done")
    file.write(str(round(TEMP, 2)) + "," + str(round(RH, 2)) + "," + str(round(CO2, 2)) + "\n")
    file.flush()

reset = machine.Pin(22, machine.Pin.OUT, machine.Pin.PULL_DOWN)
#button = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
reset.on()
reset.off()
reset.on()

i2c = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2), freq = 100000)
oled = SSD1306_I2C(128, 64, i2c, 0X3D)
timer.init(period=600000, mode=Timer.PERIODIC, callback=lambda t:save(temp, rh, co2))

square = (2 ** 16) - 1

CRC8_POLYNOMIAL = 0x131
crc_table = []
for crc in range(256):
    for crc_bit in range(8):
        if crc & 0x80:
            crc = (crc << 1) ^ CRC8_POLYNOMIAL;
        else:
            crc = (crc << 1);
        crc = crc%256
    crc_table.append(crc)
print (crc_table)
CRC_TABLE = crc_table

bint = struct.pack('>H', 1)
msb = bint[0]
lsb = bint[1]
crc = 0xff
crc ^= msb
crc = CRC_TABLE[crc]
if lsb is not None:
    crc ^= lsb
    crc = CRC_TABLE[crc]
crch = crc
dataCO2 = bint + bytes([crch])
i2c.writeto_mem(0x62, 0x21b1 , dataCO2, addrsize = 16)

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
    #SHT41
    i2c.writeto_mem(0X44, 0XFD, b'', addrsize = 8)
    time.sleep_ms(10)
    data = i2c.readfrom(0x44, 6)
    rawTemp = (data[0] << 8) + data[1]
    rawHumi = (data[3] << 8) + data[4]
    temp = -45 + 175 * (rawTemp/square)
    rh = 100 * (rawHumi / square)
    print("temperature:",temp, "C")
    print("Humidity:", rh, "%RH")
    
    #SCD41
    i2c.writeto_mem(0x62, 0xe4b8 , b'', addrsize = 16)
    time.sleep_ms(1)
    dataSCD = i2c.readfrom(0x62, 3)
    ready = ((dataSCD[0] & 0x07 == 0))
    print(ready)
    if ready:
        i2c.writeto_mem(0x62, 0xec05 , b'', addrsize = 16)
        time.sleep_ms(10)
        dataSCD = i2c.readfrom(0x62, 9)
        co2 = (dataSCD[0] << 8) | dataSCD[1]
        tempC = (dataSCD[3] << 8) | dataSCD[4]
        rhC = (dataSCD[6] << 8) | dataSCD[7]
        tempC = -45 + 175 * (temp / (2**16))
        rhC = 100 * (rh/(2**16))
        print ("temp:", round(temp, 2), "RH:", round(rh, 2), "co2:", round(co2, 0))

        oled.fill(0)
        oled.contrast(255)
        oled.text ("Temp:", 0, 33)
        oled.text (str(round(temp, 2)), 40, 33)
        circle(84, 33, 2)
        oled.text ("C", 88, 33)
        oled.text ("Humi:", 0, 44)
        oled.text (str(round(rh, 2)), 40, 44)
        oled.text ("%RH", 80, 44)
        oled.text ("CO2 :", 0, 55)
        oled.text (str(round(co2, 0)), 40, 55)
        oled.text ("ppm", 80, 55)
        oled.show()
    time.sleep(5)