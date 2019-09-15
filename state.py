'randomizers written like weighted transition graphs'
import math, random

# function(state)
# return {(piece, newstate): weight}

randomizers = {}

def randomizer(start):
    def d(func):
        func.start = start
        randomizers[func.__name__] = func
        return func
    return d


@randomizer(frozenset())
def bag(state):
    'state = frozenset(pieces dealt from bag)'
    if len(state) == 6:
        c = (set('jiltsoz') - state).pop()
        return {(c, frozenset()): 1}
    return {(c, state | frozenset((c,))): 1 for c in 'jiltsoz' if c not in state}


@randomizer('zszs')
def tgm(state, rolls=6):
    'state = string history, most recent at end'
    p = {c: 0 for c in 'jiltsoz'}
    w = 1
    for i in range(rolls - 1):
        carry = 0
        for c in 'jiltsoz':
            if c in state:
                carry += w
            else:
                p[c] += w
        w = carry / 7
    for c in 'jiltsoz':
        p[c] += w

    return {(c, (state + c)[-4:]): w for c, w in p.items()}

@randomizer((1,) * 7)
def weight2(state):
    state = tuple(w - 1 if w > 1 else 1 for w in state)
    d = {}
    for i, w in enumerate(state):
        c = 'jiltsoz'[i]
        nxt = list(state)
        nxt[i] += 5
        if nxt[i] > 6: nxt[i] = 6  # HACK to limit the graph size
        nxt = tuple(nxt)
        d[c, nxt] = 1 / w
    return d

@randomizer(None)
def fullrandom(state):
    return {(c, None): 1 for c in 'jiltsoz'}

@randomizer(None)
def fullrandom2(state):
    'pick a random 2-gram'
    if state is None:
        return {(c, n): 1 for c in 'jiltsoz' for n in 'jiltsoz'}
    return {(state, None): 1}

@randomizer(0)
def metronome(state):
    if state == 6:
        return {('i', 0): 1}
    return {(c, state + 1): 1/6 for c in 'jltsoz'}


def execute(rand, state, count):
    'run the randomizer for count steps'
    rmap = mapstates(rand, state)
    
    r = []
    for _ in range(count):
        trans = rmap[state]

        t = sum(trans.values())
        p = random.random() * t
        new = None
        for (c, ns), w in trans.items():
            p -= w
            if p < 0:
                r.append(c)
                new = ns
                break
        state = new

    return ''.join(r)

def normalize(d):
    'takes {key: float} and returns {key: float} with the values divided by the maximum value'
    m = max(d.values())
    return {k: v / m for k, v in d.items()}

def mapstates(func, start):
    'return {state: {(piece, newstate): weight}} for all states reachable from the given state'
    trans = {}  # as return value above
    queue = [start]
    #reachable = set()
    while queue:
        state = queue.pop(0)
        if state in trans:
            continue
        trans[state] = func(state)
        for (c, ns), p in trans[state].items():
            if p > 0 and ns not in trans:
                #reachable.add(ns)
                queue.append(ns)

    # prune starting state(s)
    #queue = [start]

    return trans

def dealfromtrans(trans):
    'takes {(piece, newstate): weight} and returns {piece: weight} normalized'
    deal = {p: 0 for p in 'jiltsoz'}
    for (piece, _), w in trans.items():
        deal[piece] += w
    return normalize(deal)

def run(func, cur):
    '''
    cur = {state: weight}
    return ({state: weight}, {piece: weight})
    '''
    nxt = {}
    deal = {c: 0 for c in 'jiltsoz'}
    for state, outerw in cur.items():
        for (pc, newstate), w in func(state).items():
            w *= outerw
            if newstate not in nxt:
                nxt[newstate] = w
            else:
                nxt[newstate] += w
            deal[pc] += w

    nxt = normalize(nxt)
    deal = normalize(deal)
    return nxt, deal

def multistep(func, state, n):
    cur = func(state)
    n -= 1
    while n > 0:
        nxt = {}
        for (seq, state), outerw in cur.items():
            for (pc, newstate), w in func(state).items():
                w *= outerw
                newseq = seq + pc
                if (newseq, newstate) not in nxt:
                    nxt[newseq, newstate] = w
                else:
                    nxt[newseq, newstate] += w
        cur = nxt
        n -= 1
    return normalize(cur)

def probkey(deal):
    return ','.join('%s=%f' % (p, deal[p]) for p in 'jiltsoz')

