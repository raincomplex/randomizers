#!/usr/bin/python2
import pygame, sys, time
import load

resolution = (640, 480)

binds = {
    pygame.K_n: 'reset',
    
    pygame.K_LEFT: 'left',
    pygame.K_RIGHT: 'right',
    pygame.K_UP: 'up',
    pygame.K_DOWN: 'down',
    pygame.K_z: 'ccw',
    pygame.K_x: 'cw',
    pygame.K_c: 'ccw',
    
    pygame.K_KP4: 'left',
    pygame.K_KP6: 'right',
    pygame.K_KP8: 'up',
    pygame.K_KP5: 'down',
    pygame.K_q: 'ccw',
    pygame.K_e: 'cw',
}

import piecedata.ars as rotsys

# end config

flags = set()

for f in ['20g']:
    if f in sys.argv:
        sys.argv.remove(f)
        flags.add(f)

if len(sys.argv) == 2:
    Randomizer = load.rands[sys.argv[1]]
else:
    print 'Usage: %s RANDOMIZER [OPTIONS...]' % sys.argv[0]
    print
    print 'Randomizers:'
    for name in sorted(load.rands):
        print '    ' + name
    print
    print 'Options:'
    print '    20g'
    print
    exit(1)

class Game:
    def __init__(self):
        self.rand = Randomizer()
        self.well = {(x, y): None for x in range(10) for y in range(20)}
        self.active = None
        self.score = [0] * 4
        self.pieces = 0
        self.over = False
        
        self.previews = []
        for i in range(3):
            self.previews.append(self.rand.next())
        
        # parameters
        self.spawn = 20
        self.lock = 30
        self.das = 12
        self.gravity = .1
        if '20g' in flags:
            self.gravity = 20

        # timers
        self.timer = 0  # spawn or lock depending on if active is set
        self.dastimer = 0
        self.dasdir = 0  # 0, -1, 1
        self.gravitytimer = 0

class Piece: pass

spawnpos = rotsys.spawnpos
piecedata = rotsys.pieces
piececolor = rotsys.colors

# event handling

def handleEvents():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            keyPressed(event.key)
        elif event.type == pygame.KEYUP:
            keyReleased(event.key)
        elif event.type == pygame.QUIT:
            exit()

held = {}
for b in binds.values():
    held[b] = False

def keyPressed(key):
    global game
    if key in binds:
        b = binds[key]
        held[b] = True
        
        if b == 'reset':
            game = Game()
        elif not game.over:
            if b == 'left':
                shiftPiece(-1, 0)
            elif b == 'right':
                shiftPiece(1, 0)
            elif b == 'up':
                harddropPiece()
            elif b == 'cw':
                rotatePiece(1)
            elif b == 'ccw':
                rotatePiece(-1)

def keyReleased(key):
    if key in binds:
        b = binds[key]
        held[b] = False

# game logic

def updateGame():
    if game.over:
        return
    
    # shift/autoshift
    left = held['left']
    right = held['right']
    if left != right:
        dx = (-1 if left else 1)
        if game.dasdir != dx:
            game.dasdir = dx
            game.dastimer = 0
        elif game.dastimer < game.das:
            game.dastimer += 1
    else:
        game.dastimer = 0
        game.dasdir = 0
    if game.dastimer == game.das:
        shiftPiece(game.dasdir, 0)

    # lock delay and spawning
    if not game.active:
        if game.timer > 0:
            game.timer -= 1
        else:
            p = Piece()
            p.name = nextPiece()
            p.x, p.y = spawnpos
            p.r = 0
            game.active = p
            game.timer = game.lock
            game.gravitytimer = 0
            game.pieces += 1

            # irs
            if held['ccw'] != held['cw']:
                dr = (1 if held['cw'] else -1)
                p.r = dr % len(piecedata[p.name])
                if collidePiece():
                    p.r = 0

            if collidePiece():
                game.over = True

    else: # game.active
        if restingPiece():
            if game.timer > 0 and not held['down']:
                game.timer -= 1
            else:
                lockPiece()

    # gravity
    if game.active and not restingPiece():
        g = game.gravity
        if held['down'] and g < 1:
            g = 1
        game.gravitytimer += g
        while game.gravitytimer >= 1 and not restingPiece():
            shiftPiece(0, 1)
            game.gravitytimer -= 1

    clearLines()

def nextPiece():
    p = game.previews.pop(0)
    game.previews.append(game.rand.next())
    return p

