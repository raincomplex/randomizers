'fixed sequence'

seq = 'jiltsoz'

class flatbag:
    def __init__(self):
        self.i = 0
    
    def next(self):
        p = seq[self.i]
        self.i = (self.i + 1) % len(seq)
        return p

def flatbag_pure(history):
    if len(history) == 0:
        return {'j': 1}
    c = seq.index(history[-1])
    return {seq[(c + 1) % 7]: 1}
