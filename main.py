#!/usr/bin/env python3
import re, sys
from multiprocessing import Pool, cpu_count

import load
from analysis import analyze
import compare

count = 1000000
if '--fast' in sys.argv:
    count = 100000

#compare_single = 'entropy'

# end config

def process(t):
    name, factory = t
    r = factory()
    s = ''
    for i in range(count):
        s += r.next()
    a = analyze(s)
    print('...', name)
    return (name, a)

pool = Pool(cpu_count())
m = pool.map(process, sorted(load.rands.items()))
print()
for t in m:
    name, a = t
    print(name)
    for k, v in sorted(a.items()):
        if not re.search(r'_[jiltsoz]$', k):
            print('    %s: %s' % (k, v))
            compare.addelement(name, k, v)
    print()

compare.similarity()

if 'compare_single' in globals():
    key = compare_single
    print(key)
    m.sort(key=lambda t: t[1][key])
    for name, a in m:
        print('%14.10f  %s' % (a[key], name))
    print()
