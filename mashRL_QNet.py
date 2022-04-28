import time
time_start = time.perf_counter()
# One-hot encoding
import numpy as np

def one_hot(x, size=16):
    return np.identity(size)[x:x + 1]


# import tensorflow.compat.v1 as tf
from tensorflow import compat
# 버전 차이때문에 v1의 것을 끌어다 사용
tf = compat.v1
tf.compat.v1.disable_eager_execution()

import gym
import matplotlib.pyplot as plt

env = gym.make('FrozenLake-v1')
input_size = env.observation_space.n
output_size = env.action_space.n
learning_rate = 0.1

# establish the feed-forward part of the network used to choose actions
X = tf.placeholder(shape = [1, input_size], dtype = tf.float32) # state input
W = tf.Variable(tf.random.uniform([input_size, output_size], 0, 0.01))  # weight

Q_hat = tf.matmul(X, W) # out Q prediction
Y = tf.placeholder(shape = [1, output_size], dtype = tf.float32)   # Y label

loss = tf.reduce_sum(tf.square(Y - Q_hat))
train = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(loss)

# set Q-learning related parameters
discount = .99
num_episodes = 2000

# create lists to contain total rewards and steps per episode
rList = []

init = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init)
    for i in range(num_episodes):
        # reset env and get first new observation
        s = env.reset()
        e = 1. / ((i // 50) + 10)
        rAll = 0
        done = False
        local_loss = []
        
        # Q-Network training !
        while not done:
            # choose an action by greedily (with e chance of random action) from q-network
            Qs = sess.run(Q_hat, feed_dict = {X: one_hot(s)})
            if np.random.rand(1) < e:
                a = env.action_space.sample()
            else:
                a = np.argmax(Qs)
            
            # get new state and reward from environment
            s1, reward, done, info = env.step(a)
            
            if done:
                # update Q, and no Q_s1, because it's terminal state
                Qs[0, a] = reward
                # (1, 16) X (16, 4) matmul 한 결과이므로 (1, 4)의 shape을 가지게 되고, [0, a]로 접근 가능
            else:
                # obtain the Q_s1 values by feeding the new state through our network
                Qs1 = sess.run(Q_hat, feed_dict = {X: one_hot(s1)})
                # update Qs
                Qs[0, a] = reward + discount * np.max(Qs1)
            
            # train our network using target (Y) and predicted Q (q_hat) values
            sess.run(train, feed_dict = {X: one_hot(s), Y: Qs})
            
            rAll += reward
            s = s1
        rList.append(rAll)


print(f'elapsed time: {time.perf_counter() - time_start}s')
print(f'success rate : {str(sum(rList) / num_episodes * 100)}%')
plt.plot(rList)
