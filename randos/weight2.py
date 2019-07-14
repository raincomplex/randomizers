import random

class Randomizer:
    def __init__(self):
        self.weights = [1] * 7
    
    def next(self):
        for i in range(7):
            if self.weights[i] > 1:
                self.weights[i] -= 1

        total = sum(1 / w for w in self.weights)
        n = random.random() * total

        for i, w in enumerate(self.weights):
            n -= 1 / w
            if n < 0 or i == 6:
                self.weights[i] += 5
                return 'jiltsoz'[i]
