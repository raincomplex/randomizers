'choose pieces from a bag, refilling when empty'
import random

class bag:
    'standard 7-piece bag'
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

class bag2(bag):
    '14-piece bag (two of each piece)'
    def __init__(self):
        bag.__init__(self, 'jiltsoz'*2)

def bag_pure(history):
    'standard 7-piece bag'
    used = len(history) % 7
    bag = set('jiltsoz')
    if used > 0:
        bag -= set(history[-used:])
    return {c: 1 for c in bag}
