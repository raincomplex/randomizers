import util

def probkey(deal):
    return ','.join('%s=%f' % (p, deal[p]) for p in 'jiltsoz')

def minimize(machine):
    'return (minimized_machine, {state: minimized_state})'
    nextgroup = 1
    ingroup = {}  # {groupnum: {state}}
    keymap = {}  # {probkey: groupnum}

    # start with all states that look identical based on their deal probabilities
    
    for state, node in machine.items():
        deal = util.normalize(util.dealfromnode(node))
        key = probkey(deal)
        if key not in keymap:
            keymap[key] = nextgroup
            ingroup[nextgroup] = set()
            nextgroup += 1
        ingroup[keymap[key]].add(state)

    groupof = {}  # {state: groupnum}
    for g in ingroup:
        for state in ingroup[g]:
            groupof[state] = g

    # separate groups based on their observable transitions (with groups instead of states) until no separations can be made

    def getkey(state):
        d = util.normalize(getgroupnode(state))
        return ','.join('%s%d=%f' % (piece, g, w) for (piece, g), w in sorted(d.items()))

    def getgroupnode(state):
        node = machine[state]
        d = {}  # {(piece, groupnum): weight}
        for (piece, newstate), weight in node.items():
            g = groupof[newstate]
            d[piece, g] = d.get((piece, g), 0) + weight
        return d

    def updategroupof(g):
        for state in ingroup[g]:
            groupof[state] = g

    madesep = True
    while madesep:
        madesep = False

        for g in ingroup:
            sep = {}  # {key: {state}}
            for state in ingroup[g]:
                key = getkey(state)
                if key not in sep:
                    sep[key] = set()
                sep[key].add(state)

            if len(sep) > 1:
                keys = list(sep)
                ingroup[g] = sep[keys[0]]
                updategroupof(g)
                for key in keys[1:]:
                    ingroup[nextgroup] = sep[key]
                    updategroupof(nextgroup)
                    nextgroup += 1
                madesep = True
                break

    # produce a new machine from the groups
    
    newmachine = {}
    for g in ingroup:
        # it doesn't matter which state we use from the group, since they're indistinguishable
        state = next(iter(ingroup[g]))
        newmachine[g] = getgroupnode(state)

    return newmachine, groupof
