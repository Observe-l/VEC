from mailbox import NotEmptyError
from util.BSSQLUtil import *
from util.BaseStation import *
import numpy as np
from util.BaseStationTransfer import *
from util.Taskinteraction import taskInteraction
from util.systeminfo import systeminfo
from util.systeminfo import BSCPU
import numpy as np


class A2EnvExtreme:
    def __init__(self):
        
        self.taskIt = taskInteraction()

        self.b = 2  # number of base station
        self.u = 0.1

        # state1 global resource
        self.Gb = None  # state1 global resource

        # state2 reliability
        self.Tn = [4,4] #maximun tolerance delay
        self.omega1 = 0.8  # range from[0,1]
        self.omega2 = 0.8
        # self.normalized_utilization=np.zeros([1,2])
        self.computing_efficiency=np.zeros(self.b)
        self.completion_ratio= np.zeros(self.b)
        self.total_received_task = np.zeros(self.b)
        self.reliability = np.zeros(self.b)
        
        # state3 transactions generated by BSs
        self.Ntr = self.get_Ntr(0)
    

        # action parameters
        self.maximum_block_size = 10  # 10/5=2

        # reward parameters
        self.epsilon1 = 0.8
        self.epsilon2 = 0.2
        self.maximum_tolerance_dalay = 2
        self.gamma = -10
        self.reward = 0
    

    def get_Gb(self):
        '''
        @return: available computing resource
        '''
        # print(self.baseStations[0].vehicle_density)
        sysinfo = systeminfo()
        bscpu=sysinfo.getAllTask()
        self.global_computing_resource = np.array([29,20])
        self.reserved_computing_resource = np.array([i.cpu for i in bscpu])
        print("Reserved Computing Resource:",self.reserved_computing_resource)
        Gb = np.array([self.global_computing_resource[i] - (self.reserved_computing_resource[i] +self.u * float(self.vehicle_density[i])) for i in range(self.b)])
        return Gb

    def get_Ntr(self,num):
        '''
        range from (0:10]
        @return: Ntr
        '''
        return np.array([num])

    def get_normalized_utilization(self,Ib,task):
        '''
        @return: normalization_utilization
        '''
        print("delay of task:",task.delay)
        difference1 = self.Tn[Ib] - task.delay
        print("difference",difference1)
        if difference1 < 0:
            result = 0
        else:
            result= np.log(1 + difference1)/np.log(1 + self.Tn[Ib])
        print("normalized_utility:",result)
        return result

    def update_compute_efficiency(self, Ib,normalized_utilization):
        '''
        update the compute efficaiency according to normalized utility and previous compute efficiency
        @return:
        '''
        self.computing_efficiency[Ib] = (1 - self.omega1) * self.computing_efficiency[Ib] + self.omega1*normalized_utilization
        print("Compute efficiency of "+str(Ib)+":",self.computing_efficiency[Ib])
        return

    def update_completion_ratio(self,Ib,done_status):
        print("task_done_status:",done_status)
        if done_status==1:
            # print("done")
            one =1
        else: 
            # print("undone")
            one=0
        self.completion_ratio[Ib] = self.total_received_task[Ib]*self.completion_ratio[Ib]+one/(self.total_received_task[Ib]+1)
        self.total_received_task[Ib]+=1
        return

    def get_reliability(self, Ib):
        self.reliability[Ib]= self.omega2 * self.computing_efficiency[Ib] + (1 - self.omega1) * self.computing_efficiency[Ib]
        print("reliability of "+str(Ib)+":",self.reliability[Ib])
        return

    def initialize_state_space(self):
        tasks = self.taskIt.selectAllTasks()
        self.Ntr = self.get_Ntr(2)
        self.vehicle_density = np.array([tasks[-1].vehicle_density[i+1] for i in range(self.b)])
        self.Gb = self.get_Gb()
        for task in tasks:
            Ib = int(task.allocation_basestation_id)-1
            #update state 2
            normalized_utilization=self.get_normalized_utilization(Ib,task)
            print("normalized_utilization",normalized_utilization)
            self.update_compute_efficiency(Ib,normalized_utilization)
            self.update_completion_ratio(Ib,task.done_status)
            self.get_reliability(Ib)
            #save the state to the basestation database
            print()
        return
        

    def get_reward(self, Ib,delay):
        Sbk = 8
        #TODO: the delay should be got from real blockchain
        if delay > self.maximum_tolerance_dalay:
            self.reward = self.gamma
        else:
            self.reward = (self.epsilon1 * self.reliability[Ib] + self.epsilon2 * Sbk / 2.0) * np.log(
                    1 + self.maximum_tolerance_dalay - delay)
        self.reward = np.float(self.reward)
        return self.reward

    def updateBSByTasks(self,tasks):
         #update state3
        self.get_Ntr(len(tasks))
        for task in tasks:
            Ib = int(task.allocation_basestation_id)-1
            #update state 1
            for i in range(self.b):
                print("vehicle_density:",task.vehicle_density)
                self.vehicle_density[i] = task.vehicle_density[i+1]
                print("task"+str(task.id)+"vehicle density near BS"+str(i)+":"+str(self.vehicle_density[i]))
            self.Gb = self.get_Gb()  # state1 global resource
            
            #update state 2
            normalized_utilization = self.get_normalized_utilization(Ib,task)
            print("normalized_utilization",normalized_utilization)
            self.update_compute_efficiency(Ib,normalized_utilization)
            self.update_completion_ratio(Ib,task.done_status)
            self.get_reliability(Ib)

            #save the state to the basestation database
        return







