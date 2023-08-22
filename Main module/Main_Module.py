import socket, time, sqlite3

#######################Configuration#############################

count = 25              #The amount of sensor modules

# The next variables must be a float value
valCO2 = [-1.00, 10000.00]     #min/max value CO2
valNOx = [0.00, 500.00]       #min/max value NOx
valVOC = [0.00, 500.00]       #min/max value VOC
valHUM = [0.00, 100.00]       #min/max value humidity
valTEMP = [-40.00, 125.00]    #min/max value temperature

dbfile = "/home/rock/Enviroment.db"

DEBUG = False

######################End Configuration#########################

HOST_NAME = ["131.211.88.124", "131.211.88.96"]

##name = "HPTsen"
##
##for i in range (count):
##    sen = name+str(i+1 )
##    HOST_NAME.append(sen)
##print(HOST_NAME)
    
PORT = 52171
bad_chars = ['[', ']', 'b', '"', "'"]

storedata = []
def dataComm():
    global HOST_NAME, PORT, stored, bad_chars, DEBUG
    state, dis, dele, amountT = 0, 0, 0, 1
    state = 0
    for j in range (len(HOST_NAME)):
        print("device:", j)    
        for i in range (5):
            print("Try:", i+1)
            print("trying to connect to:", HOST_NAME[j])
            
            try:
                state = 1
                dis = 0
                HOST = socket.gethostbyname(HOST_NAME[j])
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((HOST, PORT))
                    print ("connected")
                    while (True):
                        
                        if (dis == 3):
                            s.close()
                            state = 5
                            print ("Force disconnected")
                            break
                        
                        elif (state == 1):
                            print("Send request")
                            s.send(b'Request data')
                            state = 2
                        
                        elif (state == 2):
                            dataR = s.recv(1024)
                            dataChar = ''.join((filter(lambda i: i not in bad_chars, str(dataR))))
                            dataSplit = dataChar.split(": ")
                            if (DEBUG):
                                print("Received data from MM     :", dataR, type(dataR))
                                print("Characters removed        :", dataChar)
                                print("First position split data :",dataSplit[0])
                                print("Second position split data:",dataSplit[1])
                                print(" ")
                            
                            if (dataSplit [0] == "Amount"):
                                amount = int(dataSplit[1])
                                if (amount != 0):
                                    s.send(b'ACK')
                                    state = 3
                                else:
                                    s.send(b'DIS')
                                    dis = 3
                            else:
                                state = 1
                                dis += 1
                        
                        elif (state == 3):
                            dataR = s.recv(1024)
                            if dataR == b'NACK':
                                state = 2
                            else:
                                dataChar = ''.join((filter(lambda i: i not in bad_chars, str(dataR))))
                                dataSplit = dataChar.split(", ")
                                if (DEBUG):
                                    print("Received data from MM    :", dataR, type(dataR))
                                    print("Characters removed       :", dataChar)
                                    print("First position split data:",dataSplit[0])

                                if (DEBUG):
                                    print("Processing data")
                                for z in range (5):
                                    dataSplit [z+2] = float(dataSplit[z+2])
                                if (dataSplit[2] >= valTEMP[0] and dataSplit[2] <= valTEMP[1]):                #Temperature check
                                    if (dataSplit[3] >= valHUM[0] and dataSplit[3] <= valHUM[1]):              #Humidity check
                                        if (dataSplit[4] >= valVOC[0] and dataSplit[4] <= valVOC[1]):          #VOC Check
                                            if (dataSplit[5] >= valNOx[0] and dataSplit[5] <= valNOx[1]):      #NOx check
                                                if (dataSplit[6] >= valCO2[0] and dataSplit[6] <= valCO2[1]):  #CO2 check
                                                    if (DEBUG):    
                                                        print("Round: ", amountT, amount)
                                                    #storedata.append(dataSplit)
                                                    if (j == 0):
                                                        table = "HPTsen0"
                                                    elif (j == 1):
                                                        table = "HPTsen1"
                                                    elif (j == 2):
                                                        table = "HPTsen2"
                                                        
                                                    SQL(dataSplit, table)
                                                    if (amount == amountT):                              #Check of all data is collected
                                                        if (DEBUG):
                                                            print("ACK")
                                                        for z in range (len(storedata)):
                                                            print(z + 1, ":", storedata[z])
                                                        print ("Amount of datasets:", len(storedata))
                                                        s.send(b'ACK')
                                                        amountT = 1
                                                        state = 4
                                                        dis = 0
                                                    elif (amountT < amount):
                                                        if (DEBUG):
                                                            print("Next")
                                                        s.send(b'NEXT')
                                                        amountT += 1
                                                        dis = 0
                                                    else:
                                                        print("amount wrong: NACK")
                                                        s.send(b'NACK')
                                                        dele += 1
                                                else:
                                                    print("CO2 wrong: NACK")
                                                    s.send(b'NACK')
                                                    dele += 1
                                            else:
                                                print("NOx wrong: NACK")
                                                s.send(b'NACK')
                                                dele += 1
                                        else:
                                            print("VOC wrong: NACK")
                                            s.send(b'NACK')
                                            dele += 1
                                    else:
                                        print("Humidity wrong: NACK")
                                        s.send(b'NACK')
                                        dele += 1
                                else:
                                    print("Temperature wrong: NACK")
                                    s.send(b'NACK')
                                    dele += 1
                                
                                if (dele == 3):
                                    if (amount == amountT):                              #Check of all data is collected
                                        if (DEBUG):
                                            print("ACK, wrong data")
                                        if (len(storedata) != 0):
                                            for z in range (len(storedata)):
                                                print(z + 1, ":", storedata[z])
                                        print ("Amount of dataset:", len(storedata))
                                        s.send(b'ACK')
                                        amountT = 1
                                        state = 4
                                        dis = 0
                                        
                                    elif (amountT < amount):
                                        if (DEBUG):
                                            print("Next")
                                        s.send(b'NEXT')
                                        amountT += 1
                                    dele = 0
                                    
                        elif (state == 4):
                            dataR = s.recv(1024)
                            if (dataR == b'END'):
                                print("Disconnect")
                                s.send(b'END')
                                s.close()
                                state = 5
                                break
                            else:
                                s.send(b'NACK')
                                dis += 1
            except:
                print("could not connect to:", HOST_NAME[j])
                time.sleep(0.55)
                 
            if (state == 5):
    ##            print("state 5")
                break

def SQL(data, table):
    global dbfile
    
    dataStandard = "INSERT INTO " + table + "(id, time, temperature, humidity, voc, nox, co2)"
    dataMeasure = "values('" + data[0] + "', '" + data[1] + "', " + str(data[2]) + ", " + str(data[3]) + ", " + str(data[4]) + ", " + str(data[5]) + ", " + str(data[6]) + ");"
    data = dataStandard + " " + dataMeasure
    
    con = sqlite3.connect(dbfile)

    cur = con.cursor()
    
    cur.execute(data)
    con.commit()
    
##    for row in cur.execute("SELECT * FROM " + table ):
##        print (row)

    con.close()

def main():
    dataComm()
##    start = time.time()
##    while (1):
##        if (time.time() - start >= 600):
##            dataComm()
##            start = time.time()
        

if __name__ == "__main__":
    main()