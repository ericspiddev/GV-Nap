import os
FILECHUNKSIZE=4096


def recvStr(s):
    recvStr = ""
    while('\n' not in recvStr):
        recvStr += s.recv(1).decode('utf-8')
    return recvStr

def recvFile(s, fileName):
    f = open(fileName, "w")
    while True:
        data = s.recv(FILECHUNKSIZE).decode('utf-8')
        f.write(data)
        if(len(data) != FILECHUNKSIZE):
            break
    f.close()

def updateFileDatabase(s, fileName, hostName, port):
    f = open(fileName, "a")
    data = ""
    while True:
        data = recvStr(s)
        print("Data is  {}".format(data))
        if(data == "#$%^&ENDOFFILELINE#$%^&\n"):
            print("leaving update")
            break
        data = data.rstrip('\n')
        f.write("{},{},{}".format(data, hostName, port))
    f.close()

def sendFileLines(s, fileName):
    f = open(fileName, "r")
    line = "noteof"
    while(line):
            line = f.readline()
            print("line is {}".format(line))
            sendStr(s, line)
    print("Send kill string")
    sendStr(s, "#$%^&ENDOFFILELINE#$%^&\n")

def sendData(s, data, dataSize):
    sentData = 0
    while(sentData != dataSize):
        sentData += s.send(bytes(data, 'utf-8'))

def sendStr(s, string):
    strLen = len(string)
    sendData(s, string, int(strLen))

def sendFile(s, fileName):
    size = os.path.getsize(fileName)
    f = open(fileName, "r")
    dataSent = 0
    while(dataSent != size):
        dataSent += s.send(f.read().encode('utf-8'))
    f.close()
