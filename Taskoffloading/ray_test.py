import random
import time
import ray
import math

@ray.remote
def cal(data: ray.data.Dataset[int],cho1: int, cho2: int, p1: int, p2:int, it_range: int) -> float:
    start=time.time()
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
    end=time.time()
    z = p1*z1 + p2*z2
    print("cal time:",end-start)
    del data
    return z

def local_cal(data: ray.data.Dataset[int],cho1: int, cho2: int, p1: int, p2:int, it_range:int) -> float:
    start=time.time()
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
            for i in num:
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



if __name__ == "__main__":
    ray.init(address='auto', _redis_password='5241590000000000')
    # ray.init(address='ray://192.168.1.119:10001')
    file = []

    # file_list = ["/home/lwh/Documents/VEC/Taskoffloading/Taskfile/task_200Kbits.csv","/home/lwh/Documents/VEC/Taskoffloading/Taskfile/task_1Mbits.csv",
    #              "/home/lwh/Documents/VEC/Taskoffloading/Taskfile/task_2Mbits.csv","/home/lwh/Documents/VEC/Taskoffloading/Taskfile/task_3Mbits.csv","/home/lwh/Documents/VEC/Taskoffloading/Taskfile/task_4Mbits.csv"]
    file_list = ["/home/ubuntu/Documents/Taskfile/task_200Kbits.csv","/home/ubuntu/Documents/Taskfile/task_1Mbits.csv",
                 "/home/ubuntu/Documents/Taskfile/task_2Mbits.csv","/home/ubuntu/Documents/Taskfile/task_3Mbits.csv",
                 "/home/ubuntu/Documents/Taskfile/task_4Mbits.csv"]

    for file_name in file_list:
        file.append(ray.data.read_csv(file_name))
    # D_list = [0.2,1,2,3,4]
    # # This should be set at basestation program.
    # fs = random.uniform(3,7)
    # n = random.randint(0,4)
    # base_iter = get_iter(n)
    # Cn = cal_cn(n,base_iter)
    # # All parameter, [cho1,cho2,p1,p2,iter]
    # all_parameter = [random.randint(1,4),random.randint(1,4),random.randint(1,10),random.randint(1,10),round(7/fs*base_iter)]
    # Dn = D_list[n]
    n=int(input("Select file:[0]200Kbits; [1]1Mbits; [2]2Mbits; [3]3Mbits; [4]4Mbits\n"))
    i = 0
    while i < 10:
        task = cal.options(resources={"vehicle10": 1}).remote(file[n],1,1,5,6,15)
        task_result = ray.get(task)
        del task
        i += 1

    # for i in range(20):
    #     cho1 = random.randint(1,4)
    #     cho2 = random.randint(1,4)s
    #     task = cal.remote(file[4],1,cho1,10,cho2,30)
    #     result = ray.get(task)
    #     print(result)
    # Chose Task randomly. 0.2MB,
    # file0 = ray.data.read_csv("/home/ubuntu/Documents/Taskfile/task_200Kbits.csv")
    # file1 = ray.data.read_csv("/home/ubuntu/Documents/Taskfile/task_1Mbits.csv")
    # file2 = ray.data.read_csv("/home/ubuntu/Documents/Taskfile/task_2Mbits.csv")
    # file3 = ray.data.read_csv("/home/ubuntu/Documents/Taskfile/task_3Mbits.csv")
    # file4 = ray.data.read_csv("/home/ubuntu/Documents/Taskfile/task_4Mbits.csv")
    # file0 = ray.data.read_csv("/home/lwh/Documents/VEC/Taskoffloading/Taskfile/task_200Kbits.csv")
    # file1 = ray.data.read_csv("/home/lwh/Documents/VEC/Taskoffloading/Taskfile/task_1Mbits.csv")
    # file2 = ray.data.read_csv("/home/lwh/Documents/VEC/Taskoffloading/Taskfile/task_2Mbits.csv")
    # file3 = ray.data.read_csv("/home/lwh/Documents/VEC/Taskoffloading/Taskfile/task_3Mbits.csv")
    # file4 = ray.data.read_csv("/home/lwh/Documents/VEC/Taskoffloading/Taskfile/task_4Mbits.csv")

    # size = [0.2,1,2,3,4]
    
    # # a = input("Select Task:[0:200K, 1:1M, 2:2M, 3:3M, 4:4M]\n")
    # print("start")
    # while 1:
    #     p1 = random.randint(1,10)
    #     p2 = random.randint(1,10)
    #     cho1 = random.randint(1,4)
    #     cho2 = random.randint(1,4)

    #     start_time = time.time()

    #     task = cal.options(num_cpus=1, resources={"vehicle2": 1}).remote(file4,p1,cho1,p2,cho2)
    #     result = ray.get(task)
    #     # result = local_cal(file4,p1,cho1,p2,cho2)
    #     end_time = time.time()
    #     total_time = end_time-start_time
    #     print("Total time: ",total_time)
    #     print("cho1:",cho1,"cho2:",cho2)
    #     print("result is:",result)
