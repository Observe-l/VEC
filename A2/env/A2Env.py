from datetime import datetime
import gym
import gym.spaces
import numpy as np
import time
import sys
sys.path.append("..")
# from model.A2ModelSQL import A2EnvExtreme
from model.A2ModelSQL import A2EnvExtreme
from model.pretrainEnv import pretrainEnv
# from util.TaskSQLUtil import countAll,getFirstId,getLastId
from util.BSSQLUtil import *
from Blockchain.anchornode_select import anchornode_selection
from util.Taskinteraction import taskInteraction

class A2Env(gym.Env):
    def __init__(self,env_config):
        # dimension = 2*self.b+1
        # self.action_space = gym.spaces.Tuple([Discrete(self.b),Discrete(40)])
        # self.action_space = gym.spaces.MultiDiscrete([self.b,40])
        self.b=2  #number of base station
        self.action_space = gym.spaces.Discrete(self.b)
        observation_array_min = np.append([0.0 for i in range(self.b)],[0.0 for i in range(self.b)])
        observation_array_min = np.append(observation_array_min,[0.0])
        observation_array_max = np.append([100.5 for i in range(self.b)],[10.0 for i in range(self.b)])
        observation_array_max = np.append(observation_array_max,[10.0])
        self.observation_space = gym.spaces.box.Box(observation_array_min,observation_array_max,dtype=np.float32)
        # TODO:add reset the task table
        self.task_id=getFirstId()
        self.iteration=0
        print("(Init)initial task id:",self.task_id)
        self.reset()

    def reset(self):
        '''
        reset the state of the environment
        @return: state
        '''
        if self.iteration<2000:


        
        self.base_station = A2EnvExtreme()   #Load the data from the dataset
        self.observation = np.concatenate([self.base_station.Gb,self.base_station.reliability,self.base_station.Ntr])
        self.done = False
        self.step_num = 0
        self.begin_time = taskInteraction.getNowTimestamp()

        return self.observation

    def step(self,action)->tuple:
        '''
        step in env
        @param action: take action selected by agent(range from[0,num of base station],Sbk)
        @return: tuple of (observation, reward, done, info)
        '''
        #pretrain the model
        
        #print the base station chosen
        reward = self.base_station.get_reward(action)
        # change the anchornode
        anchornode_selection(action)
        print("(Step)In iteration "+str(self.iteration)+", the consensus node chosen is:",action)
        # wait for the sql to add data
        while True:
            time.sleep(2)
            self.end_time = taskInteraction.getNowTimestamp()
            new_tasks = taskInteraction.selectLatest(self.begin_time,self.end_time)
            if len(new_tasks)!=0:
                print("(Step)add task num:", len(new_tasks))
                # update the base station database if there exists update
                self.base_station.updateBSByTasks(new_tasks)
            break
        self.observation = np.concatenate([self.base_station.Gb, self.base_station.reliability, self.base_station.Ntr])
        # reward=self.base_station.get_reward(action[0],action[1])
              #update the state of chosen base station
        #update the step number:iteration number=1
        self.step_num += 1
        if self.step_num > 100:
            self.done = True
        self.observation = np.concatenate([self.base_station.Gb, self.base_station.reliability, self.base_station.Ntr])
        self.iteration+=1
        return self.observation,reward,self.done,{}



    def render(self):
        print("Render flag")
        return




