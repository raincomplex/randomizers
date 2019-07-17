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
    def __init__(self):
        self.size = 12
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

def wet_pure(history):
    size = 12
    if len(history) < size:
        history = list('jiltsoz') + history
    history = history[-(size-1):]
    
    for c in 'jiltsoz':
        if c not in history:
            return {c: 1}
    return {'j': 1, 'i': 1, 'l': 1, 't': 1, 's': 1, 'o': 1, 'z': 1}
