import machine
import time

i2c = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2), freq = 200000)

singleShot = 0x2400
reqDataH = 0x2236
reqDataM = 0x2130
reqDatas = 0x2236
fetchData = 0xe000
ART = 0x2b32
reqStatus = 0xF32D
softReset = 0x30A2
breakCom = 0x3093
readSerial = 0x3780

sensorAdress = 0x44
data = bytearray(6)
square = (2 ** 16) - 1

print('Scan i2c bus...')
devices = i2c.scan()

if len(devices) == 0:
  print("No i2c device !")
else:
  print('i2c devices found:',len(devices))

  for device in devices:  
    print("Decimal address: ",device," | Hexa address: ",hex(device))

try:
    print ("Send command")
    #i2c.writeto_mem(0x00, 0x06 , b'', addrsize = 8)
    i2c.writeto_mem(sensorAdress, reqDataH , b'', addrsize = 16)
except:
    print("Failed to send")

# try:
time.sleep_ms(10)
print ("Receive command")
data = i2c.readfrom_mem(0x44, fetchData, 6, addrsize = 16)
rawTemp = (data[0] << 8) + data[1]
rawHumi = (data[3] << 8) + data[4]
temp = -45 + 175 * (rawTemp/square)
RH = 100 * (rawHumi / square)
print("Data T1:", hex(data[0]), "Data T2", hex(data[1]))
print("Data H1:", hex(data[3]), "Data H2", hex(data[4]))
print("Data CRC-T:", hex(data[2]), "Data CRC-H", hex(data[5]))
print("temperature:",temp, "C")
print("Humidity:", RH, "%RH")
# except:
#     print("Failed to receive")
