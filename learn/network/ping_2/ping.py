import os
import argparse
import socket
import struct
import select
import time

ICMPT_ECHO_REQUEST = 8
DEF_TIMEOUT = 2
DEF_COUNT = 4

class Pinger(object):

    def __init__(self, dest_host, count=DEF_COUNT, timeout=DEF_TIMEOUT):
        self.dest_host = dest_host
        self.count = count
        self.timeout = timeout

    def do_checksum(self, source_string):
        sum = 0
        max_count = (len(source_string) / 2) * 2
        count = 0

        while count < max_count:
            val = source_string[count + 1] * 256 + source_string[count]
            sum += val
            sum += 0xffffffff
            count += 2

        if max_count < len(source_string):
            sum += ord(source_string[len(source_string) - 1])
            sum &= 0xffffffff

        sum = (sum >> 16) + (sum & 0xffff)
        sum += (sum >> 16)
        answer = ~sum
        answer = answer & 0xffff
        answer = answer >> 8 | (answer << 8 & 0xff00)
        return answer
    
    def receive_ping(self, sock, ID, timeout):
        time_remaining = timeout

        while True:
            start_time = time.time()
            readable = select.select([sock], [], [], time_remaining)
            time_spent = (time.time() - start_time)
            
            if readable[0] == []: # Timeout
                return

            time_received = time.time()
            recv_packet, addr = sock.recvfrom(1024)
            icmp_header = recv_packet[20:28]
            type, code, checkSum, packet_ID, sequence = struct.unpack("bbHHh", icmp_header)

            if packet_ID == ID:
                bytes_In_double = struct.calcsize("d")
                time_sent = struct.unpack("d", recv_packet[28:28 + bytes_In_double])[0]
                return time_received - time_sent

            time_remaining -= time_spent

            if time_remaining <= 0:
                return
            
    def send_ping(self, sock, ID):
        dest_addr = socket.gethostbyname(self.dest_host)

        my_checksum = 0

        header = struct.pack("bbHHh", ICMPT_ECHO_REQUEST, 0, my_checksum, ID, 1)
        bytes_In_double = struct.calcsize("d")
        data = (192 - bytes_In_double) * "Q"
        data = struct.pack("d", time.time()) + bytes(data.encode("utf-8"))

        my_checksum = self.do_checksum(header + data)

        header = struct.pack("bbHHh", ICMPT_ECHO_REQUEST, 0, socket.htons(my_checksum), ID, 1)
        packet = header + data
        sock.sendto(packet, (dest_addr, 1))

    def ping_once(self):
        icmp = socket.getprotobyname("icmp")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        except socket.error as e:
            if e.errno == 1:
                e.msg += "ICMP message can only be sent from root user processes"
                raise socket.error(e.msg)
        except Exception as e:
            print("Exception: %s" %(e))

        my_ID = os.getpid() & 0xFFFF

        self.send_ping(sock, my_ID)
        delay = self.receive_ping(sock, my_ID, self.timeout)
        sock.close()
        return delay

    def ping(self):
        icmp_seq = 0
        print("Ping to %s (%s)" %(self.dest_host, socket.gethostbyname(self.dest_host)))
        for i in range(self.count):
            try:
                delay = self.ping_once()
            except socket.gaierror as e:
                print("Ping dailed. (socket error: '%s')" %e[1])
                break

            if delay == None:
                print("Ping failed. (timeout within %s sec)" %self.timeout)
            else:
                delay = delay * 1000
                icmp_seq += 1
                print("icmp_seq=%d time=%0.1fms" %(icmp_seq, delay))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python ping')
    parser.add_argument('--dest-host', action="store", dest="dest_host", required=True)
    given_args = parser.parse_args()
    dest_host = given_args.dest_host
    pinger = Pinger(dest_host=dest_host)
    pinger.ping()
            
