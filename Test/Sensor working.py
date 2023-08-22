import machine
import time

i2c = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2), freq = 200000)

reqData = 0x2032
reqStatus = 0xF32D
softReset = 0x30A2
breakCom = 0x3093

sensorAdress = 0x44
data = bytearray(6)
temp = 0
humi = 0
square = (2 ** 16) - 1

try:
    print ("Send command")
    i2c.writeto_mem(sensorAdress, reqData , b'', addrsize = 8)
except:
    print("Failed to send")

time.sleep_ms(10)
print ("Receive command")
data = i2c.readfrom_mem(0x44, reqData, 6, addrsize = 8)
rawTemp = (data[0] << 8) + data[1]
rawHumi = (data[3] << 8) + data[4]
temp = -45 + 175 * (rawTemp/square)
RH = 100 * (rawHumi / square)
print("Data T1:", data[0], "Data T2", data[1])
print("Data H1:", data[3], "Data H2", data[4])
print("Data CRC-T:", data[2], "Data CRC-H", data[5])
print("temperature:",temp, "C")
print("Humidity:", RH, "%RH")

