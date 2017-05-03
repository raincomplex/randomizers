
class Randomizer:
    def __init__(self):
        self.bag = 'jiltsoz'
        self.i = 0
    
    def next(self):
        p = self.bag[self.i]
        self.i = (self.i + 1) % len(self.bag)
        return p
