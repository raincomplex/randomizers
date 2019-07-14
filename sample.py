#!/usr/bin/env python3
import sys, load

count = 1000

names = sys.argv[1:]
if not names:
    names = sorted(load.rands.keys())

for name in names:
    rand = load.rands[name]()
    s = ''
    for i in range(count):
        s += rand.next()

    print(name)
    print(s)
    print()
