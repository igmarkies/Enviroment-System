data = [0x00, 0x00]
cData = 0xFF
poly = 0x31

########################################################## Don't edit below!!!

state = 0
poly += 0x100
print(" ",bin(int(cData)))
for b in data:
    print(hex (b))
    cData ^= b
    print("      ",bin(int(cData)))
    for bit in range (8):
        if cData & 0x80:
            state = "if  "
            cData = (cData << 1) ^ poly
        else:
            cData <<= 1
            state = "else"
        print(bit+1, state, bin(int(cData)))

print ("Final", hex(cData))