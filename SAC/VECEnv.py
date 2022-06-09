import random
import struct
import gym
import gym.spaces
import numpy as np
import udp_request
from Para_def import SACEnv
from time import time
import pymysql

# import reliability
# from reliability import vehicle
# import TaskSQLUtil as TaskSQLUtil
# from Task import Task
# import A2.util.Taskinteraction
# import os, sys
# sys.path.append("/home/vec/Documents/VEC/A2/util/")
# from Taskinteraction import taskInteraction

mydb = pymysql.connect(
  host="localhost",
  user="VEC",
  password="666888",
  database="SAC"
)

class VECEnv(gym.Env):
    def __init__(self,env_config):
        self.s = 12
        self.a = 0

        self.action_space = gym.spaces.Discrete(self.s)
        observation_array_min = np.append([0.0 for i in range(self.s)], [0.0 for i in range(self.s)])
        observation_array_min = np.append(observation_array_min, [0.0 for i in range(self.s)])
        observation_array_min = np.append(observation_array_min, [0.0 for i in range(self.s)])
        observation_array_min = np.append(observation_array_min, [0.0 for i in range(self.s)])
        observation_array_min = np.append(observation_array_min, [0.0 for i in range(self.s)])
        observation_array_min = np.append(observation_array_min, [0.0 for i in range(self.s)])
        observation_array_max = np.append([100.5 for i in range(self.s)], [100.0 for i in range(self.s)])
        observation_array_max = np.append(observation_array_max, [100.0 for i in range(self.s)])
        observation_array_max = np.append(observation_array_max, [100.0 for i in range(self.s)])
        observation_array_max = np.append(observation_array_max, [100.0 for i in range(self.s)])
        observation_array_max = np.append(observation_array_max, [100.0 for i in range(self.s)])
        observation_array_max = np.append(observation_array_max, [100.0 for i in range(self.s)])
        self.observation_space = gym.spaces.box.Box(observation_array_min, observation_array_max, dtype=np.float32)
        self.base_station = SACEnv(self.s)
        # base station ID
        self.bs_ID = '0'

        # iteration
        self.iteration = 0
        # After pre-training, the real_triaining will be set to True
        self.real_training = False
        self.train_step = 100

    def reset(self):
        '''
        reset the state of the environment
        @return: state
        '''
        print("iteration times:",self.iteration)
        '''
        Receive request from Raspberry.#reset = #step + 1
        Pre-training 6000 times
        '''
        self.cal_e = time()
        if self.iteration > 5999:
            self.real_training = True
            # self.train_step = 0

            # Reload the database
            mydb.commit()

            self.msg, self.addr = udp_request.receive("request")
            '''
            Request head should be "request". Otherwise, program will exit and print error head packet.
            '''
            while self.msg[0] != "request":
                print("Request error, error head: ",self.msg[0])
                self.msg, self.addr = udp_request.receive("request")
            
            # Time stamp - when receive the udp request
            self.start_time = time()
            #Update the state space
            self.base_station.D_size = float(self.msg[3]) * np.ones(self.s)
            self.base_station.C_size = float(self.msg[4]) * np.ones(self.s)
            self.base_station.Tn = float(self.msg[5]) * np.ones(self.s)

            # Read reliability from sql database
            self.base_station.query_reliability(mydb)
            vehicle_ID = self.msg[1]
            event_ID = self.msg[2]
            
        else:
            vehicle_ID = str(random.randint(0,11))
            event_ID = "1"
            self.msg = ["request",vehicle_ID, event_ID]
    
        self.base_station.get_Fs(mydb)
        self.base_station.get_rate(vehicle_ID, event_ID, mydb)
    
        self.observation = np.concatenate([self.base_station.Fs,self.base_station.rt,self.base_station.link_dur,self.base_station.reliability,self.base_station.C_size,self.base_station.D_size,self.base_station.Tn])
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

        if self.real_training:
            '''
            Real traing. Get task vehicle ID and event ID from UDP message.
            '''
            vehicle_ID = self.msg[1]
            event_ID = self.msg[2]
            
            self.end_time = time()
            SAC_time = self.end_time - self.start_time
            
            # Return the action to the task vehicle. If send error, back to reset function
            action_msg = struct.pack("!i10s10s10s",3,b"offloading",str(action).encode(),str(self.base_station.Fs[action]).encode())
            status = udp_request.send(action_msg, self.addr)
            if status == False:
                print("Action send error")
                reward = 0
                self.done =True
                return self.observation,reward,self.done,{}

            # Vehicle will return a "complete" packet, or back to reset function
            msg, addr = udp_request.receive("complete")
            while self.addr != addr:
                print("Bad messages, it should from: ",self.addr, " but it's from: ",addr)
                msg, addr = udp_request.receive("complete")
            # Update message and address
            self.msg = msg
            self.addr = addr

            if self.msg[0] != "complete":
                print("Complete packet error, error head: ",self.msg[0])
                reward = 0
                self.done =True
                return self.observation,reward,self.done,{}

            # Get task execution time
            execution_time = self.msg[2]
            tde = self.base_station.get_t_delay(action, execution_time)

            # Read vehicle density from sql database
            # density = self.base_station.get_density(event_ID, mydb)
            if tde > self.base_station.Tn[action]:
                complete_status = '0'
            else:
                complete_status = '1'
            
            # Updata data for DDQN part
            # bc_ts = taskInteraction()
            # task_id = bc_ts.getNowTimestamp()+'bs'+self.bs_ID
            # com_task = Task(task_id,vehicle_ID,str(action),self.bs_ID,complete_status,density,SAC_time)

            # bc_ts.insert(com_task)
        else:
            '''
            Pre-training 6000 times
            '''
            tde = self.base_station.pre_training(action)

            
        # Calculate the reliability, completion ratio, etc.
        self.base_station.get_utility(action,tde)
        self.base_station.get_Utility_task(action)
        self.base_station.get_normalized_utility(action)
        self.base_station.update_compute_efficiency(action)
        self.base_station.get_reliability(action)
        # Update the data into sql database, only in real training phase
        if self.real_training:
            self.base_station.set_reliability(mydb)
        print("Task vehicle is:",self.msg[1],", Action is", action)

        # Complete one epoch
        self.step_num+=1
        self.iteration += 1
        reward=self.base_station.get_reward(action)
        if self.step_num>self.train_step:
            self.done = True

        '''There are 100 tasks in each epoch. After receive the next request, SAC will get the reward'''
        if self.done == False and self.real_training == True:
            # Reload the database
            mydb.commit()

            self.msg, self.addr = udp_request.receive("request")
            '''
            Request head should be "request". Otherwise, program will exit and print error head packet.
            '''
            while self.msg[0] != "request":
                print("Request error, error head: ",self.msg[0])
                self.msg, self.addr = udp_request.receive("request")
            
            # Time stamp - when receive the udp request
            self.start_time = time()
            #Update the state space
            self.base_station.D_size = float(self.msg[3]) * np.ones(self.s)
            self.base_station.C_size = float(self.msg[4]) * np.ones(self.s)
            self.base_station.Tn = float(self.msg[5]) * np.ones(self.s)

            # Read reliability from sql database
            self.base_station.query_reliability(mydb)
            vehicle_ID = self.msg[1]
            event_ID = self.msg[2]
            
            self.base_station.get_Fs(mydb)
            self.base_station.get_rate(vehicle_ID, event_ID, mydb)
    
        self.observation = np.concatenate([self.base_station.Fs,self.base_station.rt,self.base_station.link_dur,self.base_station.reliability,self.base_station.C_size,self.base_station.D_size,self.base_station.Tn])


        return self.observation,reward,self.done,{}



    def render(self,mode='human'):
        pass


if __name__ == '__main__':
    env = VECEnv(gym.Env)
    env.reset()




