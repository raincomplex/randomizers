'full random but with drought protection'
import random

class wet:
    def __init__(self):
        self.size = 12
        self.history = list('jiltsoz')

    def next(self):
        p = None
        for c in 'jiltsoz':
            if c not in self.history:
                p = c
                break

        if p is None:
            p = random.choice('jiltsoz')

        if len(self.history) == self.size:
            self.history.pop(0)
        self.history.append(p)

        return p

class wet2:
    def __init__(self, size=12):
        self.size = size
        self.history = list('jiltsoz')

    def next(self):
        p = None
        for c in 'jiltsoz':
            x = self.history.count(c)
            if x == 0:
                p = c
                break
            
        if p is None:
            lst = []
            for c in 'jiltsoz':
                x = self.history.count(c)
                if x == 1:
                    lst.append(c)
            if lst:
                p = random.choice(lst)

        if p is None:
            p = random.choice('jiltsoz')

        if len(self.history) == self.size:
            self.history.pop(0)
        self.history.append(p)

        return p

class wet3:
    'identical to wet2 for low history sizes (up to 14?), but unlike wet2 it will still balance counts on larger histories'
    def __init__(self, size=100):
        self.size = size
        self.history = []

    def next(self):
        d = {}
        for c in 'jiltsoz':
            d[c] = self.history.count(c)

        for i in range(0, self.size + 1):
            lst = []
            for k, c in d.items():
                if c == i:
                    lst.append(k)
            if lst:
                p = random.choice(lst)
                break

        if len(self.history) == self.size:
            self.history.pop(0)
        self.history.append(p)

        return p

def wet2_size100():
    'degrades to random'
    return wet2(size=100)

def wet3_size12():
    'identical to wet2'
    return wet3(size=12)

def wet_pure(history):
    size = 12
    if len(history) < size:
        history = list('jiltsoz') + history
    history = history[-(size-1):]
    
    for c in 'jiltsoz':
        if c not in history:
            return {c: 1}
    return {'j': 1, 'i': 1, 'l': 1, 't': 1, 's': 1, 'o': 1, 'z': 1}
