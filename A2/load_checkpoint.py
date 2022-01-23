import ray
from ray.rllib.agents import dqn
from env.VECEnv import VECEnv


config={
    'double_q':True,
    'framework':'tf2'
}
ray.init()
trainer = dqn.DQNTrainer(env=VECEnv,config=config)
policy=trainer.get_policy()
#load trained model
trainer.load_checkpoint("/home/jaimin/PycharmProjects/VECv1.1/checkpoint/checkpoint-1")

#use state to check the action
#build environment
env_config={}
env=VECEnv(env_config)
obs=env.reset()
print(trainer.compute_single_action(obs))




print("ss")


