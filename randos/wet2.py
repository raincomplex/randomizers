import random

class Randomizer:
    def __init__(self):
        self.size = 12
        self.history = list('jiltsoz')

    def next(self):
        p = None
        for c in 'jiltsoz':
            x = self.history.count(c)
            if x == 0:
                p = c
                break
            
        if p is None:
            lst = []
            for c in 'jiltsoz':
                x = self.history.count(c)
                if x == 1:
                    lst.append(c)
            if lst:
                p = random.choice(lst)

        if p is None:
            p = random.choice('jiltsoz')

        if len(self.history) == self.size:
            self.history.pop(0)
        self.history.append(p)

        return p
