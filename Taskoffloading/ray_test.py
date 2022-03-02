import time
import udp_request
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

    # Chose Task randomly. 0.2MB,
    file = []
    file[0] = ray.data.read_csv("/home/ubuntu/Documents/Taskfile/task_200Kbits.csv")
    file[1] = ray.data.read_csv("/home/ubuntu/Documents/Taskfile/task_1Mbits.csv")
    file[2] = ray.data.read_csv("/home/ubuntu/Documents/Taskfile/task_2Mbits.csv")
    file[3] = ray.data.read_csv("/home/ubuntu/Documents/Taskfile/task_3Mbits.csv")
    file[4] = ray.data.read_csv("/home/ubuntu/Documents/Taskfile/task_4Mbits.csv")
    size = [0.2,1,2,3,4]
    
    a = input("Select Task:[0:200K, 1:1M, 2:2M, 3:3M, 4:4M]\n")
    start_time = time.time()

    task = cal.options(num_cpus=1, resources={"vehicle2": 1}).remote(file[a])
    result = ray.get(task)
    end_time = time.time()
    total_time = end_time-start_time
    print("Total time: ",total_time)
    print("#",a," task is completed by: vehicle2")
    print("Task size: ",size[a],"Mbits")
