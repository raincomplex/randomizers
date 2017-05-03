import time

pieces = 'izsjlot'

def rand(n):
    return (n * 0x41c64e6d + 12345) & 0xffffffff

def unrand(n):
    return ((n - 12345) * 0xeeb9eb65) & 0xffffffff

class Randomizer:
    def __init__(self, seed=None):
        if seed == None:
            seed = int(time.time())
        self.seed = seed

        b = 1
        while b == 1 or b == 2 or b == 5:
            b = self.read() % 7
        self.history = [b, 1, 2, 2]

    def read(self):
        self.seed = rand(self.seed)
        return (self.seed >> 10) & 0x7fff

    def next(self):
        r = self.history[0]
        
        for i in range(5):
            b = self.read() % 7
            if b not in self.history:
                break
            b = self.read() % 7
            
        self.history.pop()
        self.history.insert(0, b)

        return pieces[r]

def test():
    r = Randomizer(unrand(0xeb48c724))
    goal = 'tijostzijslzijsltozjsltojzltsoizljsizlto'
    s = ''
    for i in range(len(goal)):
        s += r.next()

    print goal
    print s
    assert s == goal

if __name__ == '__main__':
    test()
