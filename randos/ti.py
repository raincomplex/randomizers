import random, time, sys, unittest

pieces = 'izsjlot'

def rand_type0(seed):
    while True:
        seed = ((seed * 1103515245) + 12345) & 0xffffffff
        yield (seed >> 10) & 0x7fff

class ti:
    def __init__(self, seed=None):
        if seed == None:
            seed = int(time.time())

        self.rand = rand_type0(seed)
        self.bag = [int(x/5) for x in range(35)]
        self.droughts = [4] * 7
        self.history = [1, 1, 2, 2]
        self.max_drought = 0
        self.replacement_piece = 0
        self.first = True

    def replace_bag(self, i):
        for n in range(7):
            if self.max_drought < self.droughts[n]:
                self.max_drought = self.droughts[n]
                self.replacement_piece = n
        self.bag[i] = self.replacement_piece

    def next(self):
        if self.first:
            result = next(self.rand) % 7
            while result in (1, 2, 5):
                result = next(self.rand) % 7
                if result != 1 and result != 2 and result != 5:
                    break
            self.history[0] = result
            self.first = False
            return pieces[result]

        self.max_drought = 0
        self.replacement_piece = 0

        for roll in range(6):
            n = next(self.rand) % 35
            result = self.bag[n]
            if result not in self.history:
                break
            self.replace_bag(n)
            n = next(self.rand) % 35
            result = self.bag[n]

        for piece in range(7):
            self.droughts[piece] += 1
        self.droughts[result] = 0

        self.replace_bag(n)

        self.history.pop()
        self.history.insert(0, result)

        return pieces[result]


demo_seed = 0x1106 # generates attract mode player 1 sequence

class Tests(unittest.TestCase):
    def testPRNG(self):
        rng = rand_type0(0x4321)
        for v in [
                0x6116d346, 0x793b7907, 0x1f9cda34, 0x387cf05d, 0xa35cddd2, 0xbc8c9ea3,
                0x354765a0, 0xaa1d3559, 0x3087051e, 0x604081ff, 0xed4d3bcc, 0x9de2ce15,
                0x0d9a552a, 0x59253f1b, 0xf7f848b8, 0x312f3691, 0x58e099f6, 0xd0ceb1f7,
                0x3e453864, 0x9bffaacd, 0x79745f82, 0x0c327693, 0x9a4f76d0, 0x9ee926c9,
                0xbb8cf1ce, 0x2003e8ef, 0xaa7d2ffc, 0xd4d46685, 0x658a5cda, 0x8ed0250b,
                0xab6b4fe8, 0x6479e601, 0x11c16ca6, 0xacda06e7, 0x04998294, 0x4d9de13d,
                0xd907ad32, 0x65b62a83, 0xf3d63400, 0x4e0c5439, 0x99ff6a7e, 0xbfa6ebdf,
                0x836a902c, 0x1a54faf5, 0x6923b08a, 0x38b866fb, 0xb7068318, 0x66475171,
                0xf5944b56, 0xd99c77d7, 0x9b6cb8c4, 0xf92e93ad, 0x6ea1c6e2, 0x9a46ba73,
                0xa4de9d30, 0xc9cdbda9, 0x36196f2e, 0x74488acf, 0x88485c5c, 0xde1b8b65,
                0x6b51503a, 0x3eed04eb, 0x7b2ce248, 0x6abe78e1, 0x1af43606, 0x311504c7,
                0x8651daf4, 0x6e48c21d, 0x9f8dac92, 0xa4d32663, 0x572bb260, 0xc4346319,
                0x7ed5ffde, 0x78c7c5bf, 0xbc09948c, 0x6b9f17d5, 0xcfbe3bea, 0x2b3cfedb,
                0xb7016d78, 0x7dc65c51, 0xf53c2cb6, 0x8b02adb7, 0xd39be924, 0x10436c8d,
                0x39d65e42, 0x9a0a6e53, 0x2b407390, 0xff074489, 0x97f01c8e, 0xfdc39caf,
                0x446138bc, 0x5a16a045, 0xbad5739a, 0x193754cb, 0xb86724a8, 0xf305fbc1,
                0x04872f66, 0xace472a7, 0x4c5de354, 0x463592fd, 0x2446dbf2, 0x985b9243,
                0xe85fe0c0, 0xbbcd61f9, 0x89e2c53e, 0x199b0f9f, 0x99c248ec, 0xfc7924b5,
                0xc1c1f74a, 0xa62b06bb, 0x8c0107d8, 0xd5e45731, 0x85b03e16, 0x39f95397,
                0xa46ac984, 0xeaf6356d, 0x0e6a25a2, 0xb7f59233, 0x2c8cf9f0, 0x2bcdbb69,
                0xf1e8f9ee, 0xb86d1e8f, 0xb75fc51c, 0xd17da525, 0x9a6ec6fa, 0xe12714ab,
                0x2d321708, 0x59886ea1, 0x225258c6, 0xa3405087, 0xaa559bb4
        ]:
            assert next(rng) == (v >> 10) & 0x7fff

    def testPieceSequence(self):
        rng = ti(demo_seed)
        for piece in 'jltiojslzijtolzstiojstizojlstzilsto':
            assert rng.next() == piece

def main():
    seed = demo_seed
    if len(sys.argv) > 1:
        seed = int(sys.argv[1])
    rng = Randomizer(seed)
    print(''.join(next(rng) for n in range(70)))
    
if __name__ == '__main__':
    main()
