
import socket as sock
from threading import Thread
from common import *
HOST = "127.0.0.1"
PORT = 8080

USER_FILENAME="users.txt"
DESCRIPT_FILENAME="files.txt"

class CentralServer:
    def __init__(self, host, port):
        print("Intialized central server with host {} and port {}".format(host, port))
        self.host = host
        self.port = port

    def acceptPeerConnection(self, s):
        print("Inside accept peer connection")
        self.peerSocket, addr = s.accept()
        connectorsData = recvStr(self.peerSocket)
        self.addUser(connectorsData)
        self.addUserFiles(self.peerSocket)
        print("Connectors data is {}".format(connectorsData))
        splitData = connectorsData.split(',')
        print("Welcome, {}".format(splitData[0]))


    def searchFile(self, searchStr):
        pass

    def addUser(self, data):
        print("inside add user")
        print("write data {} to file ".format(data))
        f = open(USER_FILENAME, "a")
        f.write(data)
        f.close()

    def addUserFiles(self, cs_sock):
        appendFile(cs_sock, DESCRIPT_FILENAME)




if __name__ == "__main__":
    CS = CentralServer(HOST, PORT)
    s = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    s.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
    s.bind((CS.host, CS.port))
    s.listen()
    CS.acceptPeerConnection(s)





