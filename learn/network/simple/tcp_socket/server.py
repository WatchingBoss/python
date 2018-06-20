from socket import *

serverPost = 12000

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPost))
serverSocket.listen(1)

print 'The server is ready'

while 1:
    connection, address = serverSocket.accept()
    message = connection.recv(1024)
    modMes = message.upper()
    connection.send(modMes)
    connection.close()
