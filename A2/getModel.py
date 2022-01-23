import ray
from ray.rllib.agents import dqn
from env.VECEnv import VECEnv


config={
    'double_q':True,
    'framework':'tf2'
}
ray.init()
trainer = dqn.DQNTrainer(env=VECEnv,config=config)
for i in range(1):
    trainer.train()
    print("iteration:",i)
policy=trainer.get_policy()
trainer.save_checkpoint("/home/jaimin/PycharmProjects/VECv1.1/checkpoint/checkpoint-1")
# print(model.base_model.summary())
print("ss")


