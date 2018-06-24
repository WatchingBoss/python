import socket

def socket_modes():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setblocking(1)
    s.settimeout(0.5)
    s.bind(("127.0.0.1", 0))

    socket_addr = s.getsockname()
    print("Server launched on socket: {}".format(str(socket_addr)))
    while(True):
        s.listen(1)

if __name__ == '__main__':
    socket_modes()