def combine(trans):
    merged = True
    while merged:
        merged = False

        # states that come from the same states and go to the same states (not necessarily the same as the "come from" states) can be combined
        # FIXME if goto probs are equal, can merge even if comefrom is different
        # TODO other cases?
        comefrom, goto = calccomego(trans)
        link = {}  # {(comefrom, goto): state}
        for state in list(trans):
            key = (frozenset(comefrom.get(state, ())), frozenset(goto[state]))
            if key not in link:
                link[key] = state
            else:
                #print('combine', state, '->', link[key])
                trans[link[key]] = combinetrans(link[key], state, trans, comefrom)
                del trans[state]
                # any transition into state should be merged with link[key]
                for s in trans:
                    for pc, ns in list(trans[s]):
                        if ns == state:
                            w = trans[s][pc, ns]
                            del trans[s][pc, ns]
                            if (pc, link[key]) in trans[s]:
                                trans[s][pc, link[key]] += w
                            else:
                                trans[s][pc, link[key]] = w
                merged = True

        '''
        # any two states in series can be merged
        comefrom, goto = calccomego(trans)
        for state in list(trans):
            if state in comefrom and len(comefrom[state]) == 1:
                prev = list(comefrom[state])[0]
                if len(goto[prev]) == 1:
                    trans[prev] = #TODO
                    del trans[state]
        '''

        #if merged: print(trans)

    return trans

def calccomego(trans):
    comefrom = {}  # {dest: {src}}
    goto = {}  # {src: {dest}}
    for src, t in trans.items():
        for _, dest in t:
            if dest not in comefrom:
                comefrom[dest] = set()
            comefrom[dest].add(src)
            if src not in goto:
                goto[src] = set()
            goto[src].add(dest)
    return comefrom, goto

def combinetrans(a, b, trans, comefrom):
    # FIXME is this right?
    froma = [trans[s] for s in comefrom[a]]
    fromb = [trans[s] for s in comefrom[b]]
    aw = sum(w for t in froma for (_, s), w in t.items() if s == a)
    bw = sum(w for t in fromb for (_, s), w in t.items() if s == b)
    m = aw + bw
    aw /= m
    bw /= m
    c = {}
    for (pc, ns), w in trans[a].items():
        c[pc, ns] = w * aw
    for (pc, ns), w in trans[b].items():
        if (pc, ns) not in c:
            c[pc, ns] = w * bw
        else:
            c[pc, ns] += w * bw
    return c

def minimize(func, start):
    trans = mapstates(func, start)

    nextgroup = 1
    ingroup = {}  # {groupnum: {state}}
    keymap = {}  # {probkey: groupnum}

    #trans = combine(trans)

    # start with all states that look identical based on their deal probabilities
    for state, t in trans.items():
        deal = dealfromtrans(t)
        key = probkey(deal)
        if key not in keymap:
            keymap[key] = nextgroup
            ingroup[nextgroup] = set()
            nextgroup += 1
        ingroup[keymap[key]].add(state)
        #print(key, keymap[key], state)

    groupof = {}  # {state: groupnum}
    for g in ingroup:
        for state in ingroup[g]:
            groupof[state] = g

    def getkey(state):
        # we can't use func(state) here because states may have been combined
        t = trans[state]
        d = {}  # {(piece, groupnum): weight}
        for (piece, state), weight in t.items():
            g = groupof[state]
            d[piece, g] = d.get((piece, g), 0) + weight
        #d = normalize(d)  # FIXME is this necessary? it seems to have no effect
        return ','.join('%s%d=%f' % (piece, g, w) for (piece, g), w in sorted(d.items()))

    def updategroupof(g):
        for state in ingroup[g]:
            groupof[state] = g

    madesep = True
    while madesep:
        madesep = False

        for g in ingroup:
            sep = {}  # {key: {state}}
            for state in ingroup[g]:
                key = getkey(state)
                if key not in sep:
                    sep[key] = set()
                sep[key].add(state)
            #print(g, sep)

            if len(sep) > 1:
                keys = list(sep)
                ingroup[g] = sep[keys[0]]
                updategroupof(g)
                for k in keys[1:]:
                    ingroup[nextgroup] = sep[k]
                    updategroupof(nextgroup)
                    nextgroup += 1
                madesep = True
                break

    # FIXME produce a new trans map for the minimized func
    
    return ingroup

def getdistance(at, bt):
    dist = 0
    for ast, atrans in at.items():
        aprob = dealfromtrans(atrans)

        for bst, btrans in bt.items():
            bprob = dealfromtrans(btrans)
            #print(aprob)
            #print(bprob)
            #print()
            dist += dealdistance(aprob, bprob)

    return dist / (len(at) * len(bt))

