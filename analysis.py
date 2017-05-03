
def analyze(s):
    a = {}
    a.update(droughts(s))
    a.update(baginess(s))
    a.update(evenness(s))
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
        #a['avgdrought_' + c] = sum(d) / float(len(d))
        a['meddrought_' + c] = d[len(d) / 2]
        a['repchance_' + c] = d.count(0) / float(len(d))
    return a

def baginess(seq):
    a = {}
    td = 0
    tb = 0
    c = 0
    for i in range(len(seq) - 6):
        b = seq[i:i+7]
        z = len(set(b))
        td += z
        if z == 7:
            tb += 1
        c += 1
    a['diversity'] = td / float(c)  # average number of unique pieces per 7-piece window
    a['bagginess'] = tb / float(c)  # % of 7-piece windows which have all 7 pieces
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
    
    avg = sum(diff) / float(len(diff))
    fdiff = sum((x - avg)**2 for x in diff)
    
    avg = sum(same) / float(len(same))
    fsame = sum((x - avg)**2 for x in same)
    
    return {
        'evenness_diff': fdiff,
        'evenness_same': fsame,
    }
