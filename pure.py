import random

def listrandos():
    import load
    lst = [r for r in load.rands.values() if type(r) == Factory]
    lst.sort(key=lambda f: f.name)
    lst = [r.getfunc() for r in lst]
    return lst

# binding r by returning a local function from a factory function causes pickling to fail ("can't pickle local"), so use a callable class instead
class Factory:
    def __init__(self, r):
        self.r = r
        self.__name__ = r.__name__
        self.__doc__ = r.__doc__

    def __call__(self):
        return Stream(self.r)

    def getfunc(self):
        return self.r

class Stream:
    def __init__(self, func, history=None):
        self.func = func
        self.history = history or []

    def next(self):
        r = self.func(self.history)
        p = generatePiece(r)
        self.history.append(p)
        return p

def run(randfunc, count=1000):
    'generate a piece sequence with the given randomizer function'
    s = Stream(randfunc)
    for i in range(count):
        s.next()
    return s.history

def runprob(randfunc, count, history=None):
    'find the probability of the next piece after "count" pieces, considering all possiblilities'
    if history is None:
        history = []

    r = randfunc(history)
    if count == 0:
        total = sum(r.values())
        return {c: v / total for c, v in r.items()}
    
    s = {}
    for c in 'jiltsoz':
        w = r.get(c, 0)
        if w > 0:
            x = runprob(randfunc, count - 1, history + [c])
            for d in 'jiltsoz':
                s[d] = s.get(d, 0) + w * x.get(d, 0)

    total = sum(s.values())
    return {c: v / total for c, v in s.items()}

def generatePiece(probs):
    '''
    generate a random piece from the weights given:
        probs = {"j": <float>, "i": <float>, ...}.
    
    missing weights are taken to be 0.
    at least one non-zero weight must be given.
    '''
    total = sum(probs.values())
    if total <= 0:
        raise ValueError('sum of weights must be > 0')
    r = random.random()
    for c in 'jiltso':
        r -= probs.get(c, 0) / total
        if r < 0:
            return c
    return 'z'
