import time
import ray
import socket
import struct

def udp_server():
    # Creat a UDP socket
    sk = socket.socket(type=socket.SOCK_DGRAM)

    # Bind socket to port 4563
    sk.bind(("",4563))
    rec, cli_addr = sk.recvfrom(1024)


def udp_send(msg,ip,port):
    sk = socket.socket(type=socket.SOCK_DGRAM)
    sk.sendto(msg,(ip,port))

if __name__ == "__main__":
    ray.init(address='auto', _redis_password='5241590000000000')
    while 1:
        a = input("Select task:\n[1]easy [2]media [3]heavy\n")
        start_time = time.time()
        if a == '1':
            file = "task_200K.csv"
            break
        elif a == '2':
            file = "task_2M.csv"
            break
        elif a == '3':
            file = "task_4M.csv"
            break
        else:
            print("Input wrong")


    msg = struct.pack('!20si20s',b'send',8000,file.encode())
    udp_send(msg,"192.168.31.196",4563)
    udp_server()
    end_time = time.time()
    print("Total time: ",end_time-start_time)