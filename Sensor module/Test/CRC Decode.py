from HPT import HPT
import time, utime

hpt = HPT()
bad_chars = ['[', ']', "'", '"', ",", ' ']
name = 0X01
crc = 0
Temp, Humi = hpt.sensorData(0x2236, False)
cTime = time.time()
#print("Data:", Temp, type(Temp), Humi, type(Humi))
for i in range (3):
    tCRC = hpt.calCRC(Temp, True)
    hCRC = hpt.calCRC(Humi, True)
    if (tCRC == 0 and hCRC == 0):
        print ("Try:", i+1)
        print ("Temp CRC:", tCRC, "humi CRC:", hCRC)
        break
    else:
        print("CRC is not correct. Try", i+1, "/ 3")

print(hpt.calculateData(Temp, Humi))
arr = [name, cTime, Temp[0], Temp[1], Humi[0], Humi[1]]
arrStr = str(arr)
arrByte = bytearray(arr)
crc = hpt.calCRC(bytearray(arr), True)
print("CRC 1:",crc)

arr = [name, cTime, Temp[0], Temp[1], Humi[0], Humi[1], crc]

crc = hpt.calCRC(bytearray(arr), True)
print("CRC 2:",crc)
print(arr)