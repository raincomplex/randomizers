'start with a fixed sequence, and shift the pieces randomly'
import random, math

class Shift:
    def __init__(self, maxdist=7):
        self.maxdist = maxdist

        self.i = 0
        self.seq = []
        self.last = None  # just used to check that the random spread doesn't leak

        for k in range(math.ceil(self.maxdist * 2)):
            self.advance()

    def advance(self):
        offset = 2 * self.maxdist * random.random() - self.maxdist
        self.seq.append((self.i + offset, 'jiltsoz'[self.i % 7]))
        self.seq.sort()
        self.i += 1

    def next(self):
        self.advance()
        w, p = self.seq.pop(0)
        if self.last is not None:
            assert w > self.last
        self.last = w
        return p

def shift1_75():
    return Shift(1.75)

def shift3_5():
    return Shift(3.5)

def shift7():
    return Shift(7)

def shift10_5():
    return Shift(10.5)

def shift14():
    return Shift(14)

def shift21():
    return Shift(21)
