#!/usr/bin/python3
import random
import randos, util, minimizer, forward, steady

machines = []  # [(name, machine, startprobs, seq)]
seqlen = 100

for r in randos.funcs.values():
    name = r.__name__

    machine = util.findall(r, r.start)
    if len(machine) > 10000:
        print(name, len(machine))
    m, _ = minimizer.minimize(machine)

    startprobs = steady.eigen(m)

    start = util.deal(startprobs)
    seq = util.execute(m, start, seqlen)

    print(name, len(machine), len(m), seq[:40])
    machines.append((name, m, startprobs, seq))
print()

for name1, _, _, seq in machines:
    lst = []
    center = None
    for name2, machine, startprobs, _ in machines:
        p = forward.forward(machine, seq, startprobs)
        lst.append((p, name2))
        if name2 == name1:
            center = p

    lst.sort(reverse=True)
    for p, name2 in lst:
        print(name1, name2, center - p)
    print()
