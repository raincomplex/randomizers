#!/usr/bin/env python3
import re, os, sys, json, math
from multiprocessing import Pool, cpu_count

import load, analysis, compare

count = 1000000
clean = False

if '--fast' in sys.argv:
    count = 100000
if '-c' in sys.argv:  # don't use cache
    clean = True

sourcerepo = 'https://github.com/raincomplex/randomizers'

# end config

if not os.path.isdir('html'):
    os.mkdir('html')
if not os.path.isdir('cache'):
    os.mkdir('cache')

def safefile(name):
    return re.sub(r'[^a-z0-9]', '_', name)

def getsequence(rand):
    s = ''
    r = rand()
    for i in range(count):
        s += r.next()
    return s

def process(t):
    name, rand = t

    cachepath = os.path.join('cache', safefile(name))

    s = None
    if not clean and goodcache(rand.modname, cachepath):
        usedcache = True
        with open(cachepath, 'r') as f:
            data = json.load(f)
        s = data['seq']
        a = data['ana']
        if len(s) != count:
            s = None

    if s is None:
        usedcache = False
        try:
            s = getsequence(rand)
        except:
            print('error while generating for', name)
            raise
        
        a = analysis.analyze(s)
        
        with open(cachepath, 'w') as f:
            json.dump({'seq': s, 'ana': a}, f)

    print('...', name, ' (cached)' if usedcache else '')
    return (name, a)

def goodcache(modname, cachepath):
    if not os.path.exists(cachepath):
        return False
    modpath = os.path.join('randos', modname + '.py')
    mt = os.stat(cachepath).st_mtime
    if mt < os.stat(modpath).st_mtime:
        return False
    if modpath.endswith('/general.py'):
        modpath = os.path.join('general', 'randos.py')
        if mt < os.stat(modpath).st_mtime:
            return False
    return True

pool = Pool(cpu_count())
m = pool.map(process, sorted(load.rands.items()))
pool.close()

with open(os.path.join('html', 'index.html'), 'w') as f:
    print('<h1>randomizers</h1>', file=f)
    print('<p>for the source of this project, including the randomizers, see the <a href="%s">github repo</a>' % sourcerepo, file=f)
    print('<p>', file=f)
    for (name, a) in m:
        print('<a href="algo_%s.html">%s</a><br>' % (safefile(name), name), file=f)
    print('<p><img style="max-width: 90vw; max-height: 90vh" src="similarity.png">', file=f)


keys = set()
for (name, a) in m:
    for k, v in a.items():
        keys.add(k)
        compare.addelement(name, k, v)

sim = compare.similarity()

precision = {
    'bagginess': 4,
    'bagginess6': 4,
    'diversity': 1,
    'entropy': 3,
    'evenness_diff': 3,
    'evenness_same': 3,
    'maxdrought': 1,
    'peakdrought': 1,
    'repchance': 4,
    'seq4_coverage': 4,
    'seq4_follow': 3,
}

graphqueue = []
def queuegraph(*args):
    graphqueue.append(args)
def rungraphs():
    for args in graphqueue:
        plotgraph(*args)

def plotgraph(data, imgpath):
    highx = max((t[0] for t in data), default=0) + .5
    highy = max((t[1] for t in data), default=0) * 1.1
    
    p = os.popen('''gnuplot -e 'set terminal png; set key off; plot [-.5:%f] [0:%f] "-" with boxes fill pattern 1' > %s''' % (highx, highy, imgpath), 'w')
    for k, v in sorted(data):
        p.write('%s %s\n' % (k, v))
    p.close()

with open(os.path.join('cache', 'similarity.json'), 'w') as f:
    json.dump(sim, f)

print('writing html files...')

for (name, a) in m:
    with open(os.path.join('html', 'algo_%s.html' % safefile(name)), 'w') as f:
        r = load.rands[name]
        srclink = '%s/blob/master/randos/%s.py#L%d' % (sourcerepo, r.modname, r.lineno)

        print('<p style="float: right"><a href="index.html">index</a>', file=f)
        print('<h1>%s</h1>' % name, file=f)
        print('<p>%s' % load.rands[name].desc.replace('\n', '<br>'), file=f)
        print('<p><a href="%s">source code</a>' % srclink, file=f)

        with open(os.path.join('cache', safefile(name)), 'r') as cf:
            seq = json.load(cf)['seq'][:1000]
        print('<p style="font-family: monospace; word-wrap: break-word">' + seq, file=f)

        for k, v in sorted(a.items(), key=lambda t: (t[0].endswith('_graph'), t[0])):
            lnk = '<a href="metric_%s.html">%s</a>' % (safefile(k), k)
            if k.endswith('_graph'):
                img = 'algo_%s_%s.png' % (safefile(name), safefile(k))
                queuegraph(v, os.path.join('html', img))
                v = '<br><img src="%s">' % img
            elif k in precision:
                v = ('%%.%df' % precision[k]) % v
            print('<p>%s: %s' % (lnk, v), file=f)

        print('<p>similarity: (lower is more similar) <table style="margin-left: 3em">', file=f)
        for name2, dist in sorted(sim[name].items(), key=lambda t: t[1]):
            print('<tr><td>%.3f</td><td><a href="algo_%s.html">%s</a></td></tr>' % (dist, safefile(name2), name2), file=f)
        print('</table>', file=f)

def metric_normal(key, f):
    data = []
    img = 'metric_%s.png' % safefile(key)

    print('<p style="float: right"><a href="index.html">index</a>', file=f)
    print('<h1>%s</h1>' % key, file=f)
    print('<p>%s' % analysis.desc[key], file=f)
    print('<p><img src="%s">' % img, file=f)
    print('<p><table>', file=f)
    
    m.sort(key=lambda t: t[1][key])
    for name, a in m:
        v = a[key]
        data.append(v)
        if key in precision:
            v = ('%%.%df' % precision[key]) % v
        print('<tr><td style="text-align: right">%s</td><td style="padding-left: 2em"><a href="algo_%s.html">%s</a></td></tr>' % (v, safefile(name), name), file=f)
    print('</table>', file=f)

    data = [(i, v) for i, v in enumerate(data)]
    queuegraph(data, os.path.join('html', img))

def metric_graph(key, f):
    print('<p style="float: right"><a href="index.html">index</a>', file=f)
    print('<h1>%s</h1>' % key, file=f)
    print('<p>%s' % analysis.desc[key], file=f)
    
    m.sort(key=lambda t: t[0])
    for name, a in m:
        lnk = '<a href="algo_%s.html">%s</a>' % (safefile(name), name)
        img = '<img src="algo_%s_%s.png">' % (safefile(name), safefile(key))
        print('<p>%s:<br>%s' % (lnk, img), file=f)

for key in sorted(keys):
    with open(os.path.join('html', 'metric_%s.html' % safefile(key)), 'w') as f:
        if key.endswith('_graph'):
            metric_graph(key, f)
        else:
            metric_normal(key, f)

print('plotting graphs...')
rungraphs()

print('done')
