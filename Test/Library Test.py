from HPT import HPT
import time

hpt = HPT()

#############################SHT-85 sensor commands
singleShot = 0x2400
reqDataH = 0x2236
reqDataM = 0x2130
reqDataS = 0x2236
ART = 0x2b32
reqStatus = 0xF32D
softReset = 0x30A2
breakCom = 0x3093
readSerial = 0x3780

#############################Variable declaration
temp = 0
humi = 0
count = 59
# 
# for c in range (20):
#     temp, humi = hpt.sensorData(reqDataH)
#     print (c, ":", temp, humi)
#     while 1:
#         if hpt.delay(1):
#             break
# print ("done")

file=open("Data test.csv","w")	# file is created and opened in write mode

while 1:
    if hpt.delay(1):
        count += 1
        print (count)
    if count == 60:
        tim = time.time()
        temp, humi = hpt.sensorData(reqDataH)
        file.write("Sensor 1" + ","+ str(tim) + "," +str(temp) + "," + str(humi) + "\n")
        file.flush()
        print("Data saved")
        count = 0
        
