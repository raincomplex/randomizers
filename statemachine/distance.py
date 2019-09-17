#!/usr/bin/python3
import randos, util, minimizer, forward

seqlist = []

for r in randos.funcs.values():
    machine = util.findall(r, r.start)
    size = len(machine)
    m = minimizer.minimize(machine)
    print(r.__name__, size, len(m))

    seqlist.append((r.__name__, util.execute(machine, r.start, 100)))

print()

for name, seq in seqlist:
    print(seq[:40], name)
    lst = []
    for r in randos.funcs.values():
        machine = util.findall(r, r.start)
        p = forward.forward(machine, seq)
        lst.append((p, r.__name__))

    lst.sort(reverse=True)
    for p, name in lst:
        print('   ', name, p)
    print()
