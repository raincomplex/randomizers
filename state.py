'randomizers written like weighted transition graphs'
import math

# function(state)
# return {(piece, newstate): weight}

randomizers = {}

def randomizer(start):
    def d(func):
        func.start = start
        randomizers[func.__name__] = func
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


def normalize(d):
    'takes {key: float} and returns {key: float} with the values divided by the maximum value'
    m = max(d.values())
    return {k: v / m for k, v in d.items()}

def mapstates(func, state):
    'return {state: {(piece, newstate): weight}} for all states reachable from the given state'
    trans = {}  # as return value above
    queue = [state]
    while queue:
        state = queue.pop(0)
        if state in trans:
            continue
        trans[state] = func(state)
        for (c, ns), p in trans[state].items():
            if p > 0 and ns not in trans:
                queue.append(ns)
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

    trans = combine(trans)

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

    return ingroup


import sys

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

    #print('2step =', multistep(rand, rand_start, 2))
    #print('3step =', multistep(rand, rand_start, 3))

    print()

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
