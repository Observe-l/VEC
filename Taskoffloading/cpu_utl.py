import psutil
import time

# Print utilization of cpu in "int_time" seconds. 
# If percpu = True, it will return every core's utilization
def get_cpu(int_time: float):
    utl = psutil.cpu_percent(interval=int_time,percpu=True)
    print("Average CPU utlization:", utl)
    # return utl

# Get the memory
def get_memory():
    all_mem = psutil.virtual_memory()._asdict()
    free_mem =  all_mem['total']
    ava_mem =   all_mem['available']
    utl_mem =   str(all_mem['percent']) + "%"
    used_mem =  all_mem['used']
    print(utl_mem)
    # return free_mem

if __name__ == "__main__":
    interval_time = 1.5
    while 1:
        get_cpu(interval_time)
        get_memory()
        time.sleep(interval_time)

