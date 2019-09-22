#!/usr/bin/python3
import random
import randos, util, minimizer, forward, steady

machines = []  # [(name, machine)]
startprobs = {}  # {name: startdict}
seqlist = []
seqlen = 100

for r in randos.funcs.values():
    name = r.__name__
    
    machine = util.findall(r, r.start)
    #machines.append((name, machine))
    
    m, groupof = minimizer.minimize(machine)
    machines.append((name + '_min', m))
    startprobs[name + '_min'] = steady.eigen(m)
    
    print(name, len(machine), len(m))

    #seqlist.append((name, util.execute(machine, r.start, seqlen)))

    #start = groupof[r.start]
    #start = random.choice(list(m.keys()))
    start = util.deal(startprobs[name + '_min'])
    seqlist.append((name + '_min', util.execute(m, start, seqlen)))

print()

for name, seq in seqlist:
    print(seq[:40] + '...', name)
    lst = []
    for name, machine in machines:
        print(name)
        p = forward.forward(machine, seq, startprobs[name])
        lst.append((p, name))

    lst.sort(reverse=True)
    for p, name in lst:
        print('   ', name, p)
    print()
