import socket
from binascii import hexlify

def convertIP4():
    for ip_addr in ['127.0.0.1', '192.168.0.1']:
        packed_ip = socket.inet_aton(ip_addr)
        unpacked_ip = socket.inet_ntoa(packed_ip)
        print("IP address: {}\nPacked: {}\nUnpacked: {}".format(ip_addr, packed_ip, unpacked_ip))

if __name__ == '__main__':
    convertIP4()
