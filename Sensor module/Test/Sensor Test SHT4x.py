from HPT import HPT as hpt
import machine, time

i2c = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2), freq = 200000)

reqDataH = 0xFD
reqDataM = 0xF6
reqDataL = 0xE0
fetchData = 0x89
heater = 0x39

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


i2c.writeto_mem(sensorAdress, reqDataH , b'', addrsize = 8)
time.sleep_ms(10)
data = i2c.readfrom(0x44, 6)
rawTemp = (data[0] << 8) + data[1]
rawHumi = (data[3] << 8) + data[4]
temp = -45 + 175 * (rawTemp/square)
RH = 100 * (rawHumi / square)
print("temperature:",temp, "C")
print("Humidity:", RH, "%RH")

