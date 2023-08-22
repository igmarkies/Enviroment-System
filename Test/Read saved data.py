rawData = open('Data test.csv','r').read()
lines = rawData.split('\n')
lines = [ele for ele in lines if ele != ""]
#print (lines)
# for line in lines:
#     print ("line", line)
#     data = line.split(', ')
#     for dat in data:
#         pack = dat.split(',')
#         print ("float data:", float(pack[3]))
#byte = line.split(',')
        
data = lines[-1].split(', ')
for dat in data:
    pack = dat.split(',')
print ("name	   :", str(pack[0]))
print ("time	   :", int(pack[1]))
print ("temperature:", float(pack[2]), "'C")
print ("Humidity   :", float(pack[3]), "%RH")
