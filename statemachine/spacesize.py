#!/usr/bin/python3
import math, random
import randos, minimizer, util, forward, steady

def main():
    seqlen = 100
    print('seqlen', seqlen)
    print()

    full = 7 ** seqlen
    
    for name in randos.funcs:
        r = randos.funcs[name]
        machine = util.findall(r, r.start)
        machine, _ = minimizer.minimize(machine)

        print(name)
        if seqlen <= 8 and len(machine) < 200:
            x = exact(machine, seqlen)
            print('exact', x, x / full)
        small, avg, large = heuristic(machine, seqlen)
        print('heuristic', small / full, avg / full, large / full)
        print()


def exact(machine, seqlen):
    possible = set()
    def countpossible(state, sofar):
        for p, nxt in machine[state]:
            if len(sofar) < seqlen - 1:
                countpossible(nxt, sofar + p)
            else:
                possible.add(sofar + p)

    for state in machine:
        countpossible(state, '')

    return len(possible)


def heuristic(machine, seqlen, count=100):
    startprobs = steady.eigen(machine)
    exps = []

    for _ in range(count):
        state = util.deal(startprobs)
        seq = util.execute(machine, state, seqlen)
        p = forward.forward(machine, seq, startprobs)
        exps.append(-p)

    small = min(exps)
    large = max(exps)

    avg = 2**small * (sum(2**(p-small) for p in exps) / len(exps))

    def makeint(p):
        if p == math.inf:
            return math.inf
        return int(2**p)

    return makeint(small), int(avg), makeint(large)


if __name__ == '__main__':
    main()
