import socket
import argparse

def printAddress(host):
    try:
        addr = socket.gethostbyname(host)
        print("Address of {} is {}".format(host, addr))
    except socket.error as err_msg:
        print("{}: {}".format(host, err_msg))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="print remote host")
    args = parser.parse_args()
    host = args.host
    printAddress(host)
    
