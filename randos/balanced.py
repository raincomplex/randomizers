'based on <a href="https://www.reddit.com/r/Tetris/comments/ceap8l/randomizer_concept_ramblings/">this reddit post</a>'
import random

def balanced9():
    '5 from a standard bag, 2 random, 2 least seen'
    return Balanced(std=5, rand=2, least=2)

def balanced7():
    '5 from a standard bag, 2 random'
    return Balanced(std=5, rand=2, least=0)

def balanced5():
    '5 from a standard bag'
    return Balanced(std=5, rand=0, least=0)

class Balanced:
    def __init__(self, std=5, rand=2, least=2):
        self.std = std
        self.rand = rand
        self.least = least

        self.counts = {c: 0 for c in 'jiltsoz'}
        self.rebag()

    def rebag(self):
        self.bag = random.sample('jiltsoz', self.std)

        self.bag += [random.choice('jiltsoz') for _ in range(self.rand)]

        seen = list(self.counts.items())
        seen.sort(key=lambda t: (t[1], random.random()))
        self.bag += [t[0] for t in seen[:self.least]]

        random.shuffle(self.bag)

    def next(self):
        p = self.bag.pop()
        if not self.bag:
            self.rebag()
        self.counts[p] += 1
        return p


def balanced_long_add_pure(history):
    'look at a big section of history, decreasing the chance for a piece each time it occurs (additive)'
    score = 5
    p = {c: score for c in 'jiltsoz'}
    for c in history[-score*7:]:
        if p[c] > 0:
            p[c] -= 1
    if sum(p.values()) == 0:
        p = {c: 1 for c in 'jiltsoz'}
    return p

def balanced_long_mul_pure(history):
    'look at a big section of history, decreasing the chance for a piece each time it occurs (multiplicative)'
    score = 5
    p = {c: score for c in 'jiltsoz'}
    for c in history[-score*7:]:
        p[c] *= .7
    return p
