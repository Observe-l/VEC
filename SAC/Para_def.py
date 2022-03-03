import numpy as np
import pandas as pd
import pymysql
import random

mydb = pymysql.connect(
  host="localhost",
  user="zequn",
  password="666888",
  database="SAC"
)

# delaycmd = "select offloading_delay from sacenv"
compcmd = "select computation_size from sacenv"

# delaycmd = "select offloading_delay from" + table + "where timestamp = " + timestamp
# compcmd = "select computation_size from" + table + "where timestamp = " + timestamp

# tdelay = pd.read_sql(delaycmd, mydb)
# csize = pd.read_sql(compcmd, mydb)

class SACEnv:
    def __init__(self, s):
        self.s = s
        self.t = 1
        self.u = 0.1
        self.D_size = self.get_D_size()
        self.C_size = self.get_C_size()
        self.lam = -10
        self.Tn = 10
        self.pn = 0.1
        # self.Vehicle_density = self.get_vehicle_density()
        self.t_delay = np.zeros(s)
        self.utility = np.zeros(s)
        self.Utility_task = np.zeros(s)

        self.normalized_utility = np.zeros(s)

        self.compute_efficiency = np.zeros(s)
        self.omega1 = 0.2  #range from[0,1]
        self.completion_ratio = np.zeros(s)
        self.total_received_task = np.zeros(s)
        self.omega2 = 0.2
        # self.reliability = self.get_reliability()


        self.reliability = np.zeros(s)



        #simulation data
        self.Fs = self.get_Fs()
        self.snr = self.get_snr()
        self.link_dur = self.get_link_dur()

    def get_Fs(self):
        return np.random.uniform(3, 7,(self.s,))

    def get_snr(self):
        return np.random.uniform(1, 6,(self.s,))

    def get_link_dur(self):
        return np.random.uniform(2, 5,(self.s,))


    def get_C_size(self):
        # a = np.random.uniform(1, 5)
        # b = np.random.uniform(50, 60)
        # c = np.random.uniform(70, 80)
        # a1 = np.float32(a)
        # b1 = np.float32(b)
        # c1 = np.float32(c)
        # return np.array([a1, b1, c1])
        return np.random.uniform(0.2, 4, (self.s,))
        # csize = pd.read_sql(compcmd, mydb)
        # csi = np.array(csize)
        # csi1 = np.float32(csi)
        # return csi1.reshape((4,))


    def get_D_size(self):
        return np.random.uniform(0.2, 4, (self.s,))

    def get_t_delay(self, Vs):
        # a = np.random.uniform(0.1, 0.5)
        # b = np.random.uniform(5, 10)
        # c = np.random.uniform(8, 18)
        # a1 = np.float32(a)
        # b1 = np.float32(b)
        # c1 = np.float32(c)
        # return np.array([a1, b1, c1])
        # return np.random.uniform(1, 13, (self.s,))
        # tdelay = np.zeros(4)
        sv = Vs
        event = 1
        tv = 0
        datasize = 4
        vehicle = "vehicle" + str(sv)
        table = "ts_vehicle" + str(tv)
        timestamp = str(event)
        delaycmd = "select " + vehicle + " from " + table + " WHERE EVENT = " + timestamp
        transmission = np.float32(pd.read_sql(delaycmd, mydb))
        tde = datasize/transmission
        self.t_delay[Vs] = tde
        # tde = np.array(tdelay)
        # tde1 = np.float32(tde)
        # return tde1.reshape((4,))
        return self.t_delay

    def get_utility(self,Vs):

        self.t_delay = self.get_t_delay(Vs)
        difference = self.Tn - self.t_delay[Vs]
        if difference<=0:
            self.utility[Vs] = self.lam
        else:
            self.utility[Vs] = np.log(1+difference)
        return

    # def get_vehicle_density(self):
    #     return np.random.uniform(5, 40)

    def get_Utility_task(self,Vs):
        self.Utility_task[Vs] = self.utility[Vs] - self.pn * self.C_size[Vs]
        return self.Utility_task[Vs]

    def get_normalized_utility(self,Vs):
        if self.Tn > self.t_delay[Vs]:
            self.normalized_utility[Vs] = np.log(1 + self.Tn-self.t_delay[Vs])/np.log(1 + self.Tn)
        else:
            self.normalized_utility[Vs] = 0
        return self.normalized_utility

    def update_compute_efficiency(self,Vs):
        self.compute_efficiency[Vs] = (1-self.omega1)*self.compute_efficiency[Vs]+self.omega1*self.normalized_utility[Vs]
        return

    def update_total_received(self,Vs):
        self.total_received_task[Vs]+=1
        return

    def update_completion_ratio(self,Vs):
        one = 1 if self.t_delay[Vs]<self.Tn else 0
        self.total_received_task[Vs] += 1
        self.completion_ratio[Vs] = ((self.total_received_task[Vs])*self.completion_ratio[Vs]+one)/self.total_received_task[Vs]
        return

    def get_reliability(self,Vs):
        result = self.omega2 * self.compute_efficiency[Vs] + (1 - self.omega2) * self.completion_ratio[Vs]
        return result

    def update_reliability(self,Vs):
        self.get_normalized_utility(Vs)
        self.update_compute_efficiency(Vs)
        self.update_completion_ratio(Vs)
        self.reliability[Vs] = self.get_reliability(Vs)
        return

    def get_reward(self,Vs):
        self.reward = self.Utility_task[Vs]
        return self.reward


if __name__ == '__main__':
    #vailable computing resource
    s = 4
    bs = SACEnv(s)
    # print(bs.Fs)
    # print(bs.snr)
    # print(bs.link_dur)
    # print(bs.reliability)
    d = bs.C_size.reshape((4,))
    print(bs.D_size)
    print(bs.C_size)
    print(bs.get_t_delay(1))




    # i = 1
    # while i <= 1000:
    #     bs.get_utility(2)
    #     u=bs.get_Utility_task(2)
    #     print(u)
    #     i =+ 1