import sys
import socket
import argparse

def erEx(mes, e):
    print("{}: {}".format(mes, e))
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Socket errors')
    parser.add_argument('--host', action="store", dest="host", required=False)
    parser.add_argument('--port', action="store", dest="port", type=int, required=False)
    parser.add_argument('--file', action="store", dest="file", required=False)
    given_args = parser.parse_args()
    host = given_args.host
    port = given_args.port
    fileName = given_args.file

    # Create socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        erEx("Error creating socket", e)

    # Connect to given host/port
    try:
        s.connect((host, port))
    except socket.gaierror as e:
        erEx("Address-related error connetiing to server", e)
    except socket.error as e:
        erEx("Connection error", e)

    # Sending data
    try:
        msg = "GET %s HTTP/1.0\r\n\r\n" % fileName
        s.sendall(msg.encode('utf-8'))
    except socket.error as e:
        erEx("Error sending data", e)

    # Waiting to receive data from remote host
    while True:
        try:
            buf = s.recv(2048)
        except socket.error as e:
            erEx("Error receiving data", e)
        if not len(buf):
            break
        sys.stdout.write(buf.decode('utf-8'))

if __name__ == '__main__':
    main()





