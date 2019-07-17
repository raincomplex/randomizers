import random

class nes:
    def __init__(self):
        self.last = None

    def next(self):
        x = random.choice('jiltsozx')
        if x == 'x' or x == self.last:
            x = random.choice('jiltsoz')
        self.last = x
        return x

def nes_pure(history):
    if len(history) > 0:
        last = history[-1]
        # 7 points to each of 'jiltsozx'
        # last and x get rerolled into 'jiltsoz' (14/7 = +2 each)
        p = {c: (9 if c != last else 2) for c in 'jiltsoz'}
    else:
        # 7 points to each of 'jiltsozx'
        # x gets rerolled into 'jiltsoz' (+1 each)
        p = {c: 8 for c in 'jiltsoz'}
    return p
