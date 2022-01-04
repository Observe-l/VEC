import ray
import math
import time
import pandas as pd

ray.init(address='auto', _redis_password='5241590000000000')

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

start_time = time.time()
df = pd.read_csv("./Taskfile/task_200K.csv")
# print(df)
# cal_data = ray.data.read_csv("/home/lwh/Documents/VEC-Blockchain/Taskfile/task_200K.csv")
# task = cal.remote(cal_data)
# result = str(ray.get(task))
result = loc_cal(df)
end_time = time.time()
print("Total time:",end_time-start_time)
