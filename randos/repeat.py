'biased randomizers'

def repeat_last_pure(history):
    'deals many copies of a piece'
    p = {c: 1 for c in 'jiltsoz'}
    if len(history) > 0:
        p[history[-1]] += 14
    return p

def repeat_recent_pure(history):
    'more likely to deal a piece that has been dealt recently'
    p = {c: 1 for c in 'jiltsoz'}
    for c in history[-14:]:
        p[c] += 1
    return p
