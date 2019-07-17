#!/usr/bin/env python3
import os, json

minconnections = 5
maxdist = .2  # maximum distance to create a connection

with open(os.path.join('cache', 'similarity.json'), 'r') as f:
    sim = json.load(f)

d = {}
include = set()
for cur in sim:
    n = 0
    for other, dist in sorted(sim[cur].items(), key=lambda t: t[1]):
        if (other, cur) not in d:
            d[cur, other] = dist
        if n < minconnections:
            include.add((cur, other))
            include.add((other, cur))
        n += 1

dotfile = os.path.join('cache', 'similarity.dot')
with open(dotfile, 'w') as f:
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

os.system('fdp -Tpng < %s > %s' % (dotfile, os.path.join('html', 'similarity.png'))
