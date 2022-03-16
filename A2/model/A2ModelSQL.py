from util.BSSQLUtil import *
from util.BaseStation import *
import numpy as np
from util.BaseStationTransfer import *
from util.TaskSQLUtil import *

import numpy as np


class A2EnvExtreme:
    def __init__(self):
        
        # get the basestation model
        baseStationsDF = selectAll()
        self.baseStations = BSDF2BS(baseStationsDF)
        self.b = len(self.baseStations)  # number of base station
        self.u = 0.1

        # state1 global resource
        self.Gb = self.get_Gb()  # state1 global resource

        # state2 reliability
        self.Tn = [4,4] #maximun tolerance delay
         # get from zequn
        self.omega1 = 0.8  # range from[0,1]
        self.omega2 = 0.8
        self.reliability = np.array([self.baseStations[i].reliability for i in range(self.b)])

        # state3 transactions generated by BSs
        self.Ntr = self.get_Ntr(0)

        # action parameters
        self.maximum_block_size = 10  # 10/5=2

        # reward parameters
        self.epsilon1 = 0.4
        self.epsilon2 = 0.6
        self.maximum_tolerance_dalay = 20
        self.gamma = -1
        self.reward = 0

    def get_Gb(self):
        '''
        @return: available computing resource
        '''
        print(self.baseStations[0].vehicle_density)
        Gb = np.array([self.baseStations[i].global_computing_resource - (self.baseStations[i].reserved_computing_resource +self.u * float(self.baseStations[i].vehicle_density)) for i in range(self.b)])
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
        difference = self.Tn[Ib] - task.delay
        if difference < 0:
            normalized_utility = 0
        else:
            normalized_utility = np.log(1 + difference) / np.log(1 + self.Tn[Ib])
        return normalized_utility

    def update_compute_efficiency(self, Ib,normalized_utilization):
        '''
        update the compute efficaiency according to normalized utility and previous compute efficiency
        @return:
        '''
        self.baseStations[Ib].computing_efficiency = (1 - self.omega1) * self.baseStations[Ib].computing_efficiency + self.omega1 * \
                                      normalized_utilization

        return

    def update_completion_ratio(self, Ib):
        self.baseStations[Ib].total_received_task = countAllByBS(Ib)
        num_done = countDoneByBS(Ib)
        if self.baseStations[Ib].total_received_task==0:
            self.baseStations[Ib].completion_ratio=0
            return
        self.baseStations[Ib].completion_ratio = num_done/self.baseStations[Ib].total_received_task
        return

    def get_reliability(self, Ib):
        result = self.omega2 * self.baseStations[Ib].computing_efficiency + (1 - self.omega1) * self.baseStations[Ib].computing_efficiency
        self.baseStations[Ib].reliability = result
        self.reliability[Ib]=result
        return


    def get_verify_time1(self):
        return np.random.uniform(15, 30)

    def get_verify_time2(self):
        return np.random.uniform(10, 21)


    def get_reward(self, Ib):
        Sbk = 8
        #TODO: the delay should be got from real blockchain
        if Ib == 0:
            delay = self.get_verify_time1()
        else:
            delay = self.get_verify_time2()
        if delay > self.maximum_tolerance_dalay:
            self.reward = -5
        else:
            self.reward = (self.epsilon1 * self.baseStations[Ib].reliability + self.epsilon2 * Sbk / 2.0) * (
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
                self.baseStations[i].vehicle_density = task.vehicle_density[str(i+1)]
                print("task"+str(task.id)+"vehicle density near BS"+str(i)+":"+str(self.baseStations[i].vehicle_density))
            self.Gb = self.get_Gb()  # state1 global resource
            
            #update state 2
            normalized_utilization = self.get_normalized_utilization(Ib,task)
            self.update_compute_efficiency(Ib,normalized_utilization)
            self.update_completion_ratio(Ib)
            self.get_reliability(Ib)

            #save the state to the basestation database
            update(self.baseStations[Ib])
        return



