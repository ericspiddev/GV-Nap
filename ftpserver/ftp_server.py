
import os
import socket
from os import listdir
from threading import Thread

HOST="127.0.0.1"
PORT=5665
DATAPORT=8080
COMMRECVSIZE=512
FILECHUNKSIZE=4096

class FtpServer:
    def __init__(self, host, port, encoding, decoding):
        self.host = host
        self.port = port
        self.encoding = encoding
        self.decoding = decoding
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
            command = controlSock.recv(COMMRECVSIZE).decode(self.decoding)
            if(len(command) == 0):
                print("Ending connection!")
                controlSock.close()
                exit(1)
            self.executeCommand(self.getBaseCmd(command), command.split())

    def getBaseCmd(self, userCmd):
        return userCmd.split()[0]

    def executeCommand(self, basecmd, fullcmd):
        if basecmd.upper() == "connect".upper():
            return
        elif basecmd.upper() == "list".upper():
            self.listFiles()
        elif basecmd.upper() == "retr".upper():
            self.retr(fullcmd[1])
        elif basecmd.upper() == "stor".upper():
            self.stor(fullcmd[1])
        else:
            print("Unrecognized command")
    def retr(self, fileName):
        dataSock = self.dataClient()
        if not self.doesFileExist(fileName):
            print("File does not exist!")
            dataSock.send("-1".encode(self.encoding))
            dataSock.close()
        dataSock.send("0".encode(self.encoding))
        f = open(fileName, "r")
        dataSock.send(f.read().encode(self.encoding))
        f.close()
        dataSock.close()

    def listFiles(self):
        dataSock = self.dataClient()
        files = listdir()
        for file in files:
            if(os.path.isfile(file)):
                dataSock.send("{}\n".format(file).encode(self.encoding))
        dataSock.close()


    def stor(self, fileName):
        dataSock = self.dataClient()
        print(dataSock)
        f = open(fileName, "w")
        while True:
            data = dataSock.recv(FILECHUNKSIZE).decode(self.decoding)
            f.write(data)
            if(len(data) != FILECHUNKSIZE):
                break
        f.close()
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
