import socket
import struct
import time
import threading
import queue
import ray
import math
import requests
import time
import pandas as pd

q = queue.Queue(maxsize=10)

@ray.remote
def cal(data: ray.data.Dataset[int]) -> int:
    link_time=time.time()
    z=0
    for task in data.iter_batches(batch_format="pandas"):
        num = task.values
        for i in num:
            lg = float(i[0])
            cs = float(i[1])
            z += 3*math.log(lg) + math.cos(cs) ** 2
    cal_time=time.time()
    print("cal time:",cal_time-link_time)
    return z

def loc_cal(data: pd.DataFrame):
    z=0
    i=0
    for index, row in data.iterrows():
        # print(row[1])
        lg = float(row[0])
        cs = float(row[1])
        z += 3*math.log(lg) + math.cos(cs) ** 2
        i += 1
        if i>200 :
            break
    return z

def udp_server():
    # Creat a UDP socket
    sk = socket.socket(type=socket.SOCK_DGRAM)

    # Bind socket to port 4563
    sk.bind(("",4563))
    while 1:
        rec, cli_addr = sk.recvfrom(1024)
        msg = struct.unpack('!20si20s',rec)
        q.put(msg)
        # sk.close()

def udp_send(msg,ip,port):
    sk = socket.socket(type=socket.SOCK_DGRAM)
    sk.sendto(msg,(ip,port))

if __name__ == "__main__":
    ray.init(address='auto', _redis_password='5241590000000000')
    udp_get = threading.Thread(target=udp_server)
    udp_get.setDaemon(True)
    udp_get.start()
    while q.empty():
        pass
    # get IP, port, file name
    msg = q.get_nowait()
    ip = msg[0].decode().rstrip('\x00')
    port = msg[1]
    file = msg[2].decode().rstrip('\x00')

    # deal with task
    start_time = time.time()
    df = pd.read_csv("http://%s:%s/%s"%(ip,port,file))
    
    # cal_data = ray.data.from_pandas(df)
    # task = cal.remote(cal_data)
    # result = str(ray.get(task))
    result = str(loc_cal(df))
    end_time = time.time()
    with open("./result.txt",'w') as f:
        f.write(result)
        f.close()
    
    f = open("./result.txt",'rb')
    test_response = requests.post("http://%s:%s/result.txt"%(ip,port),f)
    
    print("Total time: ",end_time-start_time)

    complete = struct.pack('!20si20s',b'complete',4563,file.encode())
    udp_send(complete,ip,4563)
    udp_send(complete,"192.168.31.196",4563)
    