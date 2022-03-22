import struct
import time
import udp_request
import ray
import math
import random

@ray.remote
def cal(data: ray.data.Dataset[int],cho1: int, cho2: int, p1: int, p2:int, it_range: int) -> float:
    # start=time.time()
    z1=0
    z2=0
    for task in data.iter_batches(batch_format="pandas"):
        num = task.values
        for ite in range(it_range):
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
    # end=time.time()
    z = p1*z1 + p2*z2
    # print("cal time:",end-start)
    return z

# Execution time: T = Cn / Fs, here, Fs is 7. So Cn = T * 7
def cal_cn(file_id:int, iter:int) -> float:
    if file_id == 0:
        return float(iter/30*0.2 * 7 )
    elif file_id == 1:
        return float(iter/30*1 * 7)
    elif file_id == 2:
        return float(iter/20*1.3 * 7)
    elif file_id == 3:
        return float(iter/15*1.4 * 7)
    else:
        return float(iter/15*1.55 *7)

def get_iter(file_id: int) -> int:
    if file_id == 0:
        return random.randint(1,77)
    elif file_id == 1:
        return random.randint(1,15)
    elif file_id == 2:
        return random.randint(1,8)
    elif file_id == 3:
        return random.randint(1,6)
    else:
        return random.randint(1,5)

# select maximum delay of task. Assume that Dn=2.0 Mbps, Cn=5.0GHz
def get_tau(Dn:float, Cn:float) -> float:
    tau_T = Dn/2.0 + Cn/5.0
    if tau_T < 0.2:
        return 0.5
    elif tau_T < 0.7:
        return 1.0
    elif tau_T < 1.3:
        return 2.0
    else:
        return 4.0

if __name__ == "__main__":
    ray.init(address='auto', _redis_password='5241590000000000')
    # Chose Task randomly. 0.2Mbits ~ 4Mbits
    file = []
    file_list = ["/home/ubuntu/Documents/Taskfile/task_200Kbits.csv","/home/ubuntu/Documents/Taskfile/task_1Mbits.csv",
                 "/home/ubuntu/Documents/Taskfile/task_2Mbits.csv","/home/ubuntu/Documents/Taskfile/task_3Mbits.csv",
                 "/home/ubuntu/Documents/Taskfile/task_4Mbits.csv"]
    for file_name in file_list:
        file.append(ray.data.read_csv(file_name))
    
    Dn = ['0.2','1','2','3','4']

    Station_IP = ["192.168.1.117","192.168.1.122"]
    vid = ["vehicle0","vehicle1","vehicle2","vehicle3"]

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
        # Choose some task randomly
        base_iter = get_iter(n)
        Cn = str(cal_cn(n,base_iter))
        tau_n = get_tau(float(Dn[n]),float(Cn))
        bs_id = random.randint(0,1)
        # bs_id = 1
        start_time = time.time()
        '''Send request to SAC until SAC return a "offloading" packet '''
        requset_msg = struct.pack("!i10s10s10s10s10s10s",6,b"request",tv_id.encode(),str(event).encode(),Dn[n].encode(),Cn.encode(),str(tau_n).encode())
        status = udp_request.send(requset_msg,Station_IP[bs_id])

        if status == False:
            print("Send request fail")
            time.sleep(1)
            continue
    
        print("sent request to:",Station_IP[bs_id])
        msg, addr = udp_request.receive("offloading")
        print("get return")
        action = msg[1]
        fs = float(msg[2])
        # All parameter, [cho1,cho2,p1,p2,iter]
        all_parameter = [random.randint(1,4),random.randint(1,4),random.randint(1,10),random.randint(1,10),round(7/fs*base_iter)]
        task = cal.options(num_cpus=1, resources={vid[int(action)]: 1}).remote(file[n],all_parameter[0],all_parameter[1],all_parameter[2],all_parameter[3],all_parameter[4])
        result = ray.get(task)
        del task
        end_time = time.time()
        total_time = end_time-start_time

        if total_time > tau_n:
            status = "fail"
        else:
            status = "successful"
        # Send complete packet to SAC
        complete_msg = struct.pack('!i10s10s10s10s',4,b'complete',tv_id.encode(),str(total_time).encode(),status.encode())
        udp_request.send(complete_msg,Station_IP[bs_id])
        if event < 14:
            event += 1
        else:
            event = 1
            print("Completed all of the events")
        print("#",n," task is completed by: ",vid[int(action)])
        print("Total time: ",total_time,"\n")
        time.sleep(1)
