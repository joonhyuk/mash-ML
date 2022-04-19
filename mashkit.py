import numpy as np
import matplotlib.pyplot as plt

class SingleLayer:
    
    def __init__(self, learning_rate = 0.1, auto_scaling = False):
        self.w = None
        self.b = None
        self.losses = []
        self.dev_losses = []
        self.w_history = []
        self.lr = learning_rate
        self.train_mean = None
        self.train_std = None
        self.auto_scaling = auto_scaling
    
    def forpass(self, x):
        z = np.sum(x * self.w) + self.b
        return z
    
    def backprop(self, x, err):
        w_grad = x * err
        b_grad = 1 * err
        return w_grad, b_grad
    
    def add_bias(self, x):
        return np.c_[np.ones((x.shape[0], 1)), x]   # 텐서의 맨 앞에 1로 채워진 열 벡터를 추가한다.
    
    def activation(self, z):
        a = 1 / (1 + np.exp(-z))
        return a
    
    def scale_data(self, data, force = False):
        if force or ((self.train_mean is None) or (self.train_std is None)):
            self.train_mean = np.mean(data, axis=0)
            self.train_std = np.std(data, axis=0)
        # if self.train_std == 0:
            # return data
        return (data - self.train_mean) / self.train_std
    
    def update_dev_loss(self, x_dev, y_dev):
        if x_dev is None:
            return
        if self.auto_scaling:
            x_dev = self.scale_data(x_dev)
        dev_loss = 0
        for i in range(len(x_dev)):
            z = self.forpass(x_dev[i])
            a = self.activation(z)
            a = np.clip(a, 1e-10, 1-1e-10)
            dev_loss += -(y_dev[i] * np.log(a) + (1 - y_dev[i]) * np.log(1 - a))    # 각 에포크에서 평균 손실을 구하기 위해 다 더해줌
        self.dev_losses.append(dev_loss / len(y_dev))
    
    def fit(self, x, y, epochs = 100, x_dev = None, y_dev = None):
        if self.auto_scaling:
            x = self.scale_data(x, force = True)
        self.w = np.ones(x.shape[1])
        self.b = 0
        self.w_history.append(self.w.copy())
        np.random.seed(42)
        for e in range(epochs):
            loss = 0
            indexes = np.random.permutation(np.arange(len(x)))
            # indexes = range(len(x))
            for i in indexes:
                z = self.forpass(x[i])
                a = self.activation(z)
                err = - (y[i] - a)
                w_grad, b_grad = self.backprop(x[i], err)
                self.w -= w_grad
                self.b -= b_grad
                
                self.w_history.append(self.w.copy())
                a = np.clip(a, 1e-10, 1-1e-10)
                
                loss += -(y[i] * np.log(a) + (1 - y[i]) * np.log(1 - a))    # 각 에포크에서 평균 손실을 구하기 위해 다 더해줌
            self.losses.append(loss / len(y))
            self.update_dev_loss(x_dev, y_dev)
    
    def predict(self, x):
        z = [self.forpass(x_i) for x_i in x]
        a = self.activation(np.array(z))
        return a > 0.5
    
    def score(self, x, y):
        if self.auto_scaling:
            x = self.scale_data(x)
        return np.mean(self.predict(x) == y)