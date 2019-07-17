'seamless variations on bag'

def seamless_bag_pure(history):
    bag = set('jiltsoz')
    for c in history[-7:]:
        bag.discard(c)
    if not bag:
        bag = set('jiltsoz')
    return {c: 1 for c in bag}

# TODO deep bag (a 7-piece bag which is filled from a second 7-piece bag)

def seamless_deep_pure(history):
    'a 7-piece bag which is filled from a second 7-piece bag'
    bag = list('jiltsoz'*2)
    for c in history[-7:]:
        if c in bag:
            bag.remove(c)
    return {c: bag.count(c) for c in 'jiltsoz'}

def seamless_bag2_pure(history):
    'seamless 14-piece bag'
    bag = list('jiltsoz'*2)
    for c in history[-14:]:
        if c in bag:
            bag.remove(c)
    if not bag:
        bag = list('jiltsoz')
    return {c: bag.count(c) for c in 'jiltsoz'}

def seamless_bag3_pure(history):
    'seamless 21-piece bag'
    bag = list('jiltsoz'*3)
    for c in history[-21:]:
        if c in bag:
            bag.remove(c)
    if not bag:
        bag = list('jiltsoz')
    return {c: bag.count(c) for c in 'jiltsoz'}
