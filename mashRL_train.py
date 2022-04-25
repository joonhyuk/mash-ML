import numpy as np
import matplotlib.pyplot as plt
import random as pr
import gym
from gym.envs.registration import register

def rargmax(vector):
    m = np.amax(vector)
    indices = np.nonzero(vector == m)[0]
    return pr.choice(indices)

register(
    id = 'FrozenLake-v3', 
    entry_point = 'gym.envs.toy_text:FrozenLakeEnv', 
    kwargs = {'map_name' : '4x4', 
              'is_slippery' : False}
)

env = gym.make('FrozenLake-v3')
# env.reset()
# initialize table with all zeros
Q = np.zeros([env.observation_space.n, env.action_space.n])
# set learning parameters
num_episodes = 250
gamma = 0.9

# create lists to contain total rewards and steps per episode
rList = []
for _ in range(num_episodes):
    # reset environment and get first new observation
    state = env.reset()
    rAll = 0
    done = False
    
    # the Q-table learning algorithm
    while not done:
        action = rargmax(Q[state, :])
        
        # get new state and reward from environment
        new_state, reward, done, _ = env.step(action)
        
        # update Q-table with new knowledge using learning rate
        Q[state, action] = reward + gamma * np.max(Q[new_state, :])
        
        rAll += reward
        state = new_state
    rList.append(rAll)
# print(Q)

print(f'success rate: {str(sum(rList) / num_episodes)}')
print('final Q-table values')
# print('LEFT\tDOWN\tRIGHT\tUP')
# print(Q)
plt.bar(range(len(rList)), rList)
plt.show()