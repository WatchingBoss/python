from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print "Server is ready to receive"

while 1:
    message, clientAddress = serverSocket.recvfrom(2048)
    modMessage = message.upper()
    serverSocket.sendto(modMessage, clientAddress)
