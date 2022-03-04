import gym
import gym.spaces
import numpy as np
import udp_request
from Para_def import SACEnv
from time import time
import mysql.connector

import sys
sys.path.append("..")
import A2.util.TaskSQLUtil as TaskSQLUtil
from A2.util.Task import Task

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
        self.request = 0
        # self.reset()

    def reset(self):
        '''
        reset the state of the environment
        @return: state
        '''
        self.base_station = SACEnv(self.s)
        # self.observation = np.hstack([self.base_station.Fs,self.base_station.snr,self.base_station.link_dur,self.base_station.reliability,self.base_station.C_size,self.base_station.D_size,self.base_station.t_delay])
        self.observation = np.concatenate([self.base_station.Fs,self.base_station.snr,self.base_station.link_dur,self.base_station.reliability,self.base_station.C_size,self.base_station.D_size,self.base_station.t_delay])
        self.done = False
        self.step_num = 0

        '''
        Receive request from Raspberry.#reset = #step + 1
        '''
        if self.request == 1:
            self.msg, self.addr = udp_request.udp_server()
            # Time stamp - when receive the udp request
            self.start_time = time()
        else:
            self.request =1

        return self.observation

    def step(self,action)->tuple:
        '''
        step in env
        @param action: take action selected by agent(range from[0,num of base station],Sbk)
        @return: tuple of (observation, reward, done, info)
        '''
        #update the state of chosen base station
        # self.base_station.update_reliability(action[0])

        '''
        Request head should be "request". Otherwise, program will exit and print error head packet.
        '''
        if self.msg[0].decode().rstrip('\x00') != "request":
            print("Request error, error head: ",self.msg[0].decode().rstrip('\x00'))
            exit(1)
        '''
        Get task vehicle ID and event ID from UDP message.
        '''
        task_ID = int(self.msg[1].decode().rstrip('\x00'))
        event_ID = self.msg[2].decode().rstrip('\x00')
        Dn = self.msg[3].decode().rstrip('\x00')
        '''
        When SAC choose task vehicle as service vehicle, skip this action and return penalty
        '''
        if action == task_ID:
            self.observation = np.concatenate([self.base_station.Fs, self.base_station.snr, self.base_station.link_dur, self.base_station.reliability, self.base_station.C_size, self.base_station.D_size, self.base_station.t_delay])
            reward = -1000
            self.done = False
            udp_request.udp_send("skip","none","none","none",self.addr[0])
        else:
            # Time stamp - when SAC choose a action
            self.end_time = time()
            SAC_time = self.end_time - self.start_time
            # Transmite ID, event, etc. to get_t_delay function
            udp_request.udp_send("offloading","action","file_name","Task_name",self.addr[0])

            tde = self.base_station.get_t_delay(action,task_ID,event_ID,Dn)
            self.base_station.get_utility(action,tde)
            self.base_station.get_Utility_task(action)
            self.base_station.get_normalized_utility(action)
            self.base_station.update_completion_ratio(action)
            self.base_station.update_compute_efficiency(action)
            self.base_station.update_reliability(action)
            density = self.base_station.get_density(event_ID)
            com_task = Task('1',task_ID,str(action),'1','1',density,SAC_time)
            TaskSQLUtil.insert(com_task)
            # print("last state:",self.observation[0]-action)
            # print("action", action)
            # print(self.base_station.get_t_delay(action))
            # print("state:",self.observation[0])
            self.step_num+=1
            # print(self.step_num)
            # reward=self.base_station.get_reward(action[0],action[1])
            reward=self.base_station.get_reward(action)
            if self.step_num>100:
                self.done = True
            self.observation = np.concatenate([self.base_station.Fs,self.base_station.snr,self.base_station.link_dur,self.base_station.reliability,self.base_station.C_size,self.base_station.D_size,self.base_station.t_delay])
            if self.done == True:
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="zequn",
                    password="666888",
                    database="SAC"
                )
                mycursor = mydb.cursor()
                while self.a < self.s:
                    sql1 = "UPDATE dataupload SET completion_ratio = %s WHERE vehicleID = %s"
                    input_data1 = (self.base_station.completion_ratio[self.a], self.a)
                    mycursor.execute(sql1, input_data1)
                    sql2 = "UPDATE dataupload SET reliability = %s WHERE vehicleID = %s"
                    input_data2 = (self.base_station.reliability[self.a], self.a)
                    mycursor.execute(sql2, input_data2)
                    mydb.commit()
                    self.a += 1

        return self.observation,reward,self.done,{}



    def render(self,mode='human'):
        pass


if __name__ == '__main__':
    env = VECEnv()
    env.reset()




