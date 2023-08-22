import time
data = [0x0001, 0x0002, 0x0003, 0x0004,
        0x0005, 0x0006, 0x0007, 0x0008,
        0x0009]

value = data[0:]
value = [value[0], value[1], value[2]]
print(value)
value = data[3:]
value = [value[0], value[1], value[2]]
print(value)
value = data[6:]
value = [value[0], value[1], value[2]]
time.sleep_ms(10000)
print(value)
