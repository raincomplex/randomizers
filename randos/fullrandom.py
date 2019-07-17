'equal probability regardless of history'
import random

class fullrandom:
    def next(self):
        return random.choice('jiltsoz')

def fullrandom_pure(history):
    return {'j': 1, 'i': 1, 'l': 1, 't': 1, 's': 1, 'o': 1, 'z': 1}
