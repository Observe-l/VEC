from datetime import datetime
import gym
import gym.spaces
import numpy as np
import time
import sys
sys.path.append(".")
sys.path.append("..")
sys.path.append('/home/vec/Documents/VEC/Blockchain/')
sys.path.append("/home/vec/Documents/VEC/A2/util/")
# from model.A2ModelSQL import A2EnvExtreme
from model.A2ModelSQL import A2EnvExtreme
from model.pretrainEnv import pretrainEnv
# from util.TaskSQLUtil import countAll,getFirstId,getLastId
from util.BSSQLUtil import *
from anchornode_select import anchornode_selection
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
        self.iteration=0
        self.flag = 1 #pretrain flag
        print("(init)")
        self.reset()

    def reset(self):
        '''
        reset the state of the environment
        @return: state
        '''
        if self.iteration<5000:
            self.base_station = pretrainEnv()
            print("(reset) pretrain iteration=",self.iteration)
        else:
            self.flag = 0
            self.base_station = A2EnvExtreme()   #Load the data from the dataset
            self.begin_time =datetime.now().strftime('%Y%m%d%H%M%S')
            print("(reset) iteration=",self.iteration)
        print([self.base_station.Gb,self.base_station.reliability,self.base_station.Ntr])
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
        #print the base station chosen        # change the anchornode
        print("(Step)In iteration "+str(self.iteration)+", the consensus node chosen is:",action)
         # change the anchornode
        V_delay = anchornode_selection(action)
        reward = self.base_station.get_reward(action,V_delay)
        # reward = self.base_station.get_reward(action)
        #pretrain the model
        if self.flag==1:
            num = np.random.randint(0,5)
            self.base_station.updataBSByTasks(num)
        else:
            # wait for the blockchain to add data
            while True:
                time.sleep(2)
                self.end_time = datetime.now().strftime('%Y%m%d%H%M%S')
                tI=taskInteraction()
                new_tasks = tI.selectLatest(self.begin_time,self.end_time)
                if new_tasks!=0:
                    print("(Step)add task num:", len(new_tasks))
                    self.begin_time=self.end_time
                    # update the base station database if there exists update
                    self.base_station.updateBSByTasks(new_tasks)
                    break
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




