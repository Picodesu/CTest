#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════╗
║        Digital Terrarium  —  生态微景观          ║
║   A living ASCII ecosystem in your terminal.     ║
╚══════════════════════════════════════════════════╝

Plants grow, rain falls, clouds drift, day turns
into night, and tiny creatures wander the ground.

Run:  python3 digital_terrarium.py
Stop: Ctrl+C

English / 中文 / 日本語 / 한국어
"""

import random, time, os, sys

# ═══════════════ ANSI escape helpers ═══════════════
R  = '\033[0m'      # reset
D  = '\033[2m'      # dim
B  = '\033[1m'      # bold
# foreground
r  = '\033[31m'     g_ = '\033[32m'     y  = '\033[33m'
b  = '\033[34m'     m  = '\033[35m'     c  = '\033[36m'
w  = '\033[37m'
G  = '\033[92m'     Y  = '\033[93m'     B2 = '\033[94m'
C2 = '\033[96m'     M  = '\033[95m'     W2 = '\033[97m'

# canvas size (characters)
COLS = 60
ROWS = 22
GROUND = ROWS - 3          # ground line
CYCLE_LEN = 450            # ticks per full day/night cycle

# ──────────────── Pre-generated textures ────────────────
SOIL = [['.'] * COLS for _ in range(3)]
for row in SOIL:
    for x in range(COLS):
        row[x] = random.choice(['.', ',', ':', ';', '%', "'"])

def _pick(items):
    return random.choice(items)


# ═══════════════════════════════════════════════════════
#  World
# ═══════════════════════════════════════════════════════
class World:
    def __init__(self):
        self.tick = 0
        self.plants = []
        self.rain   = []
        self.bugs   = []
        self.clouds = [{'x': random.uniform(0, COLS),
                        'y': random.randint(1, 5),
                        'w': random.randint(5, 10)}
                       for _ in range(4)]
        self.stars  = [(random.randint(0, COLS-1),
                        random.randint(0, GROUND-7))
                       for _ in range(25)]
        # seed a few plants to start
        for _ in range(5):
            self._sprout()

    # ── helpers ──
    def _sprout(self, x=None):
        self.plants.append({
            'x': x or random.randint(2, COLS-3),
            'h': 0,
            'max_h': random.randint(3, 7),
            'kind': _pick(['flower', 'fern', 'tree']),
            'stem_c': _pick([g_, G, y, m]),
            'bloom_c': _pick([r, R, m, M, y, Y]),
            'bloomed': False,
        })

    def _rain(self, n=None):
        for _ in range(n or random.randint(3, 10)):
            self.rain.append({
                'x': random.randint(0, COLS-1),
                'y': 0,
                'sp': random.uniform(0.4, 0.9),
            })

    # ── tick ──
    def update(self):
        self.tick += 1
        phase = (self.tick % CYCLE_LEN) / CYCLE_LEN   # 0‥1
        self.phase = phase

        # grow plants
        for p in self.plants:
            if p['h'] < p['max_h'] and self.tick % 12 == 0:
                p['h'] += 1
            if p['h'] >= p['max_h']:
                p['bloomed'] = True

        # advance rain
        self.rain = [r for r in self.rain if r['y'] + r['sp'] < GROUND]
        for r in self.rain:
            r['y'] += r['sp']

        # drift clouds
        for cl in self.clouds:
            cl['x'] = (cl['x'] + 0.04 + random.uniform(0, 0.02)) % (COLS + cl['w'])

        # move bugs
        for b in self.bugs:
            if self.tick % 3 == 0:
                b['x'] += b['dx']
                if b['x'] <= 0 or b['x'] >= COLS - 1:
                    b['dx'] = -b['dx']
            b['frame'] += 1
            # sleep at night
            if 0.6 < phase < 0.95:
                b['dx'] = 0

        # random events
        if random.random() < 0.015:
            self._rain()
        if random.random() < 0.003 and len(self.plants) < 15:
            self._sprout()
        if random.random() < 0.004 and len(self.bugs) < 5:
            self.bugs.append({
                'x': random.randint(1, COLS-2),
                'y': GROUND - 1,
                'dx': _pick([-1, 1]),
                'frame': 0,
            })

    # ── render ──
    def render(self):
        phase = self.phase
        fr = [[' '] * COLS for _ in range(ROWS)]
        fc = [['']  * COLS for _ in range(ROWS)]

        # ── sky ──
        if phase < 0.12:       # dawn
            sky_bg = lambda x, y: (D, '.')
        elif phase < 0.42:     # day
            sky_bg = lambda x, y: (b, ' ')
        elif phase < 0.55:     # dusk
            sky_bg = lambda x, y: (D + r, '.')
        else:                   # night
            sky_bg = lambda x, y: (D, ' ')

        for sy in range(GROUND):
            for sx in range(COLS):
                fr[sy][sx] = sky_bg(sx, sy)[1]
                fc[sy][sx] = sky_bg(sx, sy)[0]

        # stars
        if phase > 0.55:
            for sx, sy in self.stars:
                if random.random() < 0.35:
                    fr[sy][sx] = _pick(['.', '*', '`', '+'])
                    fc[sy][sx] = Y + D

        # sun arc (parabolic)
        if 0.05 < phase < 0.50:
            sp = (phase - 0.05) / 0.45          # 0‥1
            sun_x = int(3 + sp * (COLS - 6))
            para = 1.0 - (2.0 * sp - 1.0) ** 2   # 0→1→0
            sun_y = max(1, int(GROUND - 2 - para * (GROUND - 6)))
            art = ['  \\|/  ', '  --O-- ', '  /|\\  ']
            for dy, row in enumerate(art):
                for dx, ch in enumerate(row):
                    nx, ny = sun_x - 3 + dx, sun_y - 1 + dy
                    if 0 <= nx < COLS and 0 <= ny < ROWS:
                        fr[ny][nx] = ch
                        fc[ny][nx] = Y

        # moon
        if phase > 0.6:
            mx, my = int(COLS * 0.78), 3
            for dy, row in enumerate([' _ ', '(_)', '   ']):
                for dx, ch in enumerate(row):
                    nx, ny = mx - 1 + dx, my - 1 + dy
                    if 0 <= nx < COLS and 0 <= ny < ROWS:
                        fr[ny][nx] = ch
                        fc[ny][nx] = W2

        # clouds
        for cl in self.clouds:
            cx, cy, cw = int(cl['x']), int(cl['y']), int(cl['w'])
            top = ' ' + '_' * cw + ' '
            mid = '/' + 'o' * cw + '\\'
            for dy, row in enumerate([top, mid]):
                for dx, ch in enumerate(row):
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < COLS and 0 <= ny < GROUND:
                        fr[ny][nx] = ch
                        fc[ny][nx] = D + w

        # rain
        for ri in self.rain:
            rx, ry = int(ri['x']), int(ri['y'])
            if 0 <= rx < COLS and 0 <= ry < ROWS:
                fr[ry][rx] = _pick(['|', '/', '\\'])
                fc[ry][rx] = C2

        # ── ground ──
        for x in range(COLS):
            fr[GROUND][x] = _pick(['_', '=', '~', '`'])
            fc[GROUND][x] = g_
        for dy in range(1, 3):
            gy = GROUND + dy
            if gy < ROWS:
                for x in range(COLS):
                    fr[gy][x] = SOIL[dy - 1][x]
                    fc[gy][x] = r if dy > 1 else g_

        # ── plants ──
        for p in self.plants:
            px, ph = int(p['x']), p['h']
            base = GROUND - 1
            for i in range(ph):
                sy = base - i
                if not (0 <= sy < ROWS and 0 <= px < COLS):
                    continue
                if i == 0:
                    fr[sy][px] = '|'
                    fc[sy][px] = g_
                elif i < ph - 1:
                    fr[sy][px] = '|' if p['kind'] != 'fern' else '/'
                    fc[sy][px] = p['stem_c']
                elif p['bloomed']:
                    if p['kind'] == 'flower':
                        fr[sy][px] = '@'
                        fc[sy][px] = p['bloom_c']
                        for dx in (-1, 1):
                            nx = px + dx
                            if 0 <= nx < COLS:
                                fr[sy][nx] = '*'
                                fc[sy][nx] = p['bloom_c']
                    elif p['kind'] == 'tree':
                        for dy2 in range(-2, 1):
                            for dx2 in range(-2, 3):
                                nx2, ny2 = px + dx2, sy + dy2
                                if 0 <= nx2 < COLS and 0 <= ny2 < ROWS:
                                    if abs(dx2) + abs(dy2) <= 3:
                                        fr[ny2][nx2] = '@'
                                        fc[ny2][nx2] = G
                        fr[sy][px] = '|'
                        fc[sy][px] = g_
                    else:   # fern
                        fr[sy][px] = '"'
                        fc[sy][px] = G
                        for dx in (-1, 1):
                            nx = px + dx
                            if 0 <= nx < COLS:
                                fr[sy][nx] = '"'
                                fc[sy][nx] = p['stem_c']
                else:
                    fr[sy][px] = '"'
                    fc[sy][px] = p['stem_c']

        # ── bugs ──
        for b in self.bugs:
            bx, by = int(b['x']), int(b['y'])
            if 0 <= bx < COLS and 0 <= by < ROWS:
                ch = ['o', '@', '0', 'o', '.', '@'][b['frame'] % 6]
                fr[by][bx] = ch
                fc[by][bx] = r

        # ── compose terminal output ──
        lines = []
        # header
        if phase < 0.12:       pl, pc = 'Dawn',  Y
        elif phase < 0.42:    pl, pc = 'Day',   B2
        elif phase < 0.55:    pl, pc = 'Dusk',  r
        else:                  pl, pc = 'Night', D
        hdr = f' {B}{c}~ Digital Terrarium ~{R}' \
              f'  {D}{pc}{pl}{R}' \
              f'  {D}Plants:{len(self.plants)}' \
              f'  Rain:{len(self.rain)}' \
              f'  Bugs:{len(self.bugs)}{R}'
        lines.append(hdr)
        lines.append(f' {D}{"─" * (COLS - 2)}{R}')

        for y in range(ROWS):
            buf = ''
            for x in range(COLS):
                ch, cl = fr[y][x], fc[y][x]
                buf += f'{cl}{ch}{R}' if cl else ch
            lines.append(f' {buf}')

        lines.append(f' {D}{"─" * (COLS - 2)}{R}')
        lines.append(f' {D}Ctrl+C to quit | Plants self-seed | Rain comes and goes{R}')

        sys.stdout.write('\033[H' + '\n'.join(lines))
        sys.stdout.flush()


# ═══════════════════════════════════════════════════════
#  Entry point
# ═══════════════════════════════════════════════════════
def main():
    # hide cursor, clear screen
    sys.stdout.write('\033[?25l\033[2J\033[H')
    world = World()
    try:
        while True:
            world.update()
            world.render()
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write('\033[?25h\033[0m\033[2J\033[H')
        print('Thanks for visiting the terrarium!')
        print('感谢光临生态微景观!')
        print('テラリウムへようこそ!')
        print('테라리움을 방문해 주셔서 감사합니다!')
        print()


if __name__ == '__main__':
    main()
