import random

class Randomizer:
    'full random but with drought protection'
    
    def __init__(self):
        self.size = 12
        self.history = list('jiltsoz')

    def next(self):
        p = None
        for c in 'jiltsoz':
            if c not in self.history:
                p = c
                break

        if p is None:
            p = random.choice('jiltsoz')

        if len(self.history) == self.size:
            self.history.pop(0)
        self.history.append(p)

        return p
