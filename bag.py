import random

class Randomizer:
    def __init__(self, bag='jiltsoz'):
        self.bag = bag
        self.rebag()

    def rebag(self):
        self.pile = list(self.bag)
        random.shuffle(self.pile)

    def next(self):
        p = self.pile.pop()
        if len(self.pile) == 0:
            self.rebag()
        return p
