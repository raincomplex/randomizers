import math
from collections import Counter

desc = {}

def analyze(s):
    a = {}
    a.update(droughts(s))
    a.update(baginess(s))
    a.update(evenness(s))
    a.update(entropy(s))
    a.update(follow(s))
    return a


def droughts(seq):
    a = {}
    dc = Counter()
    
    for c in 'jiltsoz':
        d = [len(s) for s in seq.split(c)]
        
        # remove false repeats at ends of the sequence
        if seq[0] == c:
            assert d[0] == 0
            d.pop(0)
        if seq[-1] == c:
            assert d[-1] == 0
            d.pop()
        
        dc.update(d)

        peak = max(Counter(d).items(), key=lambda t: t[1])[0]
        
        a['maxdrought_' + c] = max(d)
        a['peakdrought_' + c] = peak
        a['repchance_' + c] = d.count(0) / len(d)
    
    a['maxdrought'] = sum(a['maxdrought_' + c] for c in 'jiltsoz') / 7
    a['peakdrought'] = sum(a['peakdrought_' + c] for c in 'jiltsoz') / 7
    a['repchance'] = sum(a['repchance_' + c] for c in 'jiltsoz') / 7

    total = sum(dc.values())
    a['drought_graph'] = [(k, v / total) for k, v in dc.items()]
    
    return a

desc['maxdrought'] = 'longest time between two of the same piece (avg across 7 piece types)'
desc['peakdrought'] = 'most common time between two of the same piece (avg across 7 piece types)'
desc['repchance'] = 'chance of getting the same piece twice in a row (avg across 7 piece types)'
desc['drought_graph'] = 'histogram of drought times'


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
    a['diversity'] = td / c
    a['bagginess'] = tb / c
    a['bagginess6'] = tb6 / c
    return a

desc['diversity'] = 'average number of unique pieces per 7-piece window'
desc['bagginess'] = 'percent of 7-piece windows which have all 7 pieces'
desc['bagginess6'] = 'percent of 7-piece windows which have at least 6 pieces'


def evenness(seq):
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
        'evenness_diff': math.log(fdiff + 1, 10),
        'evenness_same': math.log(fsame + 1, 10),
    }

desc['evenness_diff'] = 'sum of squares on distribution of pairs of different pieces (log)'
desc['evenness_same'] = 'sum of squares on distribution of pairs of same pieces (log)'


def follow(seq):
    d = {}
    size = 4
    for i in range(len(seq) - size):
        a = seq[i:i+size]
        b = seq[i+size]
        if a not in d:
            d[a] = {}
        if b not in d[a]:
            d[a][b] = 0
        d[a][b] += 1

    even = 0
    for a in d:
        z = 0
        for b in d[a]:
            z += d[a][b]
        z /= 7
        s = 0
        for b in d[a]:
            s += (d[a][b] - z) ** 2
        even += s

    return {
        'follow_coverage': len(d) / (7 ** size),
        'follow_even': math.log(even + 1, 10),
    }

desc['follow_coverage'] = 'percent of 4-piece sequences that occur'
desc['follow_even'] = 'for each 4-piece sequence, sum of squares on the distribution of the next piece (log)'


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

desc['entropy'] = 'computed by counting unique 6-piece sequences'
