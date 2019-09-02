'functions for analyzing randomizers in an abstract way'
import math
import load, pure

def calcdepth(r, n, fuzz):
    '''
    calculate conditional entropy
    
    r = pure randomizer function
    n = history size
    fuzz = amount of rounding to apply to probabilities (2 = round to nearest percent)
    
    return float depth
    '''

    d = {}
    history = ['j'] * n
    change = {'j':'i', 'i':'l', 'l':'t', 't':'s', 's':'o', 'o':'z', 'z':'j'}
    
    for i in range(7 ** n):
        for k in range(n):
            history[k] = change[history[k]]
            if history[k] != 'j':
                break

        prob = r(history)
        s = ','.join('%s=%s' % (p, round(prob.get(p, 0), fuzz)) for p in 'jiltsoz')
        d[s] = d.get(s, 0) + 1

    return math.log(len(d), 7)


if __name__ == '__main__':
    import sys

    DEPTH = int(sys.argv[1])
    ROUND = 2

    scores = {}
    for name, rando in load.rands.items():
        if type(rando) is pure.Factory:
            depth = calcdepth(rando.r, DEPTH, ROUND)
            print(name, depth)
            scores[name] = depth
    print()

    for name, score in sorted(scores.items(), key=lambda t: t[1]):
        print('%.3f' % score, name)
