'weight according to recentness'
import random

class weight:
    'linear'
    def __init__(self):
        self.history = []

        self.historymax = 10  # max length of history
        self.wmaxplace = 6
        
        self.wmin = .5  # weight when piece is at 0 in history
        self.wmax = 5  # weight when piece is at wmaxplace or later in history
        self.wmissing = 10  # weight when piece is not in history at all
    
    def next(self):
        prob = {}
        for piece in 'jiltsoz':
            try:
                n = self.history.index(piece)
            except ValueError:
                w = self.wmissing
            else:
                if n > self.wmaxplace:
                    n = self.wmaxplace
                w = self.wmin + (self.wmax - self.wmin) * (n / self.wmaxplace)

            prob[piece] = w

        total = sum(prob.values())
        r = random.random() * total
        for piece, w in prob.items():
            r -= w
            if r <= 0:
                self.history.insert(0, piece)
                if len(self.history) > self.historymax:
                    self.history.pop()
                return piece

        raise Exception()

class weight2:
    'inverse to drought'
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


class weight_exp:
    'multiplicative'
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


def _recent(history, op):
    p = {}
    w = 1
    for c in reversed(history):
        if c not in p:
            p[c] = w
            w = op(w)
            if len(p) == 7:
                break
    for c in 'jiltsoz':
        if c not in p:
            p[c] = w
    return p

def weight_exp_pure(history):
    'multiplicative'
    return _recent(history, lambda w: w*2)

def weight_lin_pure(history):
    'additive'
    return _recent(history, lambda w: w+1)
