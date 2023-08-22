crc = 0xFF
poly = 0x131
data = [0xbe, 0xef]
data = str(data)
print (hex(int(data)))
data = bytearray(data)
print(data)
for b in data:
    crc ^= b
    print (hex(b))
    for _ in range(8):
        if crc & 0x80:
            crc = (crc << 1) ^ poly
        else:
            crc <<= 1
crc_to_check = data[-1]
print (crc_to_check == crc)
print(hex(crc), hex(crc_to_check), crc_to_check == crc)

