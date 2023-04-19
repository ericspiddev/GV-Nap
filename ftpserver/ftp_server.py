import os
import socket
from os import listdir
from threading import Thread
from common import *

HOST="127.0.0.1"
PORT=5665
DATAPORT=6556
COMMRECVSIZE=512
FILECHUNKSIZE=4096

class FtpServer:
    def __init__(self, host, port, encoding, decoding, serverDir):
        self.host = host
        self.port = port
        self.encoding = encoding
        self.decoding = decoding
        self.serverDir = serverDir
        self.controlSock = None

    def runServer(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen()
            while True:
                self.controlSock, addr = s.accept()
                thread = Thread(target= self.server, args=(self.controlSock, ))
                thread.start()

    def server(self, controlSock):
        while True:
            print("run server!")
            command = recvStr(self.controlSock)
            if(len(command) == 0):
                print("Ending connection!")
                controlSock.close()
                exit(1)
            print("Command is {}".format(command), flush=True)
            self.executeCommand(self.getBaseCmd(command), command.split())

    def getBaseCmd(self, userCmd):
        return userCmd.split()[0]

    def executeCommand(self, basecmd, fullcmd):
        print("base command is {}, fulll cmd is {}".format(basecmd, fullcmd), flush=True)
        if basecmd.upper() == "connect".upper():
            return
        elif basecmd.upper() == "list".upper():
            self.listFiles()
        elif basecmd.upper() == "retr".upper():
            self.retr(self.serverDir + fullcmd[1])
        elif basecmd.upper() == "stor".upper():
            self.stor(self.serverDir + fullcmd[1])
        else:
            print("Unrecognized command")
    def retr(self, fileName):
        dataSock = self.dataClient()
        if not self.doesFileExist(fileName):
            print("File does not exist!")
            sendData(dataSock, "1", 1)
            dataSock.close()
            return
        sendData(dataSock, "0", 1)
        sendFile(dataSock, fileName)
        dataSock.close()

    def listFiles(self):
        dataSock = self.dataClient()
        files = listdir(self.serverDir)
        for file in files:
            if(os.path.isfile(self.serverDir + file)):
                print("sending file {}".format(file))
                sendStr(dataSock, "{}\n".format(file))
        sendStr(dataSock, "#%^ENDLIST^%#\n")
        dataSock.close()

    def stor(self, fileName):
        dataSock = self.dataClient()
        if(dataSock == None):
            print("something bad happened!")
            return
        recvFile(dataSock, fileName)
        dataSock.close()

    def doesFileExist(self, fileName):
        f = None
        try:
            f = open(fileName, "r")
        except:
            print("File with name {0} cannot be found!".format(fileName))
            return False
        f.close()
        return True

    def dataClient(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, DATAPORT))
            return s
        except:
            print("Something went wrong forming the data client")
            return None
