import tgm

class Randomizer(tgm.Randomizer):
    def __init__(self, seed=None):
        tgm.Randomizer.__init__(self, seed=seed, rolls=6)
        self.history = [self.history[0], 1, 2, 2]

def test():
    r = Randomizer(tgm.unrand(0xeb48c724))
    goal = 'tijostzijslzijsltozjsltojzltsoizljsizlto'
    s = ''
    for i in range(len(goal)):
        s += r.next()

    print goal
    print s
    assert s == goal

if __name__ == '__main__':
    test()
