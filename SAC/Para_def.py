import numpy as np
import pandas as pd
import udp_request
import pymysql
import random

class SACEnv:
    def __init__(self, s):
        self.s = s
        self.t = 1
        self.u = 0.1
        self.D_size = 3.5 * np.ones(s)
        self.C_size = 3.2 * np.ones(s)
        self.lam = -5
        self.Tn = 2 * np.ones(s)
        self.pn = 0.1
        # self.Vehicle_density = self.get_vehicle_density()
        self.t_delay = np.zeros(s)
        self.utility = np.zeros(s)
        self.Utility_task = np.zeros(s)

        self.normalized_utility = np.zeros(s)

        self.compute_efficiency = np.zeros(s)
        self.omega1 = 0.8  #range from[0,1]
        self.completion_ratio = np.zeros(s)
        self.total_received_task = np.zeros(s)
        self.omega2 = 0.8
        self.id = []
        for i in range(self.s):
            self.id.append(i)

        self.reliability = np.zeros(s)

        #simulation data
        self.Fs = np.zeros(s)
        self.rt = np.zeros(s)
        self.link_dur = self.get_link_dur()

    def get_rate(self,task_ID:str, event_ID:str, mydb):
        sql_cmd = "select * from throughput WHERE VehicleID = 'Vehicle" + task_ID + "'"
        data=pd.read_sql(sql_cmd,mydb)
        for index, row in data.iterrows():
            for n in range(self.s):
                vehicle = "Vehicle" + str(n)
                self.rt[n] = float(row[vehicle])
        print("task vehicle is:",task_ID,", event id is:", event_ID,", rate:",self.rt)
    
    def get_Fs(self, mydb):
        sql_cmd = "select * from vehicle_information"
        data=pd.read_sql(sql_cmd,mydb)
        n = 0
        for index, row in data.iterrows():
            self.Fs[n] = float(row['Fs']) * (100-float(row['utilization'])) / 100
            n += 1

    def query_reliability(self, mydb):
        sql_cmd = "select * from dataupload"
        data=pd.read_sql(sql_cmd,mydb)
        n = 0
        for index,row in data.iterrows():
            self.reliability[n] = float(row['reliability'])
            self.total_received_task[n] = float(row['total_task'])
            self.completion_ratio[n] = float(row['completion_ratio'])
            n += 1

    def set_reliability(self, mydb):
        cursor = mydb.cursor()
        for i in range(self.s):
            sql_cmd = "UPDATE dataupload SET completion_ratio = %s, reliability = %s, total_task = %s WHERE vehicleID = %s"
            input_data = (self.completion_ratio[i],self.reliability[i], self.total_received_task[i],i)
            cursor.execute(sql_cmd, input_data)
        mydb.commit()


    def get_link_dur(self):
        l_dur = 10*np.ones(self.s)
        # return np.random.uniform(2, 5,(self.s,))
        return l_dur

    def get_t_delay(self, Vs:int,t2:str):
        tde = self.D_size[Vs]/self.rt[Vs] + float(t2)
        self.t_delay[Vs] = tde
        return tde
    
    # Before receive real data from RPi, use some random data traing 200 times
    def pre_training(self, Vs:int):
        tde = self.D_size[Vs]/self.rt[Vs] + self.C_size[Vs]/self.Fs[Vs]
        self.t_delay[Vs] = tde
        return tde
    
    ''' Receive udp request and update the state space '''
    def receive_request(self, mydb):

        ''' Receive udp packet until head is "request" '''
        udp_msg, udp_addr = udp_request.receive("request")
        while udp_msg[0] != "request":
            print("Request error, error head: ",udp_msg[0])
            udp_msg, udp_addr = udp_request.receive("request")

        ''' update state space '''
        # Reload data base
        mydb.commit()
        self.D_size = float(udp_msg[3]) * np.ones(self.s)
        self.C_size = float(udp_msg[4]) * np.ones(self.s)
        self.Tn = float(udp_msg[5]) * np.ones(self.s)

        vehicle_ID = udp_msg[1]
        event_ID = udp_msg[2]
        self.get_Fs(mydb)
        self.get_rate(vehicle_ID,event_ID,mydb)
        ''' Read reliability from sql database '''
        
        self.query_reliability(mydb)
        return udp_msg, udp_addr




    def get_utility(self,Vs, tde:float):

        # self.t_delay = self.get_t_delay(Vs)
        # difference = self.Tn - self.t_delay[Vs]
        difference = self.Tn[Vs] - tde
        if difference<=0:
            self.utility[Vs] = self.lam
        else:
            self.utility[Vs] = np.log(1+difference)
        return

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

    def update_completion_ratio(self,Vs):
        one = 1 if self.t_delay[Vs]<self.Tn[Vs] else 0
        self.completion_ratio[Vs] = ((self.total_received_task[Vs])*self.completion_ratio[Vs]+one)/(self.total_received_task[Vs]+1)
        self.total_received_task[Vs] += 1
        return

    def get_reliability(self,Vs):
        self.reliability[Vs] = self.omega2 * self.compute_efficiency[Vs] + (1 - self.omega2) * self.completion_ratio[Vs]

    def cal_reliability(self,Vs,tde):
        self.get_utility(Vs,tde)
        self.get_Utility_task(Vs)
        self.get_normalized_utility(Vs)
        self.update_compute_efficiency(Vs)
        self.update_completion_ratio(Vs)
        self.get_reliability(Vs)
    
    def get_density(self,event:str, mydb):
        sql_cmd = "select BS0_DENSITY, BS1_DENSITY from ts_vehicle0 where EVENT=" + event
        data=pd.read_sql(sql_cmd,mydb)
        for index, row in data.iterrows():
            density = {'1':str(row['BS0_DENSITY']),'2':str(row['BS1_DENSITY'])}
        return density
    

            

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
