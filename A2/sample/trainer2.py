import ray
from ray.rllib.agents.dqn import DQNTrainer
from sample.MyEnv import GridEnv

ray.init()
trainer = DQNTrainer(
    env=GridEnv,
    config={'framework':'tf'}
)
for i in range(10):
    t=trainer.train()
    print(t)