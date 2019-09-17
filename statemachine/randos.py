
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
