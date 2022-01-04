import numpy as np

from ray import tune
import ray
from ray.rllib.agents.sac import  SACTrainer


ray.init()
t = tune.run(
    SACTrainer,
    config={
        'env':"CartPole-v0",
        'twin_q':True,
    },
    stop={
        'episode_reward_mean':200
    }
)

