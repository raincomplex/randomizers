import random

class Randomizer:
    def __init__(self):
        self.last = None

    def next(self):
        x = random.choice('jiltsozx')
        if x == 'x' or x == self.last:
            x = random.choice('jiltsoz')
        self.last = x
        return x
