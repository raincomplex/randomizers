# from https://tetrisconcept.net/threads/randomizer-theory.512/page-9#post-55478

# PETE ROOLZ
#
# you can get a quick sequence out with
# python -c 'import tgm; r = tgm.TiRandomizer(); print "".join([r.next() for i in range(70)])'
#
# sample 1000-piece sequence:
#
# jlosiztjsozlijsotilsjtzoijtzlojsiztoljstiltzosjtzoiljzoslitjslizjsotlziosjlztsj
# itlojztisozlitosjlizojtlzsotjislotjzlitsjoziljsoztlijsotilzstojzziiljsztljiotsj
# iolszjotszjiloztisojlsztoiszljitzosltjijzosilzjtioszltjisotjilzostlzjoistjzilos
# jtliozstjolstziljlsotslzjisozjitoilstzolitzjsioljztoljsztoisjltiszloijztolszito
# jzilsjztisjltozsijoltzsoijlztijsotliszjloitzjoltsizjlsioojtzsloijszoitjzsltoijz
# ltisoltjzsilitosjizoltjzosltjoisztljsitlzjosiltozijltosiztjsilojztlsjiozstjizsl
# oitjslotzjliozjstlziosljtoszijtlziojlzstilozjstiljsziojtsloitzsosizjtolzjsoizjt
# sliotzjlstiolstzojloizjtsiljzsoijzstoljsitzoslijoztsijoztllsitzlosjzijtlsojtilz
# osijtzlsotzisojtilozjtisllozsjlotijsolztijlsozjtsizjositljsztijlzoitsjozltjsilo
# zjstiolzstjlosiztlojlsitzosjizltojsilzjsilztsoijozltjsolzitsljioszjitolzsitljsz
# toljsitzolijszotjlsizjoltisojtzslztislzoiojztilsjtolsjztiosljziotjzisotzisjtlzs
# oiljtzoijtszloostijoslzitjoolszijosztloijtsziljositjzsltjoilzzositzosjtzoijlzsi
# tlojstzliotslzjozisltjisztljizotjisolzjistljoisltozo


import random
import collections

# On a Ti randomizer bug:
#
# > When these 3 conditions are met:
# >
# >     1. The randomizer has just chosen the most droughted piece
# >     2. A reroll happened during the choice of that piece.
# >     3. Excluding the first piece of the game, and including this chosen piece, you have received at least one of each of the 7 piece types.
# >
# > Then the roll that chose that most droughted piece will not update the bag of 35 pieces.
#
# -- colour_thief, http://tetrisconcept.net/threads/randomizer-theory.512/page-7

def Randomizer():
    bag = ['j', 'i', 'z', 'l', 'o', 't', 's'] * 5
    history = collections.deque(['s', 'z', 's', 'z'])
    drought_order = ['j', 'i', 'z', 'l', 'o', 't', 's']
    count = { 'j' : 0, 'i' : 0, 'z' : 0, 'l' : 0, 'o' : 0, 't' : 0, 's' : 0 }
    n = 1

    # first piece is special
    first = random.choice(['j','i','l','t'])
    history.popleft()
    history.append(first)
    yield first

    while True:
        for roll in range(6):
            i = random.randint(0, 34)
            piece = bag[i]
            if piece not in history:
                break
            if roll < 5:
                bag[i] = drought_order[0]
        count[piece] += 1
        emulate_bug = all ([
            piece == drought_order[0],
            roll > 0,
            0 not in count.values()
            ])
        if not emulate_bug:
            bag[i] = drought_order[0]
        drought_order.remove(piece)
        drought_order.append(piece)
        history.popleft()
        history.append(piece)
        yield piece

if __name__ == '__main__':
    r = Randomizer()
    print "".join([r.next() for i in range(70)])
