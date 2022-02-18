from A2.util.BSSQLUtil import *
import numpy as np
from A2.util.BaseStationTransfer import *
import numpy as np

"""
In order to verify whether the of the agent is right or not, we set two base station where one is most possble
and another is most impossible. Both the data of these two base station is constant. 
"""
class A2EnvExtreme():
    def __init__(self):
        #reset basestation
        resetDB()
        #get the basestation model
        baseStationsDF = selectAll()
        self.baseStations = BSDF2BS(baseStationsDF)
        self.b = len(self.baseStations)       #number of base station
        self.u = 0.1
        self.G_total = np.array([self.baseStations[i].global_computing_resource for i in range(self.b)])
        self.Gb_bar = np.array([self.baseStations[i].reversed_computing_resource for i in range(self.b)])
        self.Vehicle_density = self.get_vehicle_density()
        self.Gb = self.get_Gb()  #state1 global resource
        self.Ntr = self.get_Ntr()    #state2 transactions generated by BSs

        self.Tn = 10 #maximun tolerance delay
        self.compute_efficiency =  np.array([self.baseStations[i].computing_efficiency for i in range(self.b)])
        self.omega1 = 0.2  #range from[0,1]
        self.completion_ratio = np.array([self.baseStations[i].completion_ratio for i in range(self.b)])
        self.total_received_task = np.array([self.baseStations[i].total_received_task for i in range(self.b)])
        self.omega2 = 0.2
        # self.reliability = self.get_reliability() #state3 reliability
        self.normalized_utility = np.zeros(self.b)
        self.t_delay = np.zeros(self.b)
        self.reliability = np.array([self.baseStations[i].total_received_task for i in range(self.b)])

        #action parameters
        self.maximum_block_size = 40 #40/5=8

        #reward parameters
        self.epsilon1 = 0.4
        self.epsilon2 = 0.6
        self.maximum_tolerance_dalay = 20
        self.gamma = -1
        self.reward = 0



    def get_vehicle_density(self):
        '''
        range from[5.0,40.0]
        @param b: the number of station
        @return: the density of vehicle around each base station
        '''
        return np.random.uniform(5, 40, (self.b))

    def get_Gb(self):
        '''
        @return: available computing resource
        '''
        Gb =self.G_total-(self.Gb_bar+self.u*self.Vehicle_density)
        return Gb

    def get_Ntr(self):
        '''
        range from (0:10]
        @return: Ntr
        '''
        return np.zeros(1)

    def update_Ntr(self):
        self.Ntr[0]+=np.random.randint(2,5)
        return

    def get_t_delay(self):
        '''
        range from[0.1,11]
        @param b: the number of station
        @return: the delay of base station
        '''
        return np.random.uniform(0.1, 11)


    def get_normalized_utilization(self,Ib):
        '''
        @return: normalization_utilization
        '''
        self.t_delay[Ib] = self.get_t_delay()
        difference = self.Tn-self.t_delay[Ib]
        if difference<0:
            self.normalized_utility[Ib]=0
        else:
            self.normalized_utility[Ib] = np.log(1+difference)/np.log(1+self.Tn)
        return

    def update_compute_efficiency(self,Ib):
        '''
        update the compute efficaiency according to normalized utility and previous compute efficiency
        @return:
        '''
        self.compute_efficiency[Ib] = (1-self.omega1)*self.compute_efficiency[Ib]+self.omega1*self.normalized_utility[Ib]
        #update the data in database
        self.baseStations[Ib].computing_efficiency = self.compute_efficiency[Ib]
        update(self.baseStations[Ib])
        return


    def update_total_received(self,Ib):
        self.total_received_task[Ib]+=1
        self.baseStations[Ib].total_received_task = self.total_received_task[Ib]
        update(self.baseStations[Ib])
        return


    def update_completion_ratio(self,Ib):
        one = 1 if self.t_delay[Ib]<self.Tn else 0
        self.update_total_received(Ib)
        self.completion_ratio[Ib] = ((self.total_received_task[Ib])*self.completion_ratio[Ib]+one)/self.total_received_task[Ib]
        self.baseStations[Ib].completion_ratio = self.completion_ratio[Ib]
        update(self.baseStations[Ib])
        return

    def get_reliability(self,Ib):
        result = self.omega2 * self.compute_efficiency[Ib] + (1 - self.omega1) * self.completion_ratio[Ib]
        return result

    def update_reliability(self,Ib):
        self.get_normalized_utilization(Ib)
        self.update_compute_efficiency(Ib)
        self.update_completion_ratio(Ib)
        self.reliability[Ib] = self.get_reliability(Ib)
        self.baseStations[Ib].reliability = self.reliability[Ib]
        update(self.baseStations[Ib])
        return

    def get_verify_time(self):
        return np.array([21,10])

    # def get_reward(self,Ib,Sbk):
    def get_reward(self,Ib):
        Sbk=8
        delay = self.get_verify_time()
        if delay>self.maximum_tolerance_dalay:
            self.reward=0
        else:
            self.reward=(self.epsilon1*self.reliability[Ib]+self.epsilon2*Sbk/2)*np.log(1+self.maximum_tolerance_dalay-delay)
        return self.reward


if __name__ == '__main__':
    #vailable computing resource
    env = A2EnvExtreme()
    print(env.Gb)
    print(env.Ntr)
    print(env.reliability)

