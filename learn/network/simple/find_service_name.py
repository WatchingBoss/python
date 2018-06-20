import socket

def find():
    proto = ['tcp', 'udp']
    ports = [80, 25, 53]

    for port in ports[:2]:
        print("Port: {}\nService name: {}".format(port, socket.getservbyport(port, proto[0])))
    
    print("Port: {}\nService name: {}".format(ports[2], socket.getservbyport(ports[2], proto[1])))
        
if __name__ == '__main__':
    find()
