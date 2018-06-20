from socket import *
import subprocess

serverName = subprocess.check_output("hostname -I", shell=True) # if server is on the same machine
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

message = raw_input('Enter your lowercase string: ')

clientSocket.send(message)

modMes = clientSocket.recv(1024)

print 'From Server: ', modMes

clientSocket.close()
