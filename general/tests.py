from general.main import generatePiece, listrandos
import unittest, random

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
            c = generatePiece(p)
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
    for r in listrandos():
        setattr(Robustness, 'test_' + r.__name__, maketest(r))
