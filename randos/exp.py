import random

class Randomizer:
    def __init__(self):
        self.history = list('ojltisz')
        self.actual = []
        self.chance = .5
        self.protect = True  # drought protection

    def next(self):
        x = None

        if self.protect:
            for p in 'jiltsoz':
                if len(self.actual) == 12 and p not in self.actual:
                    x = p
                    break

        if x is None:
            for i in range(len(self.history) - 1):
                if random.random() < self.chance:
                    x = self.history.pop(i)
                    self.history.append(x)
                    break

        if x is None:
            x = self.history[-1]

        if len(self.actual) == 12:
            self.actual.pop(0)
        self.actual.append(x)

        return x
