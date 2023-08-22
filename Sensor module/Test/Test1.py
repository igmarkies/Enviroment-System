from HPT import HPT as hpt
import machine, time, struct, math

i2c = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2), freq = 200000)

i2c.writeto_mem(0x62, 0x3f86, b'', addrsize = 16)
time.sleep(1)

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

bint = struct.pack(">H", 1)
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
i2c.writeto_mem(0x62, 0x2416, dataCO2, addrsize = 16)
time.sleep_ms(10)
i2c.writeto_mem(0x62, 0x2313, b'', addrsize = 16)
time.sleep(1)
dataSCD = i2c.readfrom(0x62, 24)
cal = (dataSCD[0] << 8) | dataSCD[1]
print(cal)