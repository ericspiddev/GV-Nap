
import socket as sock

HOST = "127.0.0.1"
PORT = 8080

class CentralServer:
    def __init__(self, host, port):
        print("Intialized central server")
        self.host = host
        self.port = port

    def acceptPeerConnection(self,):
        print("Inside accept peer connection")
        s = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        s.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen()
        peerSocket, addr = s.accept()



with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn :
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
