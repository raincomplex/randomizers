'''
the Forever Bag

Pieces are taken from a set bag (such as JILTSOZ) in order, repeating, to fill a window of a fixed size (I use 4, but any number > 1 works; higher numbers behave more like full random, but still with shorter droughts). Each time a piece is needed, it is chosen randomly from the window, and then replaced with the next piece in the bag order. The order of the bag is notably important when the window size is smaller than the bag -- this limits what the first piece can be (only JILT, with my parameters).
'''
import random

def factory1():
    'plain'
    return Randomizer()

def factory2():
    'window=10'
    return Randomizer(windowsize=10)

def factory3():
    'shuffle'
    return Randomizer(shuffle=True)

class Randomizer:
    def __init__(self, bag='jiltsoz', windowsize=4, shuffle=False):
        self.bag = list(bag)
        self.size = windowsize
        self.shuffle = shuffle
        self.window = []
        self.i = 0

        if self.shuffle:
            random.shuffle(self.bag)
        
        for i in range(self.size):
            self.window.append(self.bag[self.i])
            self.advance()

    def next(self):
        r = random.randint(0, self.size - 1)
        p = self.window[r]
        self.window[r] = self.bag[self.i]
        self.advance()
        return p

    def advance(self):
        self.i = (self.i + 1) % len(self.bag)
        if self.i == 0 and self.shuffle:
            random.shuffle(self.bag)

if __name__ == '__main__':
    fb = ForeverBag('jiltsoz', 4)
    for i in range(10):
        s = ''
        for i in range(40):
            s += fb.next()
        print s
