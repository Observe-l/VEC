from ray import tune
import ray
from ray.rllib.agents.dqn import DQNTrainer
from env.VECEnv import VECEnv
ray.init()
t = tune.run(
    DQNTrainer,
    config={
        'env':VECEnv,
        'double_q':True,
        'framework':'tfe'
    },
    stop={
        'episodes_total':200
    }
)