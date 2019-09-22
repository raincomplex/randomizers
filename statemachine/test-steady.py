#!/usr/bin/python3
import randos, steady, util, minimizer

usemin = False
showStatesThreshold = 10

for name, r in randos.funcs.items():
    machine = util.findall(r, r.start)
    if usemin:
        machine, _ = minimizer.minimize(machine)

    start = steady.eigen(machine)
    count = {}  # {prob: [state]}
    for state, prob in start.items():
        prob = round(prob, 10)
        if prob not in count:
            count[prob] = []
        count[prob].append(state)

    print(name)
    for prob, states in sorted(count.items()):
        print('%.10f %d' % (prob, len(states)))
        if len(states) < showStatesThreshold:
            print('   ', str(states)[1:-1])
    print()
