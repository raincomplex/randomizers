#!/usr/bin/python2
import importlib, re, sys, glob
from multiprocessing import Pool, cpu_count

from analysis import analyze
import compare

modulenames = glob.glob('randos/*.py')
modulenames = [re.sub(r'randos/(.*)\.py$', lambda m: m.group(1), n) for n in modulenames]
modulenames.remove('__init__')

count = 100000
if '--fast' in sys.argv:
    count = 10000

# end config

modules = {}
for m in modulenames:
    modules[m] = importlib.import_module('randos.' + m)

rands = []
for name, m in sorted(modules.items()):
    if hasattr(m, 'factory'):
        rands.append((name, m.factory))
    elif hasattr(m, 'factory1'):
        i = 1
        while hasattr(m, 'factory' + str(i)):
            f = getattr(m, 'factory' + str(i))
            n = name + '/' + (f.__doc__ or str(i))
            rands.append((n, f))
            i += 1
    elif hasattr(m, 'Randomizer'):
        rands.append((name, m.Randomizer))
    else:
        print 'module has no factory functions or Randomizer class:', name

def process(t):
    name, factory = t
    r = factory()
    s = ''
    for i in range(count):
        s += r.next()
    a = analyze(s)
    print '...', name
    return (name, a)

pool = Pool(cpu_count())
m = pool.map(process, rands)
print
for t in m:
    name, a = t
    print name
    for k, v in sorted(a.items()):
        if not re.search(r'_[jiltsoz]$', k):
            print '    %s: %s' % (k, v)
            compare.addelement(name, k, v)
    print

compare.similarity()
