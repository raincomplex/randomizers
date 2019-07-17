'pieces are drawn from a bag (the window) which is refilled by a second bag'
import random

def deepbag_window4():
    'window=4'
    return DeepBag(windowsize=4)

def deepbag_window7():
    'window=7'
    return DeepBag(windowsize=7)

def deepbag_window10():
    'window=10'
    return DeepBag(windowsize=10)

def deepbag_fixed4():
    'window=4, fixed second bag'
    return DeepBag(windowsize=4, shuffle=False)

def deepbag_fixed7():
    'window=7, fixed second bag'
    return DeepBag(windowsize=7, shuffle=False)

def deepbag_fixed10():
    'window=10, fixed second bag'
    return DeepBag(windowsize=10, shuffle=False)

class DeepBag:
    def __init__(self, bag='jiltsoz', windowsize=7, shuffle=True):
        self.window = []
        self.size = windowsize
        
        self.bag = list(bag)
        self.shuffle = shuffle
        self.i = 0

        if self.shuffle:
            random.shuffle(self.bag)
        
        for i in range(self.size):
            self.window.append(self.bag[self.i])
            self.advance()

    def next(self):
        r = random.randint(0, self.size - 1)
        p = self.window[r]
        self.window[r] = self.bag[self.i]
        self.advance()
        return p

    def advance(self):
        self.i = (self.i + 1) % len(self.bag)
        if self.i == 0 and self.shuffle:
            random.shuffle(self.bag)
