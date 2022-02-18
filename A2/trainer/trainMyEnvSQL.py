from ray import tune
import ray
from ray.rllib.agents.dqn import DQNTrainer
from A2.env.A2Env import A2Env
ray.init()
t = tune.run(
    DQNTrainer,
    config={
        'env':A2Env,
        'double_q':True,
        'framework':'tfe'
    },
    stop={
        'episodes_total':50
    }
)