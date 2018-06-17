import socket
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8

def checkSum(str):
    count = 0
    csum = 0
    countTo = (len(str)) - (len(str) % 2)

    while count < countTo:
        thisVal = ord(str[count + 1]) * 256 + ord(str[count])
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count += 2

    if countTo < len(str):
        csum = csum + ord(str[len(str) - 1])
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = -csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)

    return answer

def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout

    while True:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = time.time() - startedSelect
        if whatReady[0] == []:
            return "Request timed out"
        timeRecived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)

        # Fetch ICMP header form the IP packet
        icmpPacket = recPacket[20:]
        icmpType, icmpCode, icmpCheckSum, icmpID, icmpSeq, icmpTimeStamp = \
                                                           struct.unpack("bbHHhd", icmpPacket)
        if checkSum(icmpPacket) == 0 and icmpTipe == 0 \
           and icmpCode == 0 and icmpID == ID and icmpSeq == 1:
            return time.time() - icmpTimeStamp

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return "Request timed out"

def sendOnePing(mySocket, destAddr, ID):
    myCheckSum = 0
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myCheckSum, ID, 1)
    data = struct.pack("d", time.time())
    myCheckSum = checkSum(header + data)

    # Get the right checksum and put in the header
    if sys.playform == 'darwin':
        myCheckSum = htons(myCheckSum) & 0xffff
        # Convert 16-bit int form host to network byte order
    else:
        myCheckSum = htons(myCheckSum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myCheckSUm, ID, 1)
    packet = header + data

    mySocket.sendto(packet, (destAddr, 1))

def doOnePing(destAddr, timeout):
    icmp = socket.getprotobyname("icmp")

    mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)

    myID = os.getpid() & 0xFFFF

    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)

    mySocket.close()
    return delay

def ping(host, timeout=1):
    dest = socket.gethostbyname(host)
    print("Ping " + dest + " using Python:")
    print("")
    while True:
        delay = doOnePing(dest, timeout)
        print(delay)
        time.sleep(1)

    return delay

ping("23.61.196.58")


