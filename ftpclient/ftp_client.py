import socket as sock


supportedCmds = ["STOR", "CONNECT", "LIST", "RETR", "QUIT"]
isConnected = False
ENCODING = 'utf-8'

DATAHOST="127.0.0.1"
DATAPORT=8080

FILECHUNKSIZE=4096
DECODING='utf-8'

def main():
    print("Welcome to FTP Client!")
    commSocket = None
    while True:
        userCmd = input(">")
        separatedCmd = parseCmd(userCmd)
        if separatedCmd == None:
            print("Bad command please enter a valid FTP command")
        baseCmd = separatedCmd[0]

        if not verifyCommandArgs(baseCmd, separatedCmd):
            print("Poorly formatted command please ensure you provide the appropriate number of arguments")
            continue

        if baseCmd.upper() == "connect".upper():
            commSocket = connect(separatedCmd[1], separatedCmd[2])
            if(commSocket == None):
                print("Connection failed! Please try again")
                continue
            commSocket.send(bytes(userCmd, ENCODING))
            print("Successful connection formed")
            isConnected = True

        elif baseCmd.upper() ==  "quit".upper():
            print("Leaving FTP client")
            exit(0)

        elif isConnected == False:
            print("A connection must be formed before using the LIST, STOR, or RETR commands!")
            continue

        elif baseCmd.upper() == "list".upper():
            commSocket.send(bytes(userCmd, ENCODING))
            listFiles()

        elif baseCmd.upper() ==  "stor".upper():
            if not doesFileExist(separatedCmd[1]):
                print("Stor file does not exist!")
                continue
            commSocket.send(bytes(userCmd, ENCODING))
            stor(separatedCmd[1])

        elif baseCmd.upper() == "retr".upper():
            commSocket.send(bytes(userCmd, ENCODING))
            retr(separatedCmd[1])

        else:
            print("Something went really wrong!")


def verifyCommandArgs(baseCmd, fullCmd):
    if baseCmd.upper() ==  "connect".upper():
        return len(fullCmd) == 3
    elif baseCmd.upper() ==  "stor".upper() or baseCmd.upper() ==  "retr".upper() :
        return len(fullCmd) == 2
    elif baseCmd.upper() == "list".upper():
        return len(fullCmd) == 1
    else:
        return True

def connect(ip, port):
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

def listFiles():
    dataSocket = dataServer(DATAHOST, DATAPORT)
    while True:
        data = dataSocket.recv(256)
        if len(data) == 0:
            break
        print(data.decode(DECODING), end="")
    dataSocket.close()

def stor(fileName):
    dataSocket = dataServer(DATAHOST, DATAPORT)
    print("data socket is {}".format(dataSocket))
    f = open(fileName, "r")
    dataSocket.send(f.read().encode(ENCODING))
    f.close()
    dataSocket.close()

def retr(fileName):
    print("inside retr call with filename {0}".format(fileName))
    dataSocket = dataServer(DATAHOST,  DATAPORT)
    if not fileFoundOnServer(dataSocket):
        print("Requestd file {} not found on the server".format(fileName))
        dataSocket.close()
        return
    f = open(fileName, "w")
    while True:
        data = dataSocket.recv(FILECHUNKSIZE).decode(DECODING)
        f.write(data)
        if(len(data) != FILECHUNKSIZE):
            break
    f.close()
    dataSocket.close()


def dataServer(ip, port):
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


def fileFoundOnServer(dataSocket):
    isFound = dataSocket.recv(8).decode(DECODING)
    return isFound == "0"

def isValidCommand(userCmd):
    if userCmd.upper() in supportedCmds:
        return True
    else:
        return False

def parseCmd(userCmd):
    separatedCmd = userCmd.split()
    if isValidCommand(separatedCmd[0]):
        return separatedCmd
    else:
        return None

def doesFileExist(fileName):
    f = None
    try:
        f = open(fileName, "r")
    except:
        print("File with name {0} cannot be found!".format(fileName))
        return False
    f.close()
    return True



if __name__ == "__main__":
    main()