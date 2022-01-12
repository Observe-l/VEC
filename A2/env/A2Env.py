import gym
import gym.spaces
import numpy as np
# from model.A2ModelSQL import A2EnvSQL
from model.A2ModelExtreme import A2EnvExtreme

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
        #update the state of chosen base station
        self.base_station.update_reliability(action)
        self.base_station.get_Ntr()
        self.base_station.get_Gb()
        # print("last state:",self.observation[0]-action)
        # print("action",action)
        # print("state:",self.observation[0])
        self.step_num+=1
        # reward=self.base_station.get_reward(action[0],action[1])
        reward=self.base_station.get_reward(action)
        if self.step_num>100:
            self.done=True
        self.observation = np.concatenate([self.base_station.Gb,self.base_station.reliability,self.base_station.Ntr])
        return self.observation,reward,self.done,{}



    def render(self,mode='human'):
        pass





