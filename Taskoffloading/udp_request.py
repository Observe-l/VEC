import socket
import struct

def udp_server():
    # Creat a UDP socket
    sk = socket.socket(type=socket.SOCK_DGRAM)
    # Bind socket to port 4563
    sk.bind(("",4563))
    rec, cli_addr = sk.recvfrom(1024)
    # message fomat: 1.request: string; 2.ID: string; 3.Task size: float;
    msg = struct.unpack('!20s20sf',rec)
    return msg, cli_addr

def udp_send(req:str,ID:str,size:float,ip):
    sk = socket.socket(type=socket.SOCK_DGRAM)
    msg = struct.pack('!20s20sf',req.encode(),ID.encode(),size)
    sk.sendto(msg,(ip,4563))