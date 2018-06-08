import socket

HOST, PORT = '', 12000

lSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lSocket.bind((HOST, PORT))
lSocket.listen(2)

print ("Serving HTTP on port %s" % PORT)

while True:
    clientConnection, clientAddress = lSocket.accept()
    request = clientConnection.recv(1024)
    print (request)

    httpResponse = """\
HTTP/1.1 200 OK 

Everything works quite good:))"""

    clientConnection.sendall(httpResponse.encode())
    clientConnection.close()