def dealdistance(a, b):
    '''
    takes two deals: {piece: weight}
    return a number from 0 (they are the same) to 1 (they are inverses).
    '''
    am = sum(a.values())
    bm = sum(b.values())
    d = 0
    for p in 'jiltsoz':
        d += abs(a[p] / am - b[p] / bm)
        #d += abs(a[p] - b[p])
    return d / 7

def forward(rand, start, seq):
    trans = mapstates(rand, start)
    states = list(trans)

    comefrom = {}  # {s: {sp}}
    for sp in states:
        for c, s in trans[sp]:
            if s not in comefrom:
                comefrom[s] = set()
            comefrom[s].add(sp)

    # FIXME actual solution to this is to make mapstates() prune the initial unreachable states
    #'''
    for s in list(states):
        if s not in comefrom:
            # no state goes to this state
            states.remove(s)
            
    for s in comefrom:
        for sp in set(comefrom[s]):
            if sp not in comefrom:
                # sp was removed
                comefrom[s].remove(sp)
    #'''

    # FIXME this probably shouldn't be flat. iterate flat distribution until it settles?
    col = {s: 1/len(states) for s in states}

    tpcache = {}  # {(sp, s, c): prob}
    
    for c in seq:
        new = {}
        for i, s in enumerate(states):
            t = 0
            for sp in comefrom[s]:
                #if sp not in col:
                #    continue
                prob = tpcache.get((sp, s, c))
                if prob is None:
                    prob = getTransProb(trans[sp], s, c)
                    tpcache[sp, s, c] = prob
                t += col[sp] * prob
            new[s] = t
        col = new

    return sum(col.values())

def getTransProb(trans, s, d):
    'get the probability that we transition to state s and deal piece d'
    t = 0
    p = 0
    for (c, s2), w in trans.items():
        t += w
        if s2 == s and c == d:
            p += w
    return p / t


import sys, random

#seq = ''.join(random.choice('jiltsoz') for i in range(100))
#seq = 'jiltsoz' * 10
#seq = 'j' * 70

'''
d = {}
z = execute(bag, bag.start, 1000)
for i in range(len(z)-1):
    p = z[i:i+2]
    d[p] = d.get(p, 0) + 1
print(d)
exit(0)
'''

seqlist = []

#'''
for r in randomizers.values():
    size = len(mapstates(r, r.start))
    m = minimize(r, r.start)
    print(r.__name__, size, len(m))

    seqlist.append((r.__name__, execute(r, r.start, 100)))

print()

for name, seq in seqlist:
    print(seq[:40], name)
    lst = []
    for r in randomizers.values():
        #size = len(mapstates(r, r.start))
        p = forward(r, r.start, seq)
        lst.append((p, r.__name__))

    lst.sort(reverse=True)
    for p, name in lst:
        print('   ', name, p)
    print()
#'''

'''
states = {}
for r in randomizers.values():
    states[r] = mapstates(r, r.start)

rands = list(randomizers.values())
for i, a in enumerate(rands):
    for b in rands[i+1:]:
        at = states[a]
        bt = states[b]
        dist = getdistance(at, bt)
        print(a.__name__, b.__name__, dist)
'''

"""
if len(sys.argv) > 1:
    names = sys.argv[1:]
else:
    names = randomizers.keys()

for name in sorted(names):
    rand = randomizers[name]
    rand_start = rand.start
    print(name)

    trans = mapstates(rand, rand_start)
    maxstates = len(trans)
    print('maxstates =', maxstates)

    m = minimize(rand, rand_start)
    print('minimized =', len(m))
    '''
    for g in m:
        print(g)
        for s in m[g]:
            print('   ', s)
    '''
    
    #print('2step =', multistep(rand, rand_start, 2))
    #print('3step =', multistep(rand, rand_start, 3))

    print()
#"""

'''
uniq = {}
for state, t in trans.items():
    deal = dealfromtrans(t)
    key = ','.join('%s=%f' % (p, deal[p]) for p in 'jiltsoz')
    uniq[key] = uniq.get(key, []) + [state]

for i, key in enumerate(sorted(uniq)):
    print('#' + str(i + 1), key, len(uniq[key]))
    chunks = 16
    for i in range(0, len(uniq[key]), chunks):
        lst = uniq[key][i:i+chunks]
        print('   ', ','.join(sorted(lst)))
    print()
print(len(uniq) / maxstates, len(uniq))
'''
