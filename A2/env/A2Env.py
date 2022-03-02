import gym
import gym.spaces
import numpy as np
import time
from A2.model.A2ModelSQL import A2EnvExtreme
# from A2.model.A2ModelExtreme import A2EnvExtreme
from A2.util.TaskSQLUtil import countAll
from A2.util.BSSQLUtil import *

class A2Env(gym.Env):
    def __init__(self,env_config):
        # dimension = 2*self.b+1
        # self.action_space = gym.spaces.Tuple([Discrete(self.b),Discrete(40)])
        # self.action_space = gym.spaces.MultiDiscrete([self.b,40])
        self.b=2 #number of base station
        self.action_space = gym.spaces.Discrete(self.b)
        observation_array_min = np.append([0.0 for i in range(self.b)],[0.0 for i in range(self.b)])
        observation_array_min = np.append(observation_array_min,[0.0])
        observation_array_max = np.append([100.5 for i in range(self.b)],[10.0 for i in range(self.b)])
        observation_array_max = np.append(observation_array_max,[10.0])
        self.observation_space = gym.spaces.box.Box(observation_array_min,observation_array_max,dtype=np.float32)
        self.reset()
        # TODO:add reset the task table
        self.task_num=0

    def reset(self):
        '''
        reset the state of the environment
        @return: state
        '''

        #wait for the sql to add data
        while True:
            time.sleep(2)
            #count the total number of tasks
            temp_task_num = countAll()
            #load the number of tasks
            # update the base station database if there exists update
            if temp_task_num!=self.task_num:
                diff = temp_task_num-self.task_num
                self.task_num=temp_task_num
                self.base_station.updateBSByTasks(diff)
                break

        self.base_station = A2EnvExtreme()   #Load the data from the dataset
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

        self.observation = np.concatenate([self.base_station.Gb, self.base_station.reliability, self.base_station.Ntr])
        # reward=self.base_station.get_reward(action[0],action[1])
              #update the state of chosen base station
        self.base_station.get_Ntr()
        reward = self.base_station.get_reward(action)
        #update the step number:iteration number=1
        self.step_num += 1
        if self.step_num > 0:
            self.done = True
        self.observation = np.concatenate([self.base_station.Gb, self.base_station.reliability, self.base_station.Ntr])

        return self.observation,reward,self.done,{}



    def render(self,mode='human'):
        pass





