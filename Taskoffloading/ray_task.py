import struct
import time
import udp_request
import ray
import math
import random

@ray.remote
def cal(data: ray.data.Dataset[int],p1: int, cho1: int, p2: int, cho2:int) -> float:
    start=time.time()
    z1=0
    z2=0
    for task in data.iter_batches(batch_format="pandas"):
        num = task.values
        for i in num:
            if cho1 == 1:
                z1 += math.cos(float(i[0]))
            elif cho1 == 2:
                z1 += math.sin(float(i[0]))
            elif cho1 == 3:
                z1 += math.log(float(i[0]))
            else:
                z1 += float(i[0]) ** 2

            if cho2 == 1:
                z2 += math.cos(float(i[1]))
            elif cho2 == 2:
                z2 += math.sin(float(i[1]))
            elif cho2 == 3:
                z2 += math.log(float(i[1]))
            else:
                z2 += float(i[1]) ** 2
            # lg = float(i[0])
            # cs = float(i[1])
            # z1 += 3*math.log(lg) + math.cos(cs) ** 2
    end=time.time()
    z = p1*z1 + p2*z2
    print("cal time:",end-start)
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
    tau_n = ['0.5','1','1','2','4']
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
        p1 = random.randint(1,10)
        p2 = random.randint(1,10)
        cho1 = random.randint(1,4)
        cho2 = random.randint(1,4)
        bs_id = random.randint(0,1)
        # bs_id = 1
        start_time = time.time()
        '''Send request to SAC until SAC return a "offloading" packet '''
        # while msg[0].decode().rstrip('\x00') != "offloading":
        #     print("sent request")
        #     udp_request.udp_send(req,tv_id,str(event),Dn[n],Station_IP)
        #     msg,addr =  udp_request.udp_server()
        requset_msg = struct.pack("!i10s10s10s10s10s10s",6,b"request",tv_id.encode(),str(event).encode(),Dn[n].encode(),Cn[n].encode(),tau_n[n].encode())
        status = udp_request.send(requset_msg,Station_IP[bs_id])
        
        if status == False:
            print("Send request fail")
            time.sleep(1)
            continue
    
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
            task = cal.options(num_cpus=1, resources={vid: 1}).remote(file0,p1,cho1,p2,cho2)
        elif n== 1:
            task = cal.options(num_cpus=1, resources={vid: 1}).remote(file1,p1,cho1,p2,cho2)
        elif n== 2:
            task = cal.options(num_cpus=1, resources={vid: 1}).remote(file2,p1,cho1,p2,cho2)
        elif n== 3:
            task = cal.options(num_cpus=1, resources={vid: 1}).remote(file3,p1,cho1,p2,cho2)
        elif n== 4:
            task = cal.options(num_cpus=1, resources={vid: 1}).remote(file4,p1,cho1,p2,cho2)
        
        result = ray.get(task)
        end_time = time.time()
        total_time = end_time-start_time
        theta = float(Cn[n])/1.5

        # Send complete packet to SAC
        complete_msg = struct.pack('!i10s10s10s10s',4,b'complete',tv_id.encode(),str(theta).encode(),b"successful")
        udp_request.send(complete_msg,Station_IP[bs_id])
        if event < 14:
            event += 1
        else:
            event = 1
            print("Completed all of the events")
        print("#",n," task is completed by: ",vid)
        print("Total time: ",total_time)
        time.sleep(1)
