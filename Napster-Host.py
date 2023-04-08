from ftpclient.ftp_client import FtpClient
from ftpserver.ftp_server import FtpServer

HOST="127.0.0.1"
BYTEFORMAT='utf-8'

class NapsterHost:
    def __init__(self):
        self.client = FtpClient(HOST, 8080, BYTEFORMAT, BYTEFORMAT)
        self.server = FtpServer(HOST, 5665, BYTEFORMAT, BYTEFORMAT)

    def startClient(self):
        self.client.runClient()
    def startServer(self):
        self.server.runServer()


if __name__ == "__main__":
    peerHost = NapsterHost()
    clientOrServer = input("input 1 for client, anything else for server: ")
    if(clientOrServer == "1"):
        peerHost.startClient()
    else:
        peerHost.startServer()
