from socket import *
import subprocess

#serverName = '' # check current: hostname -I
serverName = subprocess.check_output("hostname -I", shell=True) # if server is on the same machine
print serverName
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = raw_input('Enter lowercase string: ')
clientSocket.sendto(message, (serverName, serverPort))
modMessage, serverAddress = clientSocket.recvfrom(2048)
print modMessage
clientSocket.close()
