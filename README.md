
Uses Python 3.


## Executables

`main.py` is the main program. It generates html pages and writes them to `html`. Its intermediate products are stored in `cache`.

`graph_similarity.py` uses graphviz's `fdp` to create a visual representation of the similarity metric. Depends on the output of `main.py`.

`puretests.py` contains some tests of the pure-type randomizers.

`run-tests` is a script which runs all the unit tests.

`sample.py` generates sequences of arbitrary length from a given randomizer.

`testgame.py` is a TAP-like game for testing the randomizers. It uses [pygame](http://pygame.org).


## Library

`randos` holds the randomizers. Each file can hold multiple randomizers, but they are grouped by type.

`analysis.py` evaluates the randomizer-generated sequences according to a number of metrics.

`compare.py` performs a multidimensional distance comparison, in an attempt to quantify the similarity of the randomizers based on the reported metrics.

`pure.py` contains code related to the pure-type randomizers.

`load.py` contains the magic to load the randomizers. It also wraps ones with different interfaces so they use the standard interface.

The `piecedata` directory contains rotation system data.


## Randomizer Interfaces

`Piece = a one-character string in 'jiltsoz'`


### Standard

    class Randomizer:
        def __init__(self): pass
        def next(self): return Piece


### Pure

    History = [<Piece>]
    Weight = <float>
    
    def randomizer(History):
        return {Piece: Weight}
