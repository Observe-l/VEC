import numpy as np
import pandas as pd
import pymysql
import random
import sys


# mydb = pymysql.connect(
#   host="localhost",
#   user="VEC",
#   password="666888",
#   database="SAC"
# )

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
        self.D_size = 3.5 * np.ones(s)
        self.C_size = 3.2 * np.ones(s)
        self.lam = -10
        self.Tn = 10 * np.ones(s)
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
        self.Fs = np.zeros(s)
        self.rt = np.zeros(s)
        self.link_dur = self.get_link_dur()

    def get_rate(self,task_ID:str, event_ID:str, mydb):
        table = "ts_vehicle" + task_ID
        sql_cmd = "select * from " + table + " WHERE EVENT = " + event_ID
        data=pd.read_sql(sql_cmd,mydb)
        for index, row in data.iterrows():
            for n in range(self.s):
                if n == int(task_ID):
                    self.rt[0] = 99999999999
                else:
                    vehicle = "VEHICLE" + str(n)
                    self.rt[n] = float(row[vehicle])

        return np.random.uniform(1, 6,(self.s,))
    
    def get_Fs(self, mydb):
        sql_cmd = "select * from vehicle_information"
        data=pd.read_sql(sql_cmd,mydb)
        n = 0
        for index, row in data.iterrows():
            self.Fs[n] = float(row['Fs']) * float(row['utilization'])
            n += 1

    def get_link_dur(self):
        l_dur = [10,10,10,10]
        # return np.random.uniform(2, 5,(self.s,))
        return l_dur

    def get_t_delay(self, Vs:int,t2:str):
        tde = self.D_size[Vs]/self.rt + float(t2)
        self.t_delay[Vs] = tde
        return tde
    
    # Before receive real data from RPi, use some random data traing 200 times
    def pre_training(self, Vs:int):
        tde = self.D_size[Vs]/self.rt + self.C_size[Vs]/self.Fs[Vs]
        self.t_delay[Vs] = tde
        return tde



    def get_utility(self,Vs, tde:float):

        # self.t_delay = self.get_t_delay(Vs)
        # difference = self.Tn - self.t_delay[Vs]
        difference = self.Tn[Vs] - tde
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
        if self.Tn[Vs] > self.t_delay[Vs]:
            self.normalized_utility[Vs] = np.log(1 + self.Tn[Vs]-self.t_delay[Vs])/np.log(1 + self.Tn[Vs])
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
        one = 1 if self.t_delay[Vs]<self.Tn[Vs] else 0
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
    
    def get_density(self,event:str, mydb):
        sql_cmd = "select BS0_DENSITY, BS1_DENSITY from ts_vehicle0 where EVENT=" + event
        data=pd.read_sql(sql_cmd,mydb)
        for index, row in data.iterrows():
            density = {'1':str(row['BS0_DENSITY']),'2':str(row['BS1_DENSITY'])}
        return density
    
    def insert_relibility(self, length: int, mydb):
        cursor = mydb.cursor()
        sql1 = "UPDATE dataupload SET completion_ratio = %s WHERE vehicleID = %s"
        sql2 = "UPDATE dataupload SET reliability = %s WHERE vehicleID = %s"
        for i in range(0,length):
            input_data1 = (self.completion_ratio[i],i)
            input_data2 = (self.reliability[i],i)
            cursor.execute(sql1, input_data1)
            cursor.execute(sql2, input_data2)
        mydb.commit()
            

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