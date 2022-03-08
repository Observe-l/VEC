import socket
import struct
import time

def udp_server(sk: socket.socket):
    rec, cli_addr = sk.recvfrom(1024)
    msg = []
    head = struct.unpack("!i",rec[:4])
    # message fomat: 1.head: string; 2-inf. data: string;
    for i in range(0,head[0]):
        msg_tmp = struct.unpack("!10s",rec[10*i+4:10*(i+1)+4])
        msg.append(msg_tmp[0].decode().rstrip('\x00'))
    # msg = struct.unpack('!20s20s20s20s',rec)
    return msg, cli_addr[0]

def udp_send(msg,ip):
    sk = socket.socket(type=socket.SOCK_DGRAM)
    sk.sendto(msg,(ip,4563))


'''
Application layer protocal based on UPD
Client will send a packet and wait for ACK packet.
If client doesn't get ACK in 0.2s, it will retransmit packets 1-2 times.
If transmit successfully, return "True", else return "False"
'''
def send(msg,ip) -> bool:
    ack_status = False
    ack = ['0','0']
    # message type
    head_type = struct.unpack("!10s",msg[4:14])
    # Creat a UDP socket, timeout = 0.1s, bind to port 4563
    sk = socket.socket(type=socket.SOCK_DGRAM)
    # sk.settimeout(0.05)
    sk.bind(("",4563))
    udp_send(msg,ip)

    # for i in range(0,3):
    #     udp_send(msg,ip)
    #     try:
    #         ack, addr = udp_server(sk)
    #     except:
    #         pass
    #     # If server receives the packet, it will return the a packet.
    #     # Otherwise, client will retransmit the packet 2 times.
    #     if ack[0] == "ACK":
    #         ack_status = True
    #         return ack_status
        
    return ack_status
'''
Application layer protocal based on UDP
After UDP server receive a packet, it will return ACK
'''
def receive():
    sk = socket.socket(type=socket.SOCK_DGRAM)
    sk.bind(("",4563))
    msg,addr = udp_server(sk)
    # ack = struct.pack("!i10s10s",2,b"ACK",msg[0].encode())
    # udp_send(ack, addr)
    return msg, addr
