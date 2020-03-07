
# function(state)
# return {(piece, newstate): weight}

funcs = {}  # {name: function}

def randomizer(start):
    def d(func):
        func.start = start
        funcs[func.__name__] = func
        return func
    return d


@randomizer(frozenset())
def bag(state):
    'state = frozenset(pieces dealt from bag)'
    if len(state) == 6:
        c = (set('jiltsoz') - state).pop()
        return {(c, frozenset()): 1}
    return {(c, state | frozenset((c,))): 1 for c in 'jiltsoz' if c not in state}

@randomizer('x')
def nes(state):
    d = {}
    for p in 'jiltsoz':
        # 1/8 pure random OR rerolled OR straight rolled
        d[p, p] = 2 + (7 if state != p else 0)
    return d

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

@randomizer(0)
def flatbag(state):
    return {('jiltsoz'[state], (state + 1) % 7): 1}

@randomizer(0)
def flipflop(state):
    if state == 0:
        return {
            ('j', 0): 3, ('l', 0): 3, ('t', 0): 3, ('i', 0): 3,
            ('j', 1): 1, ('l', 1): 1, ('t', 1): 1, ('i', 1): 1,
        }
    else:
        return {
            ('s', 1): 3, ('o', 1): 3, ('z', 1): 3, ('i', 1): 3,
            ('s', 0): 1, ('o', 0): 1, ('z', 0): 1, ('i', 0): 1,
        }

@randomizer('x')
def repeat_last(state):
    return {(p, p): (15 if p == state else 1) for p in 'jiltsoz'}

# randomizers which are too large
'''
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

@randomizer('jiltsoz')
def wet(state):
    for c in 'jiltsoz':
        if c not in state:
            return {(c, state[-6:] + c): 1}
    p = {}
    for c in 'jiltsoz':
        p[c, state[-6:] + c] = 1
    return p
'''
