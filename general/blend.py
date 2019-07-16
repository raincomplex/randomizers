#!/usr/bin/env python3
'demo of smoothly blending between general randomizers'

import math
from main import randos, generatePiece

one = randos.bag
two = randos.flat
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
    history.append(generatePiece(p))

print('mixing from %s to %s and back (%d pieces)' % (one.__name__, two.__name__, count))
print()
print(''.join(history))
