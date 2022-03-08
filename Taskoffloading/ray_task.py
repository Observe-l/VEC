import struct
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
    file0 = ray.data.read_csv("/home/ubuntu/Documents/Taskfile/task_200Kbits.csv")
    file1 = ray.data.read_csv("/home/ubuntu/Documents/Taskfile/task_1Mbits.csv")
    file2 = ray.data.read_csv("/home/ubuntu/Documents/Taskfile/task_2Mbits.csv")
    file3 = ray.data.read_csv("/home/ubuntu/Documents/Taskfile/task_3Mbits.csv")
    file4 = ray.data.read_csv("/home/ubuntu/Documents/Taskfile/task_4Mbits.csv")
    Dn = ['0.2','1','2','3','4']
    Cn = ['0.2','0.83','1.62','2.41','3.2']
    tau_n = "10"
    Station_IP = ["192.168.1.117","192.168.1.116"]
    req = "request"
    complete = "complete"
    allocate = "offloading"
    # Rpi 1, ID is 0
    tv_id = '0'
    
    a = input("Start\n")
    '''
    Init some parameters
    '''
    n = 0
    event = 1

    while 1:
        n = random.randint(0,4)
        # bs_id = random.randint(0,1)
        bs_id = 1
        start_time = time.time()
        '''Send request to SAC until SAC return a "offloading" packet '''
        # while msg[0].decode().rstrip('\x00') != "offloading":
        #     print("sent request")
        #     udp_request.udp_send(req,tv_id,str(event),Dn[n],Station_IP)
        #     msg,addr =  udp_request.udp_server()
        requset_msg = struct.pack("!i10s10s10s10s10s10s",6,b"request",tv_id.encode(),str(event).encode(),Dn[n].encode(),Cn[n].encode(),tau_n.encode())
        udp_request.send(requset_msg,Station_IP[bs_id])
        print("sent request to:",Station_IP[bs_id])
        msg, addr = udp_request.receive()
        print("get return")
        action = msg[1]
        if action == '0':
            vid = "vehicle1"
        elif action == '1':
            vid = "vehicle2"
        elif action == '2':
            vid = "vehicle3"
        else:
            vid = "vehicle4"

        if n == 0:
            task = cal.options(num_cpus=1, resources={vid: 1}).remote(file0)
        elif n== 1:
            task = cal.options(num_cpus=1, resources={vid: 1}).remote(file1)
        elif n== 2:
            task = cal.options(num_cpus=1, resources={vid: 1}).remote(file2)
        elif n== 3:
            task = cal.options(num_cpus=1, resources={vid: 1}).remote(file3)
        elif n== 4:
            task = cal.options(num_cpus=1, resources={vid: 1}).remote(file4)
        
        result = ray.get(task)
        end_time = time.time()
        total_time = end_time-start_time
        fn = float(Cn[n])/total_time

        # Send complete packet to SAC
        complete_msg = struct.pack('!i10s10s10s10s',4,b'complete',tv_id.encode(),str(total_time).encode(),b"successful")
        udp_request.send(complete_msg,Station_IP[bs_id])
        if event < 14:
            event += 1
        else:
            event = 1
            print("Completed all of the events")
        print("#",n," task is completed by: ",vid)
        print("Total time: ",total_time)
        time.sleep(1.5)
