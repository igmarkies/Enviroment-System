############################################################################
#Software: HPT library
#Creator: Ian Markies
#Version: 1.2
#Description:
#    This software is the is the library necassary forfunctionality of the main.py code
############################################################################

from ssd1306 import SSD1306_I2C
import time, machine, framebuf, math

class HPT:

############################### Initialization #####################################
# The values are predefined, if an other value is needed you can redefine them
# Redefine values example: hpt = HPT(20, 30, 10)
# The variables in this function only need to be defined once
    def __init__ (self, i2c, addr_dis = 0x3D, delayTime = 0, start = 0, counter = 0):
        self.width = 128
        self.height = 64
        self.i2c = i2c
        #if addr_dis != 0:
            #self.oled = SSD1306_I2C(128, 64, self.i2c, addr_dis)
        self.delayTime = delayTime
        self.start = start
        self.counter = counter
        self.dateTime = ["0", "0", "0", "0", "0", "0"]
        self.statB = 0
        self.startB = 0
        
############################### Time delay function ################################                
    def delay(self, dly):
        #dlyT = dly / 2	
        dlyT = dly
        if self.counter <= 0:
            self.start = time.time()
            self.delayTime = 0
        if (time.time() - self.start) >= 1:		# Every 1 second it adds 1 to the delay counter (delayTime) en resets start
            self.start = time.time()
            self.delayTime += 1
        if self.delayTime == dlyT:
            self.counter = 0
        else:
            self.counter += 1
        return self.delayTime == dlyT
    
############################### CRC control function ###############################
# The poly is predefined for the SHT-85 sensor
    def calCRC (self, data, showData = False, poly = 0x31, finalXOR = 0x00, crc = 0xFF):
        #print ("calCRC:", data)
        poly += 0x100
        for b in data:
            crc ^= b
#             print("Data input:", chr(b), b, "CRC value:", crc)
            for bit in range (8):
                if crc & 0x80:
                    crc = (crc << 1) ^ poly
                else:
                    crc <<= 1
        crc ^= finalXOR            
        if showData:
            #print (crc)
            return (crc)
        else:
            #print (crc)
            return (crc == 0x00)


############################### Caluculate data function ###########################
    def calculateData(self, dataTemp, dataHumi):
        square = (2 ** 16) - 1		
        
        rawTemp = (dataTemp[0] << 8) + dataTemp[1]
        rawHumi = (dataHumi[0] << 8) + dataHumi[1]
        
        temp = (-45 + 175 * (rawTemp/square))-2
        RH = 100 * (rawHumi / square)
        #print (temp, RH)
        for x in range(5, 1, -1):
            temp = round (temp, x)
            RH = round (RH, x)
        return round(temp, 2), round (RH, 2)

############################### Data gathering function ############################
# The adress is predefined for the SHT-85 sensor        
    def sensorData(self, command, output = True, adress = 0x44):
        # variables needed for this function
        data = bytearray(6)
        tempData = bytearray(3)
        humiData = bytearray(3)
        calTemp = 0
        calHumi = 0

        try:
            self.i2c.writeto_mem(adress, command , b'', addrsize = 8) #send measurement command
        except:
            print ("Failed to send command to the sensor")

        try:
            time.sleep_ms(16)	# max time the sensor needs to measure
            data = self.i2c.readfrom(adress, 6) # Store sensor data in variable
#             print("sensor data type:", type(data))
            for x in range (3): # Split data for temperature and humidity
                tempData[x] = data [x]
                humiData[x] = data [x + 3]
        except:
            print("Failed to receive data from the sensor")
        if output:
            if self.calCRC(tempData, False) and self.calCRC(humiData, False):
                calTemp, calHumi = self.calculateData(tempData, humiData)
                return calTemp, calHumi
            else:
                print("CRC in invalid")
                return "ERROR", "ERROR"
        else:
            #tempData = tempData.decode()
            #humiData = humiData.decode()
            return tempData, humiData
        
############################### UU logo function ###################################        
    def logo(self):     
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
        return fb

############################### time to string function ############################
    def time (self):    
        cTime = time.gmtime()
        for i in range (6):
            if cTime[i] < 10:
                self.dateTime[i] = "0" + str(cTime[i])
            else:
                self.dateTime[i] = str(cTime[i])
        return self.dateTime
    
############################### Draw Circle function ###############################
    def circle(self, x,y,r,color = 1,fill = 0):       #A circular function
        self.oled.text("Gallo", 0, 0)
        if(fill==0):
            for i in range(x-r,x+r+1):
                self.oled.pixel(i,int(y-math.sqrt(r*r-(x-i)*(x-i))),color)
                self.oled.pixel(i,int(y+math.sqrt(r*r-(x-i)*(x-i))),color)
            for i in range(y-r,y+r+1):
                self.oled.pixel(int(x-math.sqrt(r*r-(y-i)*(y-i))),i,color)
                self.oled.pixel(int(x+math.sqrt(r*r-(y-i)*(y-i))),i,color)
        else:
            for i in range(x-r,x+r+1):
                a = int(math.sqrt(r*r-(x-i)*(x-i)))
                self.oled.vline(i,y-a,a*2,color)

            for i in range(y-r,y+r+1):
                a = int(math.sqrt(r*r-(y-i)*(y-i)))
                self.oled.hline(x-a,i,a*2,color)
        self.oled.show()
        
############################### Button hold detection function ######################
    def buttonHold (self, button, timeB):
        #time.sleep_ms(100)
        dura = 0
        print("Button state:", button)
        if button == 0:
            if self.statB == 0:
                self.startB = timeB
                self.statB = 1
        elif button == 1:
            if self.startB != 0:
                dura = timeB - self.startB
            print("duration:", dura)
            self.startB = 0
            self.statB = 0
        return dura
###########################################################################################################################    
