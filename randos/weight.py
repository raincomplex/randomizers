import random

class Randomizer:
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
