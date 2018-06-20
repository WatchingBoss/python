import socket

def printInfo():
    hostName = socket.gethostname()
    ipAddr = socket.gethostbyname(hostName)
    print("Host name: {}\nIP address: {}".format(hostName, ipAddr))

if __name__ == '__main__':
    printInfo()
