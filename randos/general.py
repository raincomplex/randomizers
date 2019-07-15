
from general.main import *

# binding r by returning a local function from a factory function causes pickling to fail ("can't pickle local"), so use a callable class instead

class Factory:
    def __init__(self, r):
        self.r = r
        self.__doc__ = r.__name__

    def __call__(self):
        return Stream(self.r)

n = 1
for r in listrandos():
    globals()['factory' + str(n)] = Factory(r)
    n += 1
