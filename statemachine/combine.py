'possibly doomed attempt at maximizing the effect of the minimizer'

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
