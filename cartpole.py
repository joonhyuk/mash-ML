# 1. It renders instance for 1000 timesteps, perform random actions
import gym
env = gym.make('CartPole-v1')
env.reset()
for _ in range(1000):
    env.render()
    env.step(env.action_space.sample()) # take a random action
env.close()
# 2. To check all env available, uninstalled ones are also shown
from gym import envs 
print(envs.registry.all())