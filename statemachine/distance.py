#!/usr/bin/python3
import randos, util, minimizer, forward

machines = []  # [(name, machine)]
seqlist = []
seqlen = 100

for r in randos.funcs.values():
    name = r.__name__
    
    machine = util.findall(r, r.start)
    #machines.append((name, machine))
    
    m, groupof = minimizer.minimize(machine)
    newstart = groupof[r.start]
    machines.append((name + '_min', m))
    
    print(name, len(machine), len(m))

    #seqlist.append((name, util.execute(machine, r.start, seqlen)))
    seqlist.append((name + '_min', util.execute(m, newstart, seqlen)))

print()

for name, seq in seqlist:
    print(seq[:40] + '...', name)
    lst = []
    for name, machine in machines:
        p = forward.forward(machine, seq)
        lst.append((p, name))

    lst.sort(reverse=True)
    for p, name in lst:
        print('   ', name, p)
    print()
