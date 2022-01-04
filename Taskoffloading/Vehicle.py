'''
Author: Liu Weihao
Data: 12//09/2021
File name: Vehicle.py
'''

import math
import random
import ray

# ray.init()

'''
This Object is the vehical model. The virable type indicate the vehical's type. "Vs" is service vehicle, "Vt" is task vehicle
There are 13 virables
num: Vehicle number
type: Vehicle type, "Vs" (service vehicle) or "Vt" (taks vehicle).
com_source: The computational capability, the utility is (GHz), and the value is a random number in [3, 7]
task_num: If the vehical is a task vehical, this virable is indicate the total number of the take need to be allocated
data_size: This is a list of task data size. The lens of the list is task_num. The value is a random number in [0.2, 4] (Mbits)
com_size: This is a list of computation size whice every task needed. The lens of the list is task_num. The value is a random number in [0.2,3.2] (10^9 cycles)
price: unit price

tol_time: This is a list of tolerance time. The value is one of elements in {0.5, 1, 2, 4} (s)
com_efficiency: The computation efficiency of the service vehicle
complete_ratio: The completion ratio of a service vehicle
num_offload: The total number of received offloading tasks
'''

@ray.remote
class vehicle_model(object):
    task_num = 0
    data_size = []
    com_size = []
    tol_time = []
    price = []

    com_efficiency = 1
    complete_ratio = 1
    num_offload = 0
    
    def __init__(self, num = 0):
        self.num = num
        self.type = "Vs"
        self.com_source = random.uniform(3,7) #GHz
        self.weight1 = 0.5
        self.weight2 = 0.5

    '''
    When a task vehicle need to allocate some tasks to other service vehicles, use this function.
    It will generate task numbers, task data size, computational size, delay of task randomly.
    The function will return these values in order
    '''
    def task_request(self):
        if self.type == "Vt":
            return "The task haven't complete"

        self.type = "Vt"
        
        self.task_num = random.randint(2,5)  # generate task number
        # clear origional data
        self.data_size = None
        self.com_size = None
        self.tol_time = None
        self.price = None

        # generate some random data. The length of the list is task_num.
        self.data_size = [random.uniform(0.2, 4) for _ in range(self.task_num)]
        self.com_size = [random.uniform(0.2, 3.2) for _ in range(self.task_num)]
        self.tol_time = [random.choice([0.5, 1, 2, 4]) for _ in range(self.task_num)]
        self.price = [random.uniform(0.1, 0.5) for _ in range(self.task_num)]
        
        return self.num, self.type, self.task_num, self.data_size, self.com_size, self.tol_time, self.price
    
    '''
    Service vehicle model. Task vehicle will give data size and some other necessary data to service vehicle.
    This function will return it's own reliability, utility and the delay time.
    '''
    def task_handle(self, data_size, com_size, tol_time, trans_rate, pn):
        if self.type == 'Vt':
            return "The task haven't complete"
        
        self.type = "Vs"
        k = pow(10, -26)
        constant_1 = pow(pn/k, 0.5) * pow(10, -12)
        if constant_1 > self.com_source:
            fn = random.uniform(0, self.com_source)
        else:
            fn = random.uniform(0, constant_1)

        delay_time = data_size / trans_rate + com_size / fn
        utitlity_task = math.log(1 + tol_time-delay_time) / math.log(1 + tol_time)
        self.com_efficiency = (1 - self.weight1) * self.com_efficiency + self.weight1 * utitlity_task

        if delay_time <= tol_time:
            self.complete_ratio = (self.num_offload * self.complete_ratio + 1) / (self.num_offload + 1)
        else:
            self.complete_ratio = (self.num_offload * self.complete_ratio) / (self.num_offload + 1)

        reliability = self.weight2 * self.com_efficiency + (1 - self.weight2) * self.complete_ratio
        utitlity_service_vehicle = pn * com_size - k * pow(fn, 2) * com_size

        return reliability, utitlity_service_vehicle, delay_time

    
    '''
    When service vehicle complete the take, task vehicle will receive the delay time of this taks.
    Then, it will give price or penalty to service vehicle
    '''
    def task_comfirm(self, delay_time, task):
        self.task_num -= 1
        if self.task_num == 0:
            self.type = "Vs"
        
        A = -0.5 #penalty
        if delay_time <= self.tol_time[task]:
            utility_task = math.log(1 + self.tol_time[task] - delay_time)
        else:
            utility_task = A
        
        utility_task_vehicle = utility_task - self.price[task] * self.com_size[task]
        
        if delay_time <= self.tol_time[task]:
            return self.price[task] * self.com_size[task], utility_task_vehicle
        else:
            return A, utility_task_vehicle
    
    def vehicular_type(self):
        return self.type

'''
Caculate transmmission data rate. This function haven't complete yet
'''
def trans_rate(dist):
    trans_power = 30 # transmission power 30dBm
    freq = 5.3 # frequency GHz
    path_loss = 32.4 + 20 * math.log(dist, 10) + 20 * math.log(freq, 10)
    gain = 3 # antenna gain dBi
    noise = -174 # White Gaussian noise, -174 dB/Hz
    interference_noise = -150 # interference introduced by other V2V transmissions
    bandwidth = 20 # bandwidth 20Mhz
    rate = bandwidth * math.log(1 + (trans_power * pow(dist, -path_loss) * pow(gain, 2))/ (noise + interference_noise), 10)
    return rate


# test code
vehicle_1 = vehicle_model.options(num_cpus=1, resources={"Task-Vehicle": 1}).remote(1)
vehicle_2 = vehicle_model.options(num_cpus=1, resources={"Task-Vehicle": 2}).remote(2)
vehicle_3 = vehicle_model.options(num_cpus=2, resources={"Task-Vehicle": 3}).remote(3)
vehicle_4 = vehicle_model.options(num_cpus=1, resources={"Service-Vehicle": 1}).remote(4)
vehicle_5 = vehicle_model.options(num_cpus=1, resources={"Service-Vehicle": 2}).remote(5)
vehicle_6 = vehicle_model.options(num_cpus=2, resources={"Service-Vehicle": 3}).remote(6)
d1 = vehicle_1.task_request.remote()
c1, c2, c3, c4, c5, c6, c7 = ray.get(d1)
print("Vehicle number is:\t", c1, "\nVehicle type is:\t", c2, "\nTotle number of take:\t", c3, "\nData size:\t\t", c4, "Mbits\nComputation size:\t", c5, "10^9 cycles\nTolerance time:\t\t", c6, "s\nUnit price:\t\t", c7)
d2 = vehicle_2.task_handle.remote(c4[1], c5[1], c6[1], 20, c7[1])
e1,e2,e3 = ray.get(d2)
print("\nService vehicle 1 reliability:\t", e1, "\nService vehicle 1 utility:\t", e2, "\nService vehicle 1 delay time:\t", e3)
# c2 = trans_rate(20)
# print(c2)
