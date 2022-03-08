import random
import struct
import gym
import gym.spaces
import numpy as np
import udp_request
from Para_def import SACEnv
from time import time
import pymysql

import TaskSQLUtil as TaskSQLUtil
from Task import Task

mydb = pymysql.connect(
  host="192.168.1.117",
  user="VEC",
  password="666888",
  database="SAC"
)
mycursor = mydb.cursor()

class VECEnv(gym.Env):
    def __init__(self,env_config):
        self.s = 4
        self.a = 0

        self.action_space = gym.spaces.Discrete(self.s)
        observation_array_min = np.append([0.0 for i in range(self.s)], [0.0 for i in range(self.s)])
        observation_array_min = np.append(observation_array_min, [0.0 for i in range(self.s)])
        observation_array_min = np.append(observation_array_min, [0.0 for i in range(self.s)])
        observation_array_min = np.append(observation_array_min, [0.0 for i in range(self.s)])
        observation_array_min = np.append(observation_array_min, [0.0 for i in range(self.s)])
        observation_array_min = np.append(observation_array_min, [0.0 for i in range(self.s)])
        observation_array_max = np.append([100.5 for i in range(self.s)], [10.0 for i in range(self.s)])
        observation_array_max = np.append(observation_array_max, [100.0 for i in range(self.s)])
        observation_array_max = np.append(observation_array_max, [100.0 for i in range(self.s)])
        observation_array_max = np.append(observation_array_max, [100.0 for i in range(self.s)])
        observation_array_max = np.append(observation_array_max, [10.0 for i in range(self.s)])
        observation_array_max = np.append(observation_array_max, [100.0 for i in range(self.s)])
        self.observation_space = gym.spaces.box.Box(observation_array_min, observation_array_max, dtype=np.float32)
        self.base_station = SACEnv(self.s)
        # base station ID
        self.bs_ID = '2'

        # iteration
        self.iteration = 0
        self.udp_status = 0
        self.train_step = 100
        # self.reset()

    def reset(self):
        '''
        reset the state of the environment
        @return: state
        '''
        print("iteration times:",self.iteration)
        '''
        Receive request from Raspberry.#reset = #step + 1
        Pre-training 200 times
        '''
        if self.iteration > 500:
            self.udp_status = 1
            self.train_step = 0
            start = time()
            mydb.commit()
            end = time()
            print("commit time: ",end-start)
            self.msg, self.addr = udp_request.receive()
            '''
            Request head should be "request". Otherwise, program will exit and print error head packet.
            '''
            if self.msg[0] != "request":
                print("Request error, error head: ",self.msg[0])
                exit(1)

            #Update the state space
            self.base_station.D_size = float(self.msg[3]) * np.ones(self.s)
            self.base_station.C_size = float(self.msg[4]) * np.ones(self.s)
            self.base_station.Tn = float(self.msg[5]) * np.ones(self.s)
            # Time stamp - when receive the udp request
            self.start_time = time()

        # self.observation = np.hstack([self.base_station.Fs,self.base_station.snr,self.base_station.link_dur,self.base_station.reliability,self.base_station.C_size,self.base_station.D_size,self.base_station.t_delay])
        self.observation = np.concatenate([self.base_station.Fs,self.base_station.snr,self.base_station.link_dur,self.base_station.reliability,self.base_station.C_size,self.base_station.D_size,self.base_station.Tn])
        self.done = False
        
        self.step_num = 1

        return self.observation

    def step(self,action)->tuple:
        '''
        step in env
        @param action: take action selected by agent(range from[0,num of base station],Sbk)
        @return: tuple of (observation, reward, done, info)
        '''
        # update the state of chosen base station
        # self.base_station.update_reliability(action[0])

        if self.udp_status == 1:
            '''
            Real traing. Get task vehicle ID and event ID from UDP message.
            '''
            vehicle_ID = self.msg[1]
            event_ID = self.msg[2]
            
            self.end_time = time()
            SAC_time = self.end_time - self.start_time
            
            # Return the action to the task vehicle.
            action_msg = struct.pack("!i10s10s",2,b"offloading",str(action).encode())
            udp_request.send(action_msg, self.addr)
            # Vehicle will return a "complete" packet
            self.msg, self.addr = udp_request.receive()
            if self.msg[0] != "complete":
                print("Complete packet error, error head: ",self.msg[0])
                exit(1)
            t2 = self.msg[2]
            tde = self.base_station.get_t_delay(action,vehicle_ID,event_ID,t2,mydb)
            density = self.base_station.get_density(event_ID, mydb)
            if tde > self.base_station.Tn[action]:
                complete_status = '0'
            else:
                complete_status = '1'
            com_task = Task('1',vehicle_ID,str(action),self.bs_ID,complete_status,density,SAC_time)
            TaskSQLUtil.insert(com_task)
            # TaskSQLUtil.insert(com_task)
        else:
            '''
            Pre-training 200 times
            '''
            vehicle_ID = random.randint(0,3)
            event_ID = random.randint(1,14)
            tde = self.base_station.pre_training(action,str(vehicle_ID),str(event_ID),mydb)

            
        self.base_station.get_utility(action,tde)
        self.base_station.get_Utility_task(action)
        self.base_station.get_normalized_utility(action)
        self.base_station.update_completion_ratio(action)
        self.base_station.update_compute_efficiency(action)
        self.base_station.update_reliability(action) 

        self.step_num+=1
        self.iteration += 1

        reward=self.base_station.get_reward(action)
        if self.step_num>self.train_step:
            self.done = True
        self.observation = np.concatenate([self.base_station.Fs,self.base_station.snr,self.base_station.link_dur,self.base_station.reliability,self.base_station.C_size,self.base_station.D_size,self.base_station.Tn])
        
        if self.done == True and self.udp_status == 1:
            for i in range(self.s):
                sql1 = "UPDATE dataupload SET completion_ratio = %s, reliability = %s WHERE vehicleID = %s"
                input_data1 = (self.base_station.completion_ratio[i],self.base_station.reliability[i], i)
                mycursor.execute(sql1, input_data1)
                sql2 = "UPDATE dataupload SET reliability = %s WHERE vehicleID = %s"
                input_data2 = (self.base_station.reliability[i], i)
                mycursor.execute(sql2, input_data2)
                print("update to vehilce:",i)
                print("rebiability is:",self.base_station.reliability)

        print("Action is", action)
        return self.observation,reward,self.done,{}



    def render(self,mode='human'):
        pass


if __name__ == '__main__':
    env = VECEnv()
    env.reset()




