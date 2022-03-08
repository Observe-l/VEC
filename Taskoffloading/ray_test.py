import random
import time
import ray
import math

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

def local_cal(data: ray.data.Dataset[int],p1: int, cho1: int, p2: int, cho2:int) -> float:
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
    # ray.init(address='auto', _redis_password='5241590000000000')

    # Chose Task randomly. 0.2MB,
    file0 = ray.data.read_csv("/home/ubuntu/Documents/Taskfile/task_200Kbits.csv")
    file1 = ray.data.read_csv("/home/ubuntu/Documents/Taskfile/task_1Mbits.csv")
    file2 = ray.data.read_csv("/home/ubuntu/Documents/Taskfile/task_2Mbits.csv")
    file3 = ray.data.read_csv("/home/ubuntu/Documents/Taskfile/task_3Mbits.csv")
    file4 = ray.data.read_csv("/home/ubuntu/Documents/Taskfile/task_4Mbits.csv")
    # file0 = ray.data.read_csv("/home/lwh/Documents/VEC/Taskoffloading/Taskfile/task_200Kbits.csv")
    # file1 = ray.data.read_csv("/home/lwh/Documents/VEC/Taskoffloading/Taskfile/task_1Mbits.csv")
    # file2 = ray.data.read_csv("/home/lwh/Documents/VEC/Taskoffloading/Taskfile/task_2Mbits.csv")
    # file3 = ray.data.read_csv("/home/lwh/Documents/VEC/Taskoffloading/Taskfile/task_3Mbits.csv")
    # file4 = ray.data.read_csv("/home/lwh/Documents/VEC/Taskoffloading/Taskfile/task_4Mbits.csv")

    size = [0.2,1,2,3,4]
    
    # a = input("Select Task:[0:200K, 1:1M, 2:2M, 3:3M, 4:4M]\n")
    print("start")
    while 1:
        p1 = random.randint(1,10)
        p2 = random.randint(1,10)
        cho1 = random.randint(1,4)
        cho2 = random.randint(1,4)

        start_time = time.time()

        task = cal.options(num_cpus=1, resources={"vehicle2": 1}).remote(file4,p1,cho1,p2,cho2)
        result = ray.get(task)
        # result = local_cal(file4,p1,cho1,p2,cho2)
        end_time = time.time()
        total_time = end_time-start_time
        print("Total time: ",total_time)
        print("cho1:",cho1,"cho2:",cho2)
        print("result is:",result)
