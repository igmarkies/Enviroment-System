from HPT import HPT as hpt
import machine, time, struct, math

i2c = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2), freq = 100000)
data = [] * 6
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

try:
    print ("Send command")
    i2c.writeto_mem(sensorAdress, reqDataH , b'', addrsize = 8)
    #i2c.writeto(sensorAdress, reqDataH)
except:
    print("Failed to send")

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

try:
    time.sleep_ms(10)
    print ("Receive command")
    data = i2c.readfrom(0x44, 6)
    rawTemp = (data[0] << 8) + data[1]
    rawHumi = (data[3] << 8) + data[4]
    temp = -45 + 175 * (rawTemp/square)
    RH = 100 * (rawHumi / square)
    print("Data T1:", hex(data[0]), "Data T2", hex(data[1]))
    print("Data H1:", hex(data[3]), "Data H2", hex(data[4]))
    print("Data CRC-T:", hex(data[2]), "Data CRC-H", hex(data[5]))
    print("temperature:",temp, "C")
    print("Humidity:", RH, "%RH")
except:
    print("Failed to receive")
    
# make table with CRC variables


humidity = RH
temperature = temp

# package data calculating for the SGP41
paramh = struct.pack(">H", math.ceil(humidity * 0xffff / 100))
msb = paramh[0]
lsb = paramh[1]
crc = 0xff
crc ^= msb
crc = CRC_TABLE[crc]
if lsb is not None:
    crc ^= lsb
    crc = CRC_TABLE[crc]
crch = crc

paramt = struct.pack(">H", math.ceil((temperature + 45) * 0xffff / 175))
msb = paramt[0]
lsb = paramt[1]
crc = 0xff
crc ^= msb
crc = CRC_TABLE[crc]
if lsb is not None:
    crc ^= lsb
    crc = CRC_TABLE[crc]
crct = crc
data = paramh + bytes([crch]) + paramt + bytes([crct])
print (data)

# communication SGP41
# i2c.writeto_mem(0x59, 0x2619 , data, addrsize = 16)
# time.sleep_ms(500) #delay time much not go under the 50ms
# dataSGP = i2c.readfrom(0x59, 6)
# for d in range (6):
#     print ("SGP41:", hex(dataSGP[d]))
# print("")

# Data calculation SCD41    
while 1:
    i2c.writeto_mem(0x62, 0xe4b8 , b'', addrsize = 16)
    time.sleep_ms(1)
    dataSCD = i2c.readfrom(0x62, 3)
    ready = not((dataSCD[0] & 0x07 == 0) and dataSCD == 0)
    print(ready)
    if ready:
        i2c.writeto_mem(0x62, 0xec05 , b'', addrsize = 16)
        time.sleep_ms(500)
        dataSCD = i2c.readfrom(0x62, 18)
        co2 = (dataSCD[0] << 8) | dataSCD[1]
        temp = (dataSCD[3] << 8) | dataSCD[4]
        rh = (dataSCD[6] << 8) | dataSCD[7]
        temp = -45 + 175 * (temp / (2**16))
        rh = 100 * (rh/(2**16))
        for d in range (9):
            print ("SCD41:", dataSCD[d], " ", hex(dataSCD[d]))
        
        i2c.writeto_mem(sensorAdress, reqDataH , b'', addrsize = 8)
        time.sleep_ms(10)
        print ("Receive command")
        data = i2c.readfrom(0x44, 6)
        rawTemp = (data[0] << 8) + data[1]
        rawHumi = (data[3] << 8) + data[4]
        Temp = -45 + 175 * (rawTemp/square)
        RH = 100 * (rawHumi / square)
        print("Data T1:", hex(data[0]), "Data T2", hex(data[1]))
        print("Data H1:", hex(data[3]), "Data H2", hex(data[4]))
        print("Data CRC-T:", hex(data[2]), "Data CRC-H", hex(data[5]))
        print("temperature:",temp, "C")
        print("Humidity:", RH, "%RH")
        
        print ("co2:", co2, "temp:", Temp, "RH:", RH)
    time.sleep(5)
