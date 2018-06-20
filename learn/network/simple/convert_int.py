import socket

def convert(num):
    print("32-bit")
    print("Original: {}\n"
          "Long host byte order : {}\n"
          "Network byte order   : {}".format(num, socket.ntohl(num), socket.htonl(num)))
    print("16-bit")
    print("Original: {}\n"
          "Short host byte order: {}\n"
          "Network byte order   : {}".format(num, socket.ntohs(num), socket.htons(num)))

if __name__ == '__main__':
    num = int(input("Enter integer number: "))
    convert(num)
