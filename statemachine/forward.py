'''
https://en.wikipedia.org/wiki/Forward_algorithm
https://web.stanford.edu/~jurafsky/slp3/ -- Speech and Language Processing, appendix chapter A. Hidden Markov Models
'''
import util

def forward(machine, seq):
    util.prune(machine)
    
    states = list(machine)

    comefrom = {}  # {s: {sp}}
    for sp in states:
        for _, s in machine[sp]:
            if s not in comefrom:
                comefrom[s] = set()
            comefrom[s].add(sp)

    # FIXME this probably shouldn't be flat. iterate flat distribution until it settles?
    col = {s: 1/len(states) for s in states}
    '''
    if start in states:
        col = {s: 0 for s in states}
        col[start] = 1
    else:
        col = {s: 1/len(states) for s in states}
    '''

    tpcache = {}  # {(sp, s, c): prob}
    
    for c in seq:
        new = {}
        for i, s in enumerate(states):
            t = 0
            for sp in comefrom[s]:
                prob = tpcache.get((sp, s, c))
                if prob is None:
                    prob = machine[sp].get((c, s), 0) / sum(machine[sp].values())
                    tpcache[sp, s, c] = prob
                t += col[sp] * prob
            new[s] = t
        col = new

    return sum(col.values())
