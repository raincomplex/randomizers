#!/usr/bin/env python3
import unittest, random
import load, pure

enabled = True
count = 10000  # number of long histories to test
maxsize = 20  # determines length of long histories
travel = 10  # number of pieces to add to each history while checking it

class Robustness(unittest.TestCase):
    'make sure that general randomizers can be applied to arbitrary histories without breaking'

def maketest(r):
    def checkhistory(self, history):
        for k in range(travel):
            p = r(history)
            self.assertTrue(type(p) is dict)
            self.assertTrue(sum(p.values()) > 0)
            c = pure.generatePiece(p)
            self.assertTrue(c in 'jiltsoz')
            history.append(c)

    def func(self):
        # check all the short histories
        checkhistory(self, [])
        for c in 'jiltsoz':
            checkhistory(self, [c])
            for d in 'jiltsoz':
                checkhistory(self, [c, d])

        # check a bunch of random long histories
        for i in range(count):
            size = random.randint(int(maxsize/2), maxsize)
            history = []
            for k in range(size):
                history.append(random.choice('jiltsoz'))
            checkhistory(self, history)

    return func

if enabled:
    for r in pure.listrandos():
        setattr(Robustness, 'test_' + r.__name__, maketest(r))

def blend_test():
    import math

    one = load.rands['bag_pure'].getfunc()
    two = load.rands['flatbag_pure'].getfunc()
    count = 1000

    def mixprobs(a, b, v):
        c = {}
        for p in 'jiltsoz':
            c[p] = a.get(p, 0) * v + b.get(p, 0) * (1 - v)
        return c

    history = []
    for i in range(count):
        a = (i / count) * (2 * math.pi)
        v = (1 + math.cos(a)) / 2

        p1 = one(history)
        p2 = two(history)
        p = mixprobs(p1, p2, v)
        history.append(pure.generatePiece(p))

    print('mixing from %s to %s and back (%d pieces)' % (one.__name__, two.__name__, count))
    print()
    print(''.join(history))
    print()

if __name__ == '__main__':
    import sys
    
    count = 10000
    display = 80
    showrunprob = ('-p' in sys.argv)
    
    def formatProbs(p):
        return '{%s}' % ', '.join('%s %.3f' % (c, p.get(c, 0)) for c in 'jiltsoz')

    for func in pure.listrandos():
        print(func.__name__)
        seq = ''.join(pure.run(func, count))
        print(seq[:display])
        
        doubles = 0
        for i in range(len(seq) - 1):
            if seq[i] == seq[i+1]:
                doubles += 1
        print('doubles', doubles / count)
        if showrunprob:
            for c in range(7):
                print(c, formatProbs(pure.runprob(func, c)))

        print()

    blend_test()
