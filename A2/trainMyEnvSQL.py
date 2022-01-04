from ray import tune
import ray
from ray.rllib.agents.dqn import DQNTrainer
from env.A2ModelSQLEnv import A2ModelSQLEnv
ray.init(num_cpus=6)
t = tune.run(
    DQNTrainer,
    config={
        'env':A2ModelSQLEnv,
        'double_q':True,
        'framework':'tf'
    },
    stop={
        'episodes_total':150
    }
)