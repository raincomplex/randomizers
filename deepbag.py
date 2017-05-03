import random

class Randomizer:
    def __init__(self):
        self.bag = list('jiltsoz')
        self.rebag()
        
    def rebag(self):
        self.bag2 = list('jiltsoz')
        random.shuffle(self.bag2)
        
    def next(self):
        i = random.randint(0, len(self.bag) - 1)
        p = self.bag[i]
        self.bag[i] = self.bag2.pop()
        if len(self.bag2) == 0:
            self.rebag()
        return p
