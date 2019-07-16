#!/usr/bin/env python3
import os

minconnections = 5
maxdist = .3  # maximum distance to create a connection

d = {}
include = set()
with open('similarity.txt', 'r') as f:
    n = 0
    for line in f:
        if line.startswith(' '):
            dist, other = line.split()
            dist = float(dist)
            if (other, cur) not in d:
                d[cur, other] = dist
            if n < minconnections:
                include.add((cur, other))
                include.add((other, cur))
            n += 1
        else:
            cur = line.strip()
            n = 0

with open('similarity.dot', 'w') as f:
    print('graph { start=true; ', file=f)
    for (a, b), w in d.items():
        if w < maxdist or (a, b) in include:
            h = w
            if h > maxdist:
                h = maxdist
            h = (h / maxdist) ** .5
            
            h = hex(int(255 * h))[2:]
            if len(h) == 1: h = '0' + h
            color = '#' + h*3
            
            print('"%s" -- "%s" [weight=%.3f, color="%s"];' % (a, b, 1/w if w != 0 else 1e6, color), file=f)
    print('}', file=f)

os.system('fdp -Tpng < similarity.dot > similarity.png')
