import gym
import gym.spaces
import numpy as np
from Para_def import SACEnv


class VECEnv(gym.Env):
    def __init__(self,env_config):
        self.s = 3

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
        self.reset()

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
        return self.observation

    def step(self,action)->tuple:
        '''
        step in env
        @param action: take action selected by agent(range from[0,num of base station],Sbk)
        @return: tuple of (observation, reward, done, info)
        '''
        #update the state of chosen base station
        # self.base_station.update_reliability(action[0])
        self.base_station.get_utility(action)
        self.base_station.get_Utility_task(action)
        self.base_station.get_normalized_utility(action)
        self.base_station.update_completion_ratio(action)
        self.base_station.update_compute_efficiency(action)
        self.base_station.update_reliability(action)
        # print("last state:",self.observation[0]-action)
        print("action", action)
        # print("state:",self.observation[0])
        self.step_num+=1
        # reward=self.base_station.get_reward(action[0],action[1])
        reward=self.base_station.get_reward(action)
        if self.step_num>100:
            self.done=True
        self.observation = np.concatenate([self.base_station.Fs,self.base_station.snr,self.base_station.link_dur,self.base_station.reliability,self.base_station.C_size,self.base_station.D_size,self.base_station.t_delay])
        return self.observation,reward,self.done,{}



    def render(self,mode='human'):
        pass


if __name__ == '__main__':
    env = VECEnv()
    env.reset()




