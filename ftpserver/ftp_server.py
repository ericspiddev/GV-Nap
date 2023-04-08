
import os
import socket
from os import listdir
from threading import Thread

HOST="127.0.0.1"
PORT=5665
DATAPORT=8080
DECODING='utf-8'
ENCODING='utf-8'
COMMRECVSIZE=512
FILECHUNKSIZE=4096

def getBaseCmd(userCmd):
    return userCmd.split()[0]

def executeCommand(basecmd, fullcmd):
    if(basecmd.upper() == "connect".upper()):
        return
    elif(basecmd.upper() == "list".upper()):
        listFiles()
    elif(basecmd.upper() == "retr".upper()):
        retr(fullcmd[1])
    elif(basecmd.upper() == "stor".upper()):
        stor(fullcmd[1])
    else:
        print("Unrecognized command")


def retr(fileName):
    dataSock = dataClient()
    if not doesFileExist(fileName):
        print("File does not exist!")
        dataSock.send("-1".encode(ENCODING))
        dataSock.close()
    dataSock.send("0".encode(ENCODING))
    f = open(fileName, "r")
    dataSock.send(f.read().encode(ENCODING))
    f.close()
    dataSock.close()

def listFiles():
    dataSock = dataClient()
    files = listdir()
    for file in files:
        if(os.path.isfile(file)):
            dataSock.send("{}\n".format(file).encode(ENCODING))
    dataSock.close()


def stor(fileName):
    dataSock = dataClient()
    print(dataSock)
    f = open(fileName, "w")
    while True:
        data = dataSock.recv(FILECHUNKSIZE).decode(DECODING)
        f.write(data)
        if(len(data) != FILECHUNKSIZE):
            break
    f.close()
    dataSock.close()

def doesFileExist(fileName):
    f = None
    try:
        f = open(fileName, "r")
    except:
        print("File with name {0} cannot be found!".format(fileName))
        return False
    f.close()
    return True


def dataClient():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, DATAPORT))
        return s
    except:
        print("Something went wrong forming the data client")
        return None

def server(controlSock):
    while True:
        command = controlSock.recv(COMMRECVSIZE).decode(DECODING)
        if(len(command) == 0):
            print("Ending connection!")
            exit(1)
        executeCommand(getBaseCmd(command), command.split())

def welcomeFunc():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        while True:
            controlSock, addr = s.accept()
            thread = Thread(target= server, args=(controlSock, ))
            thread.start()
        # while True:
        #     command = controlSock.recv(COMMRECVSIZE).decode(DECODING)
        #     if(len(command) == 0):
        #         print("Ending connection!")
        #         exit(1)
        #     executeCommand(getBaseCmd(command), command.split())


if __name__  == "__main__":
    welcomeFunc()