import time, unittest

pieces = 'izsjlot'

def rand(n):
    return (n * 0x41c64e6d + 12345) & 0xffffffff

def unrand(n):
    return ((n - 12345) * 0xeeb9eb65) & 0xffffffff

class tgm:
    def __init__(self, seed=None, rolls=4):
        if seed == None:
            seed = int(time.time())
        self.seed = seed
        self.rolls = rolls
        
        b = 1
        while b == 1 or b == 2 or b == 5:
            b = self.read() % 7
        self.history = [b, 1, 1, 1]

    def read(self):
        self.seed = rand(self.seed)
        return (self.seed >> 10) & 0x7fff

    def next(self):
        r = self.history[0]
        
        for i in range(self.rolls - 1):
            b = self.read() % 7
            if b not in self.history:
                break
            b = self.read() % 7
            
        self.history.pop()
        self.history.insert(0, b)

        return pieces[r]

def tgm_pure(history, rolls=4, start='zzzz'):
    if len(history) == 0:
        return {'j': 1, 'i': 1, 'l': 1, 't': 1}
    
    history = history[-4:]
    if len(history) < 4:
        history = (list(start) + history)[-4:]

    p = {c: 0 for c in 'jiltsoz'}
    w = 1
    for i in range(rolls - 1):
        carry = 0
        for c in 'jiltsoz':
            if c in history:
                carry += w
            else:
                p[c] += w
        w = carry / 7
    for c in 'jiltsoz':
        p[c] += w

    return p


class tgm_tap(tgm):
    def __init__(self, seed=None):
        tgm.__init__(self, seed=seed, rolls=6)
        self.history = [self.history[0], 1, 2, 2]

def tgm_tap_pure(history):
    return tgm_pure(history, rolls=6, start='szsz')


class Tests(unittest.TestCase):
    def testPRNG(self):
        r = tgm_tap(unrand(0xeb48c724))
        goal = 'tijostzijslzijsltozjsltojzltsoizljsizlto'
        s = ''
        for i in range(len(goal)):
            s += r.next()
        assert s == goal