def getPieceBlocks(name=None):
    if name == None:
        p = game.active
        name = p.name
        x, y = p.x, p.y
        r = p.r
    else:
        x = 0
        y = 0
        r = 0
    for bx, by in piecedata[name][r]:
        yield (x + bx, y + by)

def collidePiece():
    for x, y in getPieceBlocks():
        if x < 0 or x >= 10 or y >= 20 or (y >= 0 and game.well[x, y]):
            return True
    return False

def restingPiece():
    if not game.active:
        return False
    p = game.active
    p.y += 1
    c = collidePiece()
    p.y -= 1
    return c

def lockPiece():
    for x, y in getPieceBlocks():
        game.well[x, y] = piececolor[game.active.name]
    game.active = None
    game.timer = game.spawn

def clearLines():
    filled = set()
    for y in range(20):
        c = 0
        for x in range(10):
            if game.well[x, y]:
                c += 1
        if c == 10:
            filled.add(y)

    y = y2 = 19
    while y >= 0:
        while y2 in filled:
            y2 -= 1

        if y2 != y:
            for x in range(10):
                if y2 >= 0:
                    game.well[x, y] = game.well[x, y2]
                else:
                    game.well[x, y] = None

        y -= 1
        y2 -= 1

    if len(filled) > 0:
        game.score[len(filled) - 1] += 1

def rotatePiece(dr):
    if game.active:
        p = game.active
        oldr = p.r
        p.r = (p.r + dr) % len(piecedata[p.name])
        if not collidePiece():
            return True
        # try kicking
        if allowKick():
            p.x += 1
            if not collidePiece():
                return True
            p.x -= 2
            if not collidePiece():
                return True
            p.x += 1
        p.r = oldr
    return False

def allowKick():
    p = game.active

    if p.name == 'i':
        return False
    
    if p.name in ('l', 'j', 't'):
        under = []
        for dy in (-2, -1, 0):
            for dx in (-1, 0, 1):
                block = bool(game.well.get((p.x + dx, p.y + dy)))
                under.append(block)
                
        if under[1] or under[4] or under[7]:
            if p.name == 'l' and under[0]:
                return True
            if p.name == 'j' and under[2]:
                return True
            return False
        
    return True

def shiftPiece(dx, dy):
    if not game.active:
        return False
    p = game.active
    p.x += dx
    p.y += dy
    if collidePiece():
        p.x -= dx
        p.y -= dy
        return False
    if dy > 0:
        game.timer = game.lock
    return True

def harddropPiece():
    while shiftPiece(0, 1):
        pass

def softdropPiece():
    shiftPiece(0, 1)
    if restingPiece():
        lockPiece()


# drawing + main loop

def drawScreen():
    surf = pygame.display.get_surface()
    w, h = surf.get_size()
    sz = int(h / 25.)  # block size

    surf.fill((0, 0, 0))

    pygame.draw.rect(surf, (32, 32, 32), (sz, 4*sz, 10*sz, 20*sz))
    for x in range(10):
        for y in range(20):
            color = game.well[x, y]
            if color != None:
                pygame.draw.rect(surf, color, ((1+x)*sz, (4+y)*sz, sz, sz))
    
    if game.active:
        dim = 1 - .7 * float(game.lock - game.timer) / game.lock
        color = piececolor[game.active.name]
        color = tuple(dim * c for c in color)
        for x, y in getPieceBlocks():
            pygame.draw.rect(surf, color, ((1+x)*sz, (4+y)*sz, sz, sz))

    for i, p in enumerate(game.previews):
        color = piececolor[p]
        for x, y in getPieceBlocks(p):
            pygame.draw.rect(surf, color, ((5+i*4+x)*sz, (2+y)*sz, sz, sz))

    for i, n in enumerate(game.score):
        tex = gettext(str(1+i) + 'x = ' + str(n))
        surf.blit(tex, (12*sz, (4+i)*sz))
    tex = gettext('# pieces = ' + str(game.pieces))
    surf.blit(tex, (12*sz, 8*sz))

def gettext(s):
    return font.render(s, True, (255, 255, 255))

def main():
    global game, font
    
    pygame.init()
    pygame.display.set_mode(resolution)

    font = pygame.font.Font(pygame.font.get_default_font(), 16)

    game = Game()
    game.over = True

    frame = 1/60.
    while True:
        start = time.time()
        handleEvents()
        updateGame()
        drawScreen()
        pygame.display.update()
        used = time.time() - start
        if used < frame:
            time.sleep(frame - used)

main()
