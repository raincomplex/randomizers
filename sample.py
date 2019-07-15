#!/usr/bin/env python3
import sys, load

count = 1000

names = sys.argv[1:]

for i in reversed(range(len(names))):
    if names[i].isdigit():
        count = int(names[i])
        del names[i]

if 'all' in names:
    names = sorted(load.rands.keys())

elif not names:
    for name in sorted(load.rands.keys()):
        print(name)
    print()
    print('Usage: sample.py [NAME [NAME ...]]')
    print('use "all" to sample all randomizers.')
    print('you can also give a number to change the sequence length (default 1000).')
    exit(1)

for name in names:
    if name not in load.rands:
        print('no generator with name "%s". run without arguments for a list.' % name)
        exit(1)

    rand = load.rands[name]()
    s = ''
    for i in range(count):
        s += rand.next()

    print(name)
    print(s)
    print()
