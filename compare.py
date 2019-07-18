import math

default_weight = 1
weights = {
    #'bagginess6': 1,
    #'peakdrought': 1,
}

# end config


vectors = {}
exclude_compare = set([k for k in weights if weights[k] == 0])

def addelement(name, key, value):
    # don't compare graphs
    if key.endswith('_graph'):
        weights[key] = 0
        exclude_compare.add(key)

    if name not in vectors:
        vectors[name] = {}
    vectors[name][key] = value

def similarity():
    'return {name: {name: distance}}'
    
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
            if maxes[k] != mins[k]:
                n = (v - mins[k]) / (maxes[k] - mins[k])
            else:
                n = 0
            d[k] = n

    # compute distances
    r = {}
    for name, d in vectors.items():
        r2 = {}
        for name2, d2 in vectors.items():
            if name != name2:
                z = distance(d, d2)
                r2[name2] = z
        r[name] = r2
    return r

def distance(v1, v2):
    assert set(v1) == set(v2)
    s = 0
    for k in v1:
        if k in exclude_compare:
            continue
        s += weights.get(k, default_weight) * (v1[k] - v2[k])**2
    return s
