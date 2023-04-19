import socket as sock
from common import *

supportedCmds = ["STOR", "CONNECT", "LIST", "RETR", "QUIT"]

FILECHUNKSIZE=4096

class FtpClient:
    def __init__(self, datahost, dataport, encoding, decoding, clientDir):
        self.datahost = datahost
        self.dataport = dataport
        self.encoding = encoding
        self.decoding = decoding
        self.clientDir = clientDir
        self.output =  ""
        self.commSocket = None
        self.isConnected = False

    def runClientCmd(self, userCmd):
        self.output = ""

        separatedCmd = self.parseCmd(userCmd)
        if separatedCmd == None:
            self.output += "Bad command please enter a valid FTP command"
            return self.output
        baseCmd = separatedCmd[0]
        if not self.verifyCommandArgs(baseCmd, separatedCmd):
            self.output +=("Poorly formatted command please ensure you provide the appropriate number of arguments")
            return self.output

        if baseCmd.upper() == "connect".upper():
            self.commSocket = self.connect(separatedCmd[1], separatedCmd[2])
            if(self.commSocket == None):
                self.output += "Connection failed! Please try again"
                return self.output
            sendStr(self.commSocket, userCmd)
            # self.commSocket.send(bytes(userCmd, self.encoding))
            self.output += "Successful connection formed"
            self.isConnected = True

        elif baseCmd.upper() ==  "quit".upper():
            self.output += "Leaving FTP client"
            if self.commSocket != None:
                self.commSocket.close()
            exit(0)

        elif self.isConnected == False:
            self.output += "A connection must be formed before using the LIST, STOR, or RETR commands!"
            return

        elif baseCmd.upper() == "list".upper():
            sendStr(self.commSocket, userCmd)
            self.listFiles()

        elif baseCmd.upper() ==  "stor".upper():
            storFile = self.clientDir + separatedCmd[1]
            if not self.doesFileExist(storFile):
                self.output += "Stor file does not exist!"
                return self.output
            sendStr(self.commSocket, userCmd)
            self.stor(storFile)

        elif baseCmd.upper() == "retr".upper():
            retrFile = self.clientDir + separatedCmd[1]
            sendStr(self.commSocket, userCmd)
            self.retr(retrFile)
        else:
                self.output += "Something went really wrong!"
        return self.output

    def verifyCommandArgs(self, baseCmd, fullCmd):
        if baseCmd.upper() ==  "connect".upper():
            return len(fullCmd) == 3
        elif baseCmd.upper() ==  "stor".upper() or baseCmd.upper() ==  "retr".upper() :
            return len(fullCmd) == 2
        elif baseCmd.upper() == "list".upper():
            return len(fullCmd) == 1
        else:
            return True

    def connect(self, ip, port):
        try:
            int(port)
        except:
            print("Port cannot be converted to an integer please provide a valid port number")
            return None

        try:
            s = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
            s.connect((ip, int(port)))
            return s
        except:
            print("Error connecting to ftp server something went wrong!")
            return None

    def listFiles(self):
        dataSocket = self.dataServer(self.datahost, self.dataport)
        while True:
            data = recvStr(dataSocket)
            if"#%^ENDLIST^%#" in data:
                break
            self.output += data
        dataSocket.close()

    def stor(self, fileName):
        dataSocket = self.dataServer(self.datahost, self.dataport)
        sendFile(dataSocket, fileName)
        dataSocket.close()
        self.output += "Successfully sent file {}".format(fileName)

    def retr(self, fileName):
        dataSocket = self.dataServer(self.datahost, self.dataport)
        if not self.fileFoundOnServer(dataSocket):
            self.output += "Requested file {} not found on the server".format(fileName)
            dataSocket.close()
            return
        recvFile(dataSocket, fileName)
        dataSocket.close()
        self.output += "Successfully retrieved file {}".format(fileName)


    def dataServer(self, ip, port):
        try:
            s = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
            s.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
            s.bind((ip, port))
            s.listen()
            conn, addr = s.accept()
            return conn
        except:
            print("Something went wrong with forming the data connection")
            return None


    def fileFoundOnServer(self, dataSocket):
        isFound = dataSocket.recv(1).decode(self.decoding)
        return isFound == "0"

    def isValidCommand(self, userCmd):
        if userCmd.upper() in supportedCmds:
            return True
        else:
            return False

    def parseCmd(self,userCmd):
        separatedCmd = userCmd.split()
        if separatedCmd == None or  (not self.isValidCommand(separatedCmd[0])):
            return None
        else:
            return separatedCmd

    def doesFileExist(self, fileName):
        f = None
        try:
            f = open(fileName, "r")
        except:
            print("File with name {0} cannot be found!".format(fileName))
            return False
        f.close()
        return True