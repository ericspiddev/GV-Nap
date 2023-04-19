from ftpclient.ftp_client import FtpClient
from ftpserver.ftp_server import FtpServer
from common import *
import socket as sock

from threading import Thread

HOST="127.0.0.1"
BYTEFORMAT='utf-8'

CENTRALHOST="127.0.0.1"
CENTRALPORT=8080

descriptorFile = "ftpserver/fileDescriptors.txt"

class NapsterHost:
    def __init__(self):
        self.client = FtpClient(HOST, 6556, BYTEFORMAT, BYTEFORMAT, "ftpclient/")
        self.server = FtpServer(HOST, 5665, BYTEFORMAT, BYTEFORMAT, "ftpserver/")

    def runFtpClientCmd(self, cmd):
            return self.client.runClientCmd(cmd)
    def startServer(self):
        self.server.runServer()

    def connectToCentralServer(self, csHostName, userName, userHostName, connSpeed, port ):
        self.centralServerSocket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.centralServerSocket.connect((csHostName, int(port)))
        self.sendHostInfo(self.centralServerSocket, userName, userHostName, connSpeed)
        self.sendFileInfo(self.centralServerSocket, descriptorFile)

    def sendHostInfo(self, cs_sock, userName, hostName, connSpeed):
        hostInfo = "{0},{1},{2}\n".format(userName, hostName, connSpeed)
        sendStr(cs_sock, hostInfo)

    def sendFileInfo(self, cs_sock, fileName):
        sendFile(cs_sock, fileName)



if __name__ == "__main__":
    peerHost = NapsterHost()

    # clientThread = Thread(target=peerHost.startClient)
    # serverThread = Thread(target=peerHost.startServer)

    # clientThread.start()
    # serverThread.start()
    # clientOrServer = input("input 1 for client, anything else for server: ")
    # if(clientOrServer == "1"):
    #     while(1):
    #         usercmd = input(">")
    #         peerHost.runFtpClientCmd(usercmd)
    # else:
    #     peerHost.startServer()
