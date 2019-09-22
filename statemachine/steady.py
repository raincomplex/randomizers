import numpy as np
import scipy.sparse, scipy.sparse.linalg

def machinetomatrix(machine):
    'return (matrix, {index: state})'
    m = scipy.sparse.dok_matrix((len(machine), len(machine)), np.float64)

    i = 0
    statenum = {}  # {state: index}
    indextostate = {}  # {index: state}
    for state in machine:
        statenum[state] = i
        indextostate[i] = state
        i += 1

    for state in machine:
        weights = {}  # {state: weight}
        for (_, nxt), w in machine[state].items():
            weights[nxt] = weights.get(nxt, 0) + w
        total = sum(weights.values())

        src = statenum[state]
        for nxt, w in weights.items():
            m[statenum[nxt], src] = w / total

    return m, indextostate

def eigen(machine):
    'get a steady state with linear algebra'
    if len(machine) <= 2:
        # FIXME 2 states might not always be even, and should be easy to solve specifically
        return {s: 1 for s in machine}
    
    m, its = machinetomatrix(machine)
    _, vecs = scipy.sparse.linalg.eigs(m, k=1, which='LR')  # get 1 result, Largest Real part
    vec = vecs.flatten().real
    vec /= sum(vec)

    start = {}
    for i, p in enumerate(vec):
        start[its[i]] = p
    return start


def iterate(machine):
    'naive method by choosing a random starting vector and just iterating, doesn\'t work all the time'
    comefrom = util.reverse(machine)
    
    probs = [random.random() for s in machine]
    total = sum(probs)
    col = {s: probs.pop(0) / total for s in machine}
    #col = {s: 1/len(machine) for s in machine}
    
    tpcache = {}  # {(sp, s): prob}
    maxdist = 1
    itercount = 100
    while maxdist > 1e-10 and itercount > 0:
        new = {}
        for s in machine:
            t = 0
            for sp in comefrom[s]:
                prob = tpcache.get((sp, s))
                if prob is None:
                    prob = 0
                    total = sum(machine[sp].values())
                    for c in 'jiltsoz':
                        prob += machine[sp].get((c, s), 0)
                    prob /= total
                    tpcache[sp, s] = prob
                t += col[sp] * prob
            new[s] = t
        maxdist = max(abs(new[s] - col[s]) for s in machine)
        last = col
        col = new
        itercount -= 1
    '''
    print(maxdist, itercount)
    if len(machine) == 8:
        print(last)
        print(col)
    #'''
    return col
