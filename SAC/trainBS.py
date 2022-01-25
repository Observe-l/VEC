import numpy as np

from ray import tune
import ray

from ray.rllib.agents.sac import SACTrainer

from VECEnv import VECEnv
ray.init()
t = tune.run(
    SACTrainer,
    config={
        'env':VECEnv,
        'twin_q':True,
        'framework':'torch'
    },
    stop={
        'episodes_total':200
    }
)