from time import sleep
import math
import os
import csv
import ray
import time
import itertools
import pandas
import numpy as np


# ray.init(address='ray://192.168.31.196:10001')
ray.init(address='auto', _redis_password='5241590000000000')
# ray.init()

@ray.remote
def dataset_cal(data: ray.data.Dataset[int]) -> int:
    z=0
    for task in data.iter_batches(batch_format="pandas"):
        num = task.values
        for i in num:
            lg = float(i[0])
            cs = float(i[1])
            z += 3*math.log(lg) + math.cos(cs) ** 2
    return z

@ray.remote
def nfs_cal(filename):
    z=0
    home_path = os.path.expanduser('~')
    # with open('%s/Downloads/my_150m_data.csv' %(home_path),'r') as read_file:
    with open('%s/nfsroot/%s' %(home_path,filename),'r') as read_file:
        reader = csv.reader(read_file)
        for i in itertools.islice(reader,1,None):
            lg = float(i[0])
            cs = float(i[1])
            z += 3 * math.log(lg) + math.cos(cs) ** 2
    return z

@ray.remote
def local_cal(filename):
    z=0
    home_path = os.path.expanduser('~')
    # with open('%s/Downloads/my_150m_data.csv' %(home_path),'r') as read_file:
    with open('%s/Downloads/%s' %(home_path,filename),'r') as read_file:
        reader = csv.reader(read_file)
        for i in itertools.islice(reader,1,None):
            lg = float(i[0])
            cs = float(i[1])
            z += 3 * math.log(lg) + math.cos(cs) ** 2
    return z


# df = pandas.read_csv("/home/lwh/Documents/VEC-Blockchain/task_3M.csv")
# file = ray.data.from_pandas(df)
file = ray.data.read_csv("/home/lwh/Documents/VEC-Blockchain/task_3M.csv")
# file = ray.data.from_items([{"log": i, "cos": i, "times": 1} for i in range(1,25000000)])
# task_file = ["task_100M_1.csv","task_100M_2.csv","task_100M_3.csv","task_100M_4.csv"]
# for pandafile in file.iter_batches(batch_format="pandas"):
#     # pandafile.to_csv("test.csv")
#     # z = pandafile.iloc[:,0]
#     print(pandafile.values)

Vehicle1 = ["Vehicle-1",1]
Vehicle2 = ["Vehicle-2",1]
Vehicle3 = ["Vehicle-3",1]


time_start = time.time()
# ray dataset
v2_task1=dataset_cal.options(num_cpus=1, resources={Vehicle2[0]: 1}).remote(file)
v2_task2=dataset_cal.options(num_cpus=1, resources={Vehicle2[0]: 1}).remote(file)
v2_task3=dataset_cal.options(num_cpus=1, resources={Vehicle2[0]: 1}).remote(file)
v2_task4=dataset_cal.options(num_cpus=1, resources={Vehicle2[0]: 1}).remote(file)

v3_task1=dataset_cal.options(num_cpus=1, resources={Vehicle3[0]: 1}).remote(file)
v3_task2=dataset_cal.options(num_cpus=1, resources={Vehicle3[0]: 1}).remote(file)
v3_task3=dataset_cal.options(num_cpus=1, resources={Vehicle3[0]: 1}).remote(file)
v3_task4=dataset_cal.options(num_cpus=1, resources={Vehicle3[0]: 1}).remote(file)


# nfs task file
# v2_task1=nfs_cal.options(num_cpus=1, resources={Vehicle2[0]: 1}).remote(task_file[0])
# v2_task2=nfs_cal.options(num_cpus=1, resources={Vehicle2[0]: 1}).remote(task_file[1])
# v2_task3=nfs_cal.options(num_cpus=1, resources={Vehicle2[0]: 1}).remote(task_file[2])
# v2_task4=nfs_cal.options(num_cpus=1, resources={Vehicle2[0]: 1}).remote(task_file[3])

# v3_task1=nfs_cal.options(num_cpus=1, resources={Vehicle3[0]: 1}).remote(task_file[0])
# v3_task2=nfs_cal.options(num_cpus=1, resources={Vehicle3[0]: 1}).remote(task_file[1])
# v3_task3=nfs_cal.options(num_cpus=1, resources={Vehicle3[0]: 1}).remote(task_file[2])
# v3_task4=nfs_cal.options(num_cpus=1, resources={Vehicle3[0]: 1}).remote(task_file[3])

# local task file
# v2_task1=local_cal.options(num_cpus=1, resources={Vehicle2[0]: 1}).remote(task_file[0])
# v2_task2=local_cal.options(num_cpus=1, resources={Vehicle2[0]: 1}).remote(task_file[1])
# v2_task3=local_cal.options(num_cpus=1, resources={Vehicle2[0]: 1}).remote(task_file[2])
# v2_task4=local_cal.options(num_cpus=1, resources={Vehicle2[0]: 1}).remote(task_file[3])

# v3_task1=local_cal.options(num_cpus=1, resources={Vehicle3[0]: 1}).remote(task_file[0])
# v3_task2=local_cal.options(num_cpus=1, resources={Vehicle3[0]: 1}).remote(task_file[1])
# v3_task3=local_cal.options(num_cpus=1, resources={Vehicle3[0]: 1}).remote(task_file[2])
# v3_task4=local_cal.options(num_cpus=1, resources={Vehicle3[0]: 1}).remote(task_file[3])


v2_result1 = ray.get(v2_task1)
v2_result2 = ray.get(v2_task2)
v2_result3 = ray.get(v2_task3)
v2_result4 = ray.get(v2_task4)

v3_result1 = ray.get(v3_task1)
v3_result2 = ray.get(v3_task2)
v3_result3 = ray.get(v3_task3)
v3_result4 = ray.get(v3_task4)

time_end = time.time()
total_time = time_end - time_start
print("Vehicle 2 task result:\n1. %f\n2. %f\n3. %f\n4. %f" %(v2_result1,v2_result2,v2_result3,v2_result4))
print("Vehicle 3 task result:\n1. %f\n2. %f\n3. %f\n4. %f" %(v3_result1,v3_result2,v3_result3,v3_result4))
print("Totla time is: %f" %(total_time))
