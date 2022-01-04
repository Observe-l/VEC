import random
import gym
import gym.spaces
import numpy as np
import traceback
import pprint

class GridEnv(gym.Env):
    def __init__(self,env_config):
        self.action_space = gym.spaces.Discrete(2)
        # self.observation_space=gym.spaces.Box(np.array([0]),np.array([9]),dtype=int)
        self.observation_space=gym.spaces.Box(np.array([0]),np.array([9]),dtype=int)
        self.reset()



    def reset(self):
        '''
        reset the state of theenvironment
        @return: state
        '''
        self.observation = [0]
        self.done = False
        self.step_num = 0
        return [0]

    def step(self,action)->tuple:
        '''
        step in env
        @param action: take action selected by agent
        @return: tuple of (observation, reward, done, info)
        '''
        if action==0:
            action=-1
        self.observation[0]+=action
        # print("last state:",self.observation[0]-action)
        # print("action",action)
        # print("state:",self.observation[0])
        self.step_num+=1
        reward=-1
        if self.step_num>100 or self.observation[0]<0:
            reward = -100
            self.done=True
            return self.observation,reward,self.done,{}

        if self.observation[0]==9:
            reward=100
            self.done=True

        return self.observation,reward,self.done,{}


    def render(self,mode='human'):
        pass

