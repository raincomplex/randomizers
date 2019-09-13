
Uses Python 3.

You can see the output of this project [here](http://raincomplex.github.io/randomizers).


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

`Piece := a one-character string in 'jiltsoz'`


### Standard

    randomizer() : <Stream>
    Stream.next() : <Piece>

`randomizer` is a callable which returns a stream. A stream is an object with a member function, `next`, that returns the next piece in the sequence.


### Pure

    History := [<Piece>]
    Weight := <float>
    
    randomizer(<History>) : {<Piece>: <Weight>}

`randomizer` is a callable which takes a history, which is a list of pieces, and returns a dict mapping pieces to weights.

A given history must always produce the same piece weights. This is what makes these randomizers "pure".

The sum of the weights must be greater than 0 but needn't be 1. Pieces may be left out; missing pieces are assumed to have weight 0.
