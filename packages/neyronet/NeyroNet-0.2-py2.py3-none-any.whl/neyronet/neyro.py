import numpy as np
class neyron():
    def __init__(self):
        self.weight = 0.01
        self.last_error = 1.1
        self.smoothing = 0.00001
    def calc(self, input_data):
        return input_data * self.weight
    def train(self, inp, exres):
        res = inp * self.weight
        self.last_error = exres - res
        cr = self.last_error / res
        cr = cr * self.smoothing
        self.weight += cr
    def check_train(self):
        if(self.last_error > self.smoothing) or (self.last_error < -self.smoothing):
            return False
        else:
            return True

class neyro():
    def __init__(self):
        np.random.seed(1)
        self.wei = 2 * np.random.random((3,1)) - 1
    def train(self, inp, out, we, ne=50000):
        inp = np.array(inp); out = np.array(out).T
        wei = we
        for i in range(ne):
            print(f'{i}/{ne}', end='\r')
            inpl = inp
            outs = 1 / (1 + np.exp(-np.dot(inpl, wei)))
            err = out - outs
            adj = np.dot(inpl.T, err * (outs * (1 - outs)))
            wei = wei + adj
        print(' ' * 100,end='\r')
        self.wei = wei
    def calc(self, dt):
        dt = np.array(dt)
        return 1 / (1 + np.exp(-np.dot(dt, self.wei)))
