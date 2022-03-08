import numpy as np

from ray import tune
import ray

from ray.rllib.agents.sac import SACTrainer

from VECEnv import VECEnv
# import udp_request
ray.init()
# ray.init(address='auto', _redis_password='5241590000000000')

if __name__ == '__main__':
    t = tune.run(
        SACTrainer,
        config={
            'env':VECEnv,
            'twin_q':True,
            'framework':'torch'
        },
        stop={
            'episodes_total':5000
        }
    )