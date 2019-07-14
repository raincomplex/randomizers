import math

def analyze(s):
    a = {}
    a.update(droughts(s))
    a.update(baginess(s))
    a.update(evenness(s))
    a.update(entropy(s))
    return a

def droughts(seq):
    a = {}
    for c in 'jiltsoz':
        d = [len(s) for s in seq.split(c)]
        
        # remove false repeats at ends of the sequence
        if seq[0] == c:
            assert d[0] == 0
            d.pop(0)
        if seq[-1] == c:
            assert d[-1] == 0
            d.pop()
        
        d.sort()
        
        a['maxdrought_' + c] = d[-1]
        #a['avgdrought_' + c] = sum(d) / len(d)
        a['meddrought_' + c] = d[int(len(d) / 2)]
        a['repchance_' + c] = d.count(0) / len(d)
    
    a['maxdrought'] = sum(a['maxdrought_' + c] for c in 'jiltsoz') / 7
    a['meddrought'] = sum(a['meddrought_' + c] for c in 'jiltsoz') / 7
    a['repchance'] = sum(a['repchance_' + c] for c in 'jiltsoz') / 7
    
    return a

def baginess(seq):
    a = {}
    td = 0
    tb = tb6 = 0
    c = 0
    for i in range(len(seq) - 6):
        b = seq[i:i+7]
        z = len(set(b))
        td += z
        if z == 7:
            tb += 1
        if z >= 6:
            tb6 += 1
        c += 1
    a['diversity'] = td / c  # average number of unique pieces per 7-piece window
    a['bagginess'] = tb / c  # % of 7-piece windows which have all 7 pieces
    a['bagginess6'] = tb6 / c  # % of 7-piece windows which have at least 6 pieces
    return a

def evenness(seq):
    'measure the evenness of the distribution of pairs of pieces'
    same = []
    diff = []
    for x in 'jiltsoz':
        for y in 'jiltsoz':
            n = seq.count(x + y)
            if x == y:
                same.append(n)
            else:
                diff.append(n)
    
    avg = sum(diff) / len(diff)
    fdiff = sum((x - avg)**2 for x in diff)
    
    avg = sum(same) / len(same)
    fsame = sum((x - avg)**2 for x in same)
    
    return {
        'evenness_diff': fdiff,
        'evenness_same': fsame,
    }

def entropy(seq):
    d = {}
    total = 0
    size = 6  # produces the largest spread
    for i in range(len(seq) - size + 1):
        x = seq[i:i+size]
        d[x] = d.get(x, 0) + 1
        total += 1

    e = 0
    for x, c in d.items():
        p = c / total
        e -= p * math.log(p)

    return {
        'entropy': e,
    }
