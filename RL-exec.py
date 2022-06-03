import numpy as np
import random
import time

from tools import *

EPISODES = 10
DIRECTIONS = {'right':(1, 0), 'left':(-1, 0), 'up':(0, -1), 'down':(0, 1)}

class GridWorld:
    def __init__(self, r=4, c=4):
        self.row = 0
        self.col = 0
        self.stage = np.zeros((r, c))
        self.world = np.zeros((r, c))
        self.set_world()
        self.row_size = r
        self.col_size = c
    
    def set_world(self, table:np.ndarray=None):
        if table is None:
            table = self.world
            table[self.world.shape[0]-1][self.world.shape[1]-1] = 2
        self.world = table
    
    def step(self, direction):
        '''direction : string or 0/right, 1/left, 2/up, 3/down'''
        if isinstance(direction, int):
            direction_keys = list(DIRECTIONS.keys())
            direction = direction_keys[direction]
        
        self.move_with_direction_str(direction)
        reward = -1
        done = self.is_done()
        return (self.row, self.col), reward, done
    
    def is_done(self):
        # return (self.row == self.stage.shape[0] - 1 and self.col == self.stage.shape[1]  - 1)
        return (self.world[self.row][self.col] == 2)
    
    def move_with_direction_str(self, direction:str):
        if direction not in DIRECTIONS.keys(): return False
        row_next = clamp(self.row + DIRECTIONS[direction][0], 0, self.stage.shape[0] - 1)
        col_next = clamp(self.col + DIRECTIONS[direction][1], 0, self.stage.shape[1] - 1)
        if self.world[row_next][col_next] == 1:
            return False
        self.row = row_next
        self.col = col_next
        return True
    
    def get_state(self):
        return self.row, self.col
    
    def reset(self):
        # self.__init__(*self.stage.shape)
        self.row = 0
        self.col = 0
        return (self.row, self.col)
        
class Agent:
    def __init__(self):
        pass
    
    def select_action(self):
        return random.choice(list(DIRECTIONS.keys()))

class QAgent:
    def __init__(self, row = 4, col = 4) -> None:
        self.q_table:np.ndarray = np.zeros((row, col, DIRECTIONS.keys().__len__()))
        self.result_data = np.zeros((row, col))
        self.eps = 0.9
        self.alpha = 0.1
        
    def select_action(self, s):
        # eps-greedy
        x, y = s
        direction_keys = list(DIRECTIONS.keys())
        
        if random.random() < self.eps:
            action_str = random.choice(list(DIRECTIONS.keys()))
            action = direction_keys.index(action_str)
        else:
            action_val = self.q_table[x, y, :]
            direction_int = np.argmax(action_val)
            action = DIRECTIONS[direction_keys[direction_int]]
        return action
    
    def update_table(self, history):
        # with history of ONE EPISODE, update q_table
        cum_reward = 0
        for transition in history[::-1]:
            s, a, r, s_prime = transition
            x, y = s
            # MC
            self.q_table[x, y, a] += self.alpha * (cum_reward - self.q_table[x, y, a])
            cum_reward += r
    
    def anneal_eps(self, val = 0.03):
        self.eps -= val
        self.eps = max(self.eps, 0.1)
    
    def show_table(self):
        # show max q on each s
        q_lst = self.q_table.tolist()
        
        for row_idx in range(len(q_lst)):
            row = q_lst[row_idx]
            for col_idx in range(len(row)):
                col = row[col_idx]
                action = np.argmax(col)
                self.result_data[row_idx, col_idx] = action
        print(self.result_data)
        
            

def main_MC_incremental_update(ep_num = None):
    env = GridWorld(4,4)
    agent = Agent()
    gamma = 1.0
    reward = -1
    alpha = 0.001
    
    if not ep_num: ep_num = EPISODES
    for k in range(ep_num):
        done = False
        history = []
        
        while not done:
            action = agent.select_action()
            (x, y), reward, done = env.step(action)
            history.append((x, y, reward))
        # print(history)
        env.reset()
        
        cum_reward = 0
        for transition in history[::-1]:
            x, y, reward = transition
            env.stage[x][y] += alpha * (cum_reward - env.stage[x][y])
            cum_reward = reward + gamma * cum_reward
            
    for row in env.stage:
        print(row)
    
def main_TD(ep_num = None):
    env = GridWorld()
    agent = Agent()
    gamma = 1.0
    alpha = 0.01 # MC에 비해 큰 값을 사용
    
    if not ep_num: ep_num = EPISODES
    for _ in range(ep_num):
        done = False
        while not done:
            x, y = env.get_state()
            action = agent.select_action()
            (x_prime, y_prime), reward, done = env.step(action)
            
            env.stage[x][y] += alpha * (reward + gamma * env.stage[x_prime][y_prime] - env.stage[x][y])
        env.reset()
    
    print(env.stage)

def main_MC_control(ep_num=None):
    if not ep_num: ep_num = EPISODES
    
    w = np.array([[0,0,1,0,0,0,0],
                  [0,0,1,0,0,0,0],
                  [0,0,1,0,1,0,0],
                  [0,0,0,0,1,0,0],
                  [0,0,0,0,1,0,2]])
    env = GridWorld(w.shape[0], w.shape[1])
    env.set_world(w)
    agent = QAgent(w.shape[0], w.shape[1])
    
    for _ in range(ep_num):
        done = False
        history = []
        
        s = env.reset()
        while not done:
            a = agent.select_action(s)
            s_prime, r, done = env.step(a)
            history.append((s, a, r, s_prime))
            s = s_prime
        
        agent.update_table(history)
        agent.anneal_eps()
    agent.show_table()
    # print(history)


start_time = time.perf_counter()

# main_MC_incremental_update()
# main_TD()
main_MC_control(100)


print(time.perf_counter() - start_time)
