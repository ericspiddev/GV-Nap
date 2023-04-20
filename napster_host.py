from ftpclient.ftp_client import FtpClient
from ftpserver.ftp_server import FtpServer
from common import *
import socket as sock

from threading import Thread

HOST="127.0.0.1"
BYTEFORMAT='utf-8'

CENTRALHOST="127.0.0.1"
CENTRALPORT=8080
HOSTSERVERPORT = 5665
descriptorFile = "ftpserver/fileDescriptors.txt"

class NapsterHost:
    def __init__(self):
        self.client = FtpClient(HOST, 6556, BYTEFORMAT, BYTEFORMAT, "ftpclient/")
        self.server = FtpServer(HOST, 5665, BYTEFORMAT, BYTEFORMAT, "ftpserver/")

    def runFtpClientCmd(self, cmd):
            return self.client.runClientCmd(cmd)
    def startServer(self):
        self.server.runServer()

    def connectToCentralServer(self, csHostName, userName, userHostName, connSpeed, csPort, userPort):
        self.centralServerSocket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.centralServerSocket.connect((csHostName, int(csPort)))
        self.sendHostInfo(self.centralServerSocket, userName, userHostName, connSpeed, userPort)
        self.sendFileInfo(self.centralServerSocket, descriptorFile)

    def sendHostInfo(self, cs_sock, userName, hostName, connSpeed, port):
        hostInfo = "{0},{1},{2},{3}\n".format(userName, hostName, connSpeed, port)
        sendStr(cs_sock, hostInfo)

    def sendFileInfo(self, cs_sock, fileName):
        sendFileLines(cs_sock, fileName)



if __name__ == "__main__":
    peerHost = NapsterHost()
