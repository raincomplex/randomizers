
def pure(history):
    'equal probability regardless of history'
    return {'j': 1, 'i': 1, 'l': 1, 't': 1, 's': 1, 'o': 1, 'z': 1}

def flat(history):
    'fixed sequence'
    return {'jiltsoz'[len(history) % 7]: 1}


def bag(history):
    'standard 7-piece bag'
    used = len(history) % 7
    bag = set('jiltsoz')
    if used > 0:
        bag -= set(history[-used:])
    return {c: 1 for c in bag}


def _recent(history, op):
    p = {}
    w = 1
    for c in reversed(history):
        if c not in p:
            p[c] = w
            w = op(w)
            if len(p) == 7:
                break
    for c in 'jiltsoz':
        if c not in p:
            p[c] = w
    return p

def exp(history):
    'weighted according to recent-ness, per piece type, multiplicatively.'
    return _recent(history, lambda w: w*2)

def lin(history):
    'weighted according to recent-ness, per piece type, additively.'
    return _recent(history, lambda w: w+1)


def wet(history):
    'full random, but with drought limits'
    size = 12
    if len(history) < size:
        history = list('jiltsoz') + history
    history = history[-(size-1):]
    
    for c in 'jiltsoz':
        if c not in history:
            return {c: 1}
    return pure(history)


def nes(history):
    if len(history) > 0:
        last = history[-1]
        # 7 points to each of 'jiltsozx'
        # last and x get rerolled into 'jiltsoz' (14/7 = +2 each)
        p = {c: (9 if c != last else 2) for c in 'jiltsoz'}
    else:
        # 7 points to each of 'jiltsozx'
        # x gets rerolled into 'jiltsoz' (+1 each)
        p = {c: 8 for c in 'jiltsoz'}
    return p

def tgm(history, rolls=4, start='zzzz'):
    if len(history) == 0:
        return {'j': 1, 'i': 1, 'l': 1, 't': 1}
    
    history = history[-4:]
    if len(history) < 4:
        history = (list(start) + history)[-4:]

    p = {c: 0 for c in 'jiltsoz'}
    w = 1
    for i in range(rolls - 1):
        carry = 0
        for c in 'jiltsoz':
            if c in history:
                carry += w
            else:
                p[c] += w
        w = carry / 7
    for c in 'jiltsoz':
        p[c] += w

    return p

def tap(history):
    return tgm(history, rolls=6, start='szsz')
