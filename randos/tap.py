import unittest
import tgm

class Randomizer(tgm.Randomizer):
    def __init__(self, seed=None):
        tgm.Randomizer.__init__(self, seed=seed, rolls=6)
        self.history = [self.history[0], 1, 2, 2]

class Tests(unittest.TestCase):
    def testPRNG(self):
        r = Randomizer(tgm.unrand(0xeb48c724))
        goal = 'tijostzijslzijsltozjsltojzltsoizljsizlto'
        s = ''
        for i in range(len(goal)):
            s += r.next()
        assert s == goal
