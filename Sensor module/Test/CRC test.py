data = [0x92]
crc = 0xFF
poly = 0x31

for b in data[:-1]:
    crc ^= b
    for _ in range(8, 0, -1):
        if crc & 0x80:
            crc = (crc << 1) ^ poly
        else:
            crc <<= 1
crc_to_check = data[-1]
print(data[-1], crc, crc_to_check == crc)
