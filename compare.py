import math

vectors = {}
logarithmic = set(['evenness_diff', 'evenness_same'])
exclude_compare = set('drought_graph'.split())

def addelement(name, key, value):
    if name not in vectors:
        vectors[name] = {}
    vectors[name][key] = value

def similarity():
    # find ranges
    mins = {}
    maxes = {}
    for name, d in vectors.items():
        for k, v in d.items():
            if k in exclude_compare:
                continue
            if k not in mins or v < mins[k]:
                mins[k] = v
            if k not in maxes or v > maxes[k]:
                maxes[k] = v

    # normalize
    for name, d in vectors.items():
        for k, v in list(d.items()):
            if k in exclude_compare:
                continue
            n = (v - mins[k]) / (maxes[k] - mins[k])
            if k in logarithmic:
                n = math.log(1 + n, 2)
            d[k] = n

    with open('similarity.txt', 'w') as f:
        print(file=f)
        for name, d in sorted(vectors.items()):
            print(name, file=f)
            lst = []
            for name2, d2 in vectors.items():
                if name != name2:
                    z = distance(d, d2)
                    lst.append((z, name2))
            for z, name2 in sorted(lst):
                print('    %.3f  %s' % (z, name2), file=f)
            print(file=f)
    print('wrote similarity.txt')

def distance(v1, v2):
    assert set(v1) == set(v2)
    s = 0
    for k in v1:
        if k in exclude_compare:
            continue
        s += (v1[k] - v2[k])**2
    return s
