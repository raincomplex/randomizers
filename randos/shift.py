'start with a fixed sequence, and shift the pieces randomly'
import random

class Shift:
    def __init__(self, maxdist=14):
        self.maxdist = maxdist

        self.i = 0
        self.seq = []
        self.last = None  # just used to check that the random spread doesn't leak

        for k in range(self.maxdist):
            self.advance()

    def advance(self):
        f = self.maxdist / 2
        self.seq.append((self.i + f * random.random() - f/2, 'jiltsoz'[self.i % 7]))
        self.seq.sort()
        self.i += 1

    def next(self):
        self.advance()
        w, p = self.seq.pop(0)
        if self.last is not None:
            assert w > self.last
        self.last = w
        return p

def shift7():
    return Shift(7)

def shift10():
    return Shift(10)

def shift14():
    return Shift(14)

def shift21():
    return Shift(21)
