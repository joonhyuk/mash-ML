import numpy as np
import matplotlib.pyplot as plt
import random as pr
import gym
from gym.envs.registration import register

def rargmax(vector):
    m = np.amax(vector)
    indices = np.nonzero(vector == m)[0]
    return pr.choice(indices)

def frozen_lake_lab(epochs = 2000, 
                    decaying_rate = 100, 
                    method = 'random_noise', 
                    size = '4x4', 
                    is_slippery = False):
    if method not in ('random noise', 'decaying e-greedy'):
        method = 'e-greedy'
    register(
        id = 'FrozenLake-v0', 
        entry_point = 'gym.envs.toy_text:FrozenLakeEnv', 
        kwargs = {'map_name' : size, 
                'is_slippery' : is_slippery}
    )

    env = gym.make('FrozenLake-v0')
    # initialize table with all zeros
    Q = np.zeros([env.observation_space.n, env.action_space.n])
    # set learning parameters
    num_episodes = 2000
    discount = 0.9

    # create lists to contain total rewards and steps per episode
    rList = []
    for i in range(num_episodes):
        # reset environment and get first new observation
        state = env.reset()
        rAll = 0
        done = False
        
        # decaying var
        e = 1. / ((i // decaying_rate) + 1)
        
        # the Q-table learning algorithm
        while not done:
            # decaying e-greedy
            if method == 'decaying e-greedy':
                if np.random.rand(1) < e:
                    action = env.action_space.sample()
                else:
                    action = np.argmax(Q[state, :])
            elif method == 'random noise':
                action = np.argmax(Q[state, :] + np.random.randn(1, env.action_space.n) / (i + 1))
            else:
                action = rargmax(Q[state, :])
            
            # add random noise
            
            # get new state and reward from environment
            new_state, reward, done, _ = env.step(action)
            
            # update Q-table with new knowledge using learning rate
            Q[state, action] = reward + discount * np.max(Q[new_state, :])
            
            rAll += reward
            state = new_state
        rList.append(rAll)
    # print(Q)

    print(f'success rate: {str(sum(rList) / num_episodes)}')
    print('final Q-table values')
    print('LEFT\tDOWN\tRIGHT\tUP')
    print(Q)
    plt.bar(range(len(rList)), rList)
    plt.show()

frozen_lake_lab(method='decaying e-greedy', decaying_rate=100)
