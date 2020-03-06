'''
idea came from the way i choose shirts to wear
'''
import random

class shirts:
    '''
    pieces are chosen from the front of the list, and replaced in blocks to the back of the list.

    bagcount: the number of 7-piece bags in the list
    grab: the range from which to choose next pieces
    wash: how many pieces to remove before replacing them
    '''
    def __init__(self, bagcount=1, grab=3, wash=3):
        assert grab <= bagcount * 7 - (wash - 1)
        self.grab = grab
        self.wash = wash

        self.rack = list('jiltsoz' * bagcount)
        self.bag = []
        random.shuffle(self.rack)

    def next(self):
        p = self.rack.pop(random.randint(0, self.grab - 1))
        self.bag.append(p)
        if len(self.bag) == self.wash:
            random.shuffle(self.bag)
            self.rack += self.bag
            self.bag = []
        return p

class shirts2(shirts):
    def __init__(self):
        super().__init__(bagcount=2, grab=7, wash=7)


class shirts_smooth:
    '''
    pieces are chosen from the front of the list, and the back of the list is populated with the least populous piece type (ties are broken randomly)

    count: the number of pieces in the list
    grab: the range from which to choose next pieces
    '''
    def __init__(self, count=7, grab=3):
        assert grab <= count
        self.grab = grab

        self.rack = []
        while len(self.rack) < count:
            self.addrack()

    def addrack(self):
        d = {p: 0 for p in 'jiltsoz'}
        for p in self.rack:
            d[p] += 1
        m = min(d.values())
        lst = [p for p, n in d.items() if n == m]
        self.rack.append(random.choice(lst))

    def next(self):
        p = self.rack.pop(random.randint(0, self.grab - 1))
        self.addrack()
        return p

class shirts_smooth2(shirts_smooth):
    def __init__(self):
        super().__init__(count=14, grab=7)
