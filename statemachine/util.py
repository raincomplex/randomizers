import random

# machine = {state: node}
# node = {(piece, newstate): weight}

def execute(machine, state, count):
    'run the randomizer for count steps. returns a string of dealt pieces.'
    dealt = []
    for _ in range(count):
        node = machine[state]
        
        r = random.random() * sum(node.values())
        found = False
        for (piece, newstate), weight in node.items():
            r -= weight
            if r < 0:
                dealt.append(piece)
                state = newstate
                found = True
                break
        assert found

    return ''.join(dealt)

def normalize(d):
    'takes {key: float} and returns {key: float} with the values divided by the maximum value'
    m = max(d.values())
    return {k: v / m for k, v in d.items()}

def findall(func, start):
    'return {state: {(piece, newstate): weight}} for all states reachable from the given state'
    machine = {}  # as return value above
    queue = [start]
    while queue:
        state = queue.pop(0)
        if state in machine:
            continue
        machine[state] = func(state)
        for (piece, newstate), weight in machine[state].items():
            if weight > 0 and newstate not in machine:
                queue.append(newstate)
    return machine

def prune(machine):
    'remove states which aren\'t part of any cycles. modifies argument in-place'
    back = {}
    for state in machine:
        for _, newstate in machine[state]:
            if newstate not in back:
                back[newstate] = set()
            back[newstate].add(state)

    chop = set()
    for state in machine:
        if state not in back:
            # nothing goes to state
            chop.add(state)

    while chop:
        state = chop.pop()
        for _, newstate in machine[state]:
            back[newstate].remove(state)
            if not back[newstate]:
                chop.add(newstate)
        del machine[state]

    return None

def dealfromnode(node):
    'takes {(piece, newstate): weight} and returns {piece: weight}'
    deal = {p: 0 for p in 'jiltsoz'}
    for (piece, _), weight in node.items():
        deal[piece] += weight
    return deal
