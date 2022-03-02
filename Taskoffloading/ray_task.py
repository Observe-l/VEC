import time
import udp_request
import ray
import math
import random

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

if __name__ == "__main__":
    ray.init(address='auto', _redis_password='5241590000000000')

    # Chose Task randomly. 0.2MB,
    file = []
    file[0] = ray.data.read_csv("/home/ubuntu/Documents/Taskfile/task_200Kbits.csv")
    file[1] = ray.data.read_csv("/home/ubuntu/Documents/Taskfile/task_1Mbits.csv")
    file[2] = ray.data.read_csv("/home/ubuntu/Documents/Taskfile/task_2Mbits.csv")
    file[3] = ray.data.read_csv("/home/ubuntu/Documents/Taskfile/task_3Mbits.csv")
    file[4] = ray.data.read_csv("/home/ubuntu/Documents/Taskfile/task_4Mbits.csv")
    size = [0.2,1,2,3,4]
    
    a = input("Start\n")
    n = 0
    while 1:
        n = random.choice([0,1,2,3,4])
        start_time = time.time()
        # Send a request
        # msg = struct.pack('!20s20sf',b'request',b'vehicle1',size[n])
        udp_request.udp_send("request","vehicle1",size[n],"192.168.1.117")
        msg,addr =  udp_request.udp_server()
        print("get return")
        action = msg[1].decode().rstrip('\x00')
        if action == '0':
            vid = "vehicle1"
        elif action == '1':
            vid = "vehicle2"
        else:
            vid = "vehicle3"
        task = cal.options(num_cpus=1, resources={vid: 1}).remote(file[n])
        result = ray.get(task)
        end_time = time.time()
        total_time = end_time-start_time
        # msg = struct.pack('!20s20sf',b'complete',vid.encode(),total_time)
        udp_request.udp_send("complete",vid,total_time,"192.168.1.117")
        print("#",n," task is completed by: ",vid)
        print("Total time: ",total_time)
