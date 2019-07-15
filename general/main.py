#!/usr/bin/env python3
import random
import randos

def run(randfunc, count=1000):
    'generate a piece sequence with the given randomizer function'
    history = []
    while len(history) < count:
        r = randfunc(history)
        p = generatePiece(r)
        history.append(p)
    return history

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

def formatProbs(p):
    return '{%s}' % ', '.join('%s %.3f' % (c, p.get(c, 0)) for c in 'jiltsoz')

if __name__ == '__main__':
    import sys
    
    count = 10000
    display = 80
    showrunprob = ('-p' in sys.argv)
    
    funclist = []
    for name in dir(randos):
        if not name.startswith('_'):
            funclist.append(getattr(randos, name))
    funclist.sort(key=lambda f: f.__code__.co_firstlineno)
    
    for func in funclist:
        print(func.__name__)
        seq = ''.join(run(func, count))
        print(seq[:display])
        
        doubles = 0
        for i in range(len(seq) - 1):
            if seq[i] == seq[i+1]:
                doubles += 1
        print('doubles', doubles / count)
        if showrunprob:
            for c in range(7):
                print(c, formatProbs(runprob(func, c)))

        print()