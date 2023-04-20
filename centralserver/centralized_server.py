
from posixpath import split
import socket as sock
from threading import Thread
from turtle import update
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
        while True:
            peerSocket, addr = s.accept()
            csThread = Thread(target=self.centralServerThread, args=(peerSocket, ))
            csThread.start()


    def centralServerThread(self, peerSocket):
        connectorsData = recvStr(peerSocket)
        self.addUser(connectorsData)
        splitData = connectorsData.split(',')
        self.addUserFiles(peerSocket, splitData[1], splitData[3])
        print("Welcome, {}".format(splitData[0]))
        while True:
            fileList = self.searchFile(peerSocket)
            if fileList != []:
                print("file list is not empty")
                if fileList[0] == "testitoutbreakstr":
                    break
            sendStr(peerSocket, str(len(fileList)) + "\n")
            for fileLine in fileList:
                sendStr(peerSocket, fileLine)
        print("leave the thread!")
        self.disconnectUser(splitData[1], splitData[3], splitData[0])
        return


    def disconnectUser(self, hostName, port, userName):
        with open(DESCRIPT_FILENAME, "r") as f:
           lines = f.readlines()
        with open(DESCRIPT_FILENAME, "w") as f:
            for line in lines:
                line = line.strip("\n")
                split = line.split(',')
                if split[2] != hostName and split[3] != port:
                    f.write(line + "\n")
        print("Goodbye {}!".format(userName))

    def searchFile(self, sock):
        searchStr = recvStr(sock)
        searchStr = searchStr.strip('\n')
        if(searchStr == "testitoutbreakstr"):
            print("leaving the search function")
            return ["testitoutbreakstr"]
        print("searchStr is {}".format(searchStr))
        f = open(DESCRIPT_FILENAME, "r")
        linesToReturn = []
        if f == None:
            print("Something went wrong opening the file!")
            exit(1)
        for line in f:
            linePieces = line.split(',')
            if searchStr in linePieces[1]:
                linesToReturn.append(line)
        f.close()
        return linesToReturn

    def addUser(self, data):
        f = open(USER_FILENAME, "a")
        f.write(data)
        f.close()

    def addUserFiles(self, cs_sock, hostName, port):
        updateFileDatabase(cs_sock, DESCRIPT_FILENAME, hostName, port)




if __name__ == "__main__":
    CS = CentralServer(HOST, PORT)
    s = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    s.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
    s.bind((CS.host, CS.port))
    s.listen()
    CS.acceptPeerConnection(s)





