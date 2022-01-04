from ray import tune
import ray
from ray.rllib.agents.dqn import DQNTrainer
from MyEnv import GridEnv

ray.init()
t = tune.run(
    DQNTrainer,
    config={
        'env':GridEnv,
        'double_q':True,
    },
    stop={
        'episode_reward_mean':200
    }
)

