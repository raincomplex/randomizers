import math

vectors = {}
logarithmic = set(['evenness_diff', 'evenness_same'])

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
            if k not in mins or v < mins[k]:
                mins[k] = v
            if k not in maxes or v > maxes[k]:
                maxes[k] = v

    # normalize
    for name, d in vectors.items():
        for k, v in list(d.items()):
            n = (v - mins[k]) / float(maxes[k] - mins[k])
            if k in logarithmic:
                n = math.log(1 + n, 2)
            d[k] = n

    for name, d in sorted(vectors.items()):
        print name
        lst = []
        for name2, d2 in vectors.items():
            if name != name2:
                z = distance(d, d2)
                lst.append((z, name2))
        for z, name2 in sorted(lst):
            print '    %.3f  %s' % (z, name2)
        print

def distance(v1, v2):
    assert set(v1) == set(v2)
    s = 0
    for k in v1:
        s += (v1[k] - v2[k])**2
    return s
