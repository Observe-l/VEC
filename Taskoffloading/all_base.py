import socket
import struct
import time
import threading
import queue

# q = queue.Queue(maxsize=10)


def udp_server():
    # Creat a UDP socket
    sk = socket.socket(type=socket.SOCK_DGRAM)
    # Bind socket to port 4563
    sk.bind(("",4563))
    while 1:
        rec, cli_addr = sk.recvfrom(1024)
        msg = struct.unpack('!20si20s',rec)
        udp_send(msg,cli_addr)
        # sk.close()
        

def udp_send(msg,addr):
    sk = socket.socket(type=socket.SOCK_DGRAM)
    if msg[0].decode().rstrip('\x00') == 'send':
        port = msg[1]
        print(port)
        if addr[0] == '192.168.31.216':
            ip = '192.168.31.238'
        else:
            ip = '192.168.31.216'
        file = msg[2]
        offload = struct.pack('!20si20s',addr[0].encode(),port,file)
        sk.sendto(offload,(ip,4563))
    elif msg[0].decode().rstrip('\x00') == 'complete':
        print("Task is complete from: ",addr[0])


if __name__ == "__main__":
    udp_get = threading.Thread(target=udp_server)
    # udp_get.setDaemon(True)
    udp_get.start()
    print("This is a test!")
    # z = input("test input:")
    # udp_get.join()
    