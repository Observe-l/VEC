import gym
import gym.spaces
import numpy as np
import time
# from model.A2ModelSQL import A2EnvSQL
from A2.model.A2ModelExtreme import A2EnvExtreme
from A2.util.TaskSQLUtil import countAllByBS
from A2.util.TaskSQLUtil import countDoneByBS
from A2.util.BSSQLUtil import *

class A2Env(gym.Env):
    def __init__(self,env_config):
        # dimension = 2*self.b+1
        # self.action_space = gym.spaces.Tuple([Discrete(self.b),Discrete(40)])
        # self.action_space = gym.spaces.MultiDiscrete([self.b,40])
        self.b=2
        self.action_space = gym.spaces.Discrete(self.b)
        observation_array_min = np.append([0.0 for i in range(self.b)],[0.0 for i in range(self.b)])
        observation_array_min = np.append(observation_array_min,[0.0])
        observation_array_max = np.append([100.5 for i in range(self.b)],[10.0 for i in range(self.b)])
        observation_array_max = np.append(observation_array_max,[10.0])
        self.observation_space = gym.spaces.box.Box(observation_array_min,observation_array_max,dtype=np.float32)
        self.reset()
        # TODO:add reset the task table
        self.task_num=[0,0,0]

    def reset(self):
        '''
        reset the state of the environment
        @return: state
        '''
        self.base_station = A2EnvExtreme()
        self.observation = np.concatenate([self.base_station.Gb,self.base_station.reliability,self.base_station.Ntr])
        self.done = False
        self.step_num = 0
        return self.observation

    def step(self,action)->tuple:
        '''
        step in env
        @param action: take action selected by agent(range from[0,num of base station],Sbk)
        @return: tuple of (observation, reward, done, info)
        '''
        #print the base station chosen
        print("The base station chosen is:",action)
        result=str(action)

        with open("home/jaimin/PycharmProjects/VECSQL/result/result.txt", 'a') as file:
            file.write(result)
            file.write('\n')
            file.close()

        self.observation = np.concatenate([self.base_station.Gb, self.base_station.reliability, self.base_station.Ntr])
        # reward=self.base_station.get_reward(action[0],action[1])
        reward=self.base_station.get_reward(action)
        self.step_num += 1
        if self.step_num > 100:
            self.done = True
        self.observation = np.concatenate([self.base_station.Gb, self.base_station.reliability, self.base_station.Ntr])


        #wait for the sql to add data
        while True:
            time.sleep(2)
            temp_task_num = [0,0,0]
            len = len(self.task_num)
            #load the number of tasks
            for i in range(len):
                temp_task_num[i] = countAllByBS(i+1)
            all_list = []
            #save the list of allocation basestation
            for i in range(len):
                diff = temp_task_num[i+1] -self.task_num[i+1]
                if diff!=0:
                    all_list.append([i+1,diff])
                    self.task_num[i+1]=temp_task_num[i+1]
            # update the base station database if there is update
            if len(all_list)!=0:
                for (bs_id,num) in all_list:
                    done = countDoneByBS(bs_id)
                    bs = selectById(bs_id)
                    #update total received number
                    bs.total_received_task = self.task_num[bs_id-1]
                    #update completion ratio
                    bs.completion_ratio = done / bs.total_received_task
                    update(bs)
                    self.base_station.update_reliability(bs_id,num)
                    break
        print("Go on!")
        #update the state of chosen base station
        self.base_station.get_Ntr()
        self.base_station.get_Gb()
        # print("last state:",self.observation[0]-action)
        # print("action",action)
        # print("state:",self.observation[0])

        return self.observation,reward,self.done,{}



    def render(self,mode='human'):
        pass





