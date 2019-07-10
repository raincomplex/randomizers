import random

class Randomizer:
    def __init__(self):
        self.history = list('ojltisz')
        self.chance = .5

    def next(self):
        for i in range(len(self.history) - 1):
            if random.random() < self.chance:
                x = self.history.pop(i)
                self.history.append(x)
                return x
        return self.history[-1]
