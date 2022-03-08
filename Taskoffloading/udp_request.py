import socket
import struct

def udp_server():
    # Creat a UDP socket
    sk = socket.socket(type=socket.SOCK_DGRAM)
    # Bind socket to port 4563
    sk.bind(("",4563))
    rec, cli_addr = sk.recvfrom(1024)
    msg = []
    head = struct.unpack("!i",rec[:4])
    # message fomat: 1.head: string; 2-inf. data: string;
    for i in range(0,head[0]):
        msg_tmp = struct.unpack("!20s",rec[20*i+4,20*(i+1)+4])
        msg.append(msg_tmp[0].decode().rstrip('\x00'))
    # msg = struct.unpack('!20s20s20s20s',rec)
    return msg, cli_addr

def udp_send(msg,ip):
    sk = socket.socket(type=socket.SOCK_DGRAM)
    # msg = struct.pack('!20s20s20s20s',req.encode(),data1.encode(),data2.encode(),data3.encode())
    sk.sendto(msg,(ip,4563))
