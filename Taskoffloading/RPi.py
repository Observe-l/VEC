import time
import udp_request
import struct
import ray
import math

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
    # while 1:
    #     a = input("Select task:\n[1]easy [2]media [3]heavy\n")
    #     start_time = time.time()
    #     if a == '1':
    #         file = ray.data.read_csv("/home/ubuntu/Documents/Taskfile/task_200K.csv")
    #         size = 0.2
    #         break
    #     elif a == '2':
    #         file = ray.data.read_csv("/home/ubuntu/Documents/Taskfile/task_2M.csv")
    #         size = 2.0
    #         break
    #     elif a == '3':
    #         file = ray.data.read_csv("/home/ubuntu/Documents/Taskfile/task_4M.csv")
    #         size = 4.0
    #         break
    #     else:
    #         print("Input wrong\n")

    file = ray.data.read_csv("/home/ubuntu/Documents/Taskfile/task_200K.csv")
    size = 0.2
    a = input("Start\n")
    n = 0
    while 1:
        start_time = time.time()
        msg = struct.pack('!20s20sf',b'request',b'vehicle1',size)
        udp_request.udp_send("request","vehicle1",size,"192.168.1.117")
        msg,addr =  udp_request.udp_server()
        print("get return")
        action = msg[1].decode().rstrip('\x00')
        if action == '0':
            vid = "vehicle1"
        elif action == '1':
            vid = "vehicle2"
        else:
            vid = "vehicle3"
        task = cal.options(num_cpus=1, resources={vid: 1}).remote(file)
        result = ray.get(task)
        end_time = time.time()
        n += 1
        print("#",n," task complete from: ",vid)
        print("Total time: ",end_time-start_time)
