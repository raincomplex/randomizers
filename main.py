#!/usr/bin/env python3
import re, os, sys
from multiprocessing import Pool, cpu_count

import load, analysis, compare

count = 1000000
if '--fast' in sys.argv:
    count = 100000

# end config

if not os.path.isdir('cache'):
    os.mkdir('cache')

def process(t):
    name, factory = t

    cachepath = os.path.join('cache', name.replace('/', '_'))

    s = None
    if goodcache(name, cachepath):
        usedcache = True
        with open(cachepath, 'r') as f:
            s = f.read()
        if len(s) != count:
            s = None

    if s is None:
        usedcache = False
        r = factory()
        s = ''
        for i in range(count):
            s += r.next()
        with open(cachepath, 'w') as f:
            f.write(s)

    a = analysis.analyze(s)
    print('...', name, ' (cached sequence)' if usedcache else '')
    return (name, a)

def goodcache(name, cachepath):
    if not os.path.exists(cachepath):
        return False
    modpath = os.path.join('randos', name.split('/')[0] + '.py')
    if os.stat(cachepath).st_mtime < os.stat(modpath).st_mtime:
        return False
    return True

pool = Pool(cpu_count())
m = pool.map(process, sorted(load.rands.items()))

keys = set()
with open('byalgo.txt', 'w') as f:
    print(file=f)
    for t in m:
        name, a = t
        print(name, file=f)
        for k, v in sorted(a.items()):
            if not re.search(r'_[jiltsoz]$', k):
                keys.add(k)
                print('    %s: %s' % (k, v), file=f)
                compare.addelement(name, k, v)
        print(file=f)
print('wrote byalgo.txt')

compare.similarity()

keys = keys - compare.exclude_compare

with open('bymetric.txt', 'w') as f:
    print(file=f)
    for key in sorted(keys):
        print(key, file=f)
        print('    %s' % analysis.desc[key], file=f)
        m.sort(key=lambda t: t[1][key])
        for name, a in m:
            print('%14.10f  %s' % (a[key], name), file=f)
        print(file=f)
print('wrote bymetric.txt')
