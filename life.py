#!/usr/bin/env python3
"""
Conway's Game of Life - Terminal Edition
=========================================

A colorful terminal simulation of Conway's Game of Life cellular automaton
with ANSI color animation and built-in patterns.

Usage:
    python life.py                         # Default: random 50x25 grid
    python life.py --width 80 --height 40  # Custom size
    python life.py --density 0.2           # Sparse initial state
    python life.py --pattern glider_gun    # Pre-defined pattern
    python life.py --generations 300       # Run for 300 generations
    python life.py --fps 15                # Faster animation

Rules:
    - Any live cell with 2 or 3 neighbors survives.
    - Any dead cell with exactly 3 neighbors becomes alive.
    - All other cells die or stay dead.

Patterns: glider, blinker, block, pulsar, lwss, glider_gun,
          rpentomino, diehard, acorn

Author: AI_BOT_2026 for CTest
Date: 2026-05-15
"""

import argparse
import random
import sys
import time

# ── ANSI Escape Codes ──────────────────────────────────────────────────────
LIVE_CHARS = ['\u2588', '\u2593', '\u2592']
RESET      = '\033[0m'
BOLD       = '\033[1m'
DIM        = '\033[2m'
HIDE_CUR   = '\033[?25l'
SHOW_CUR   = '\033[?25h'
CLEAR      = '\033[2J'
HOME       = '\033[H'

# ── Color Palette ──────────────────────────────────────────────────────────
RAINBOW = [196, 202, 208, 214, 220, 226, 190, 154, 118, 82,
           46, 47, 48, 49, 50, 51, 45, 39, 33, 27,
           21, 57, 93, 129, 165, 201, 200, 199, 198]


def color_256(n):
    return f'\033[38;5;{n}m'


def cell_color(x, y, age, gen):
    if age == 0:
        return DIM
    idx = (x * 7 + y * 13 + gen * 3 + age * 5) % len(RAINBOW)
    return color_256(RAINBOW[idx])


# ── Grid Operations ────────────────────────────────────────────────────────

def create_random_grid(w, h, density=0.3):
    return [[1 if random.random() < density else 0 for _ in range(w)] for _ in range(h)]


def count_neighbors(grid, x, y, w, h):
    total = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            total += grid[(y + dy) % h][(x + dx) % w]
    return total


def next_generation(grid, w, h):
    new = [[0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            n = count_neighbors(grid, x, y, w, h)
            if grid[y][x]:
                new[y][x] = 1 if n in (2, 3) else 0
            else:
                new[y][x] = 1 if n == 3 else 0
    return new


def update_ages(ages, grid, w, h):
    new_ages = [[0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if grid[y][x]:
                new_ages[y][x] = min(ages[y][x] + 1, 999)
    return new_ages


def population(grid, w, h):
    return sum(sum(row) for row in grid)


# ── Rendering ──────────────────────────────────────────────────────────────

def render_frame(grid, ages, w, h, gen, pop, max_pop):
    buf = [HOME]
    bar = f'{BOLD}\u2554\u2550\u2557{RESET} {BOLD}Conway\'s Game of Life{RESET} '
    bar += f'{DIM}\u2502{RESET} Gen: {BOLD}{gen:04d}{RESET} '
    bar += f'{DIM}\u2502{RESET} Pop: {BOLD}{pop:05d}{RESET} '
    bar += f'{DIM}\u2502{RESET} Grid: {w}x{h}'
    buf.append(bar)
    buf.append(f'{DIM}\u2554{"\u2550" * (w * 2)}\u2557{RESET}')
    for y in range(h):
        row = '\u2551'
        for x in range(w):
            if grid[y][x]:
                age = ages[y][x]
                c = cell_color(x, y, age, gen)
                ch = LIVE_CHARS[min(age // 3, 2)]
                row += f'{c}{ch}{ch}{RESET}'
            else:
                row += f'{DIM}  {RESET}'
        row += '\u2551'
        buf.append(row)
    buf.append(f'{DIM}\u255a{"\u2550" * (w * 2)}\u255d{RESET}')
    pct = (pop / max_pop * 100) if max_pop > 0 else 0
    filled = int(pct / 100 * 30)
    bv = '\u2588' * filled + '\u2591' * (30 - filled)
    c = color_256(46) if pct < 30 else color_256(226) if pct < 70 else color_256(196)
    buf.append(f' {DIM}\u2514{RESET} Density: [{c}{bv}{RESET}] {pct:.1f}%')
    sys.stdout.write('\n'.join(buf))
    sys.stdout.flush()


# ── Pre-defined Patterns ───────────────────────────────────────────────────

def make_pulsar():
    return [
        (2,0),(3,0),(4,0),(8,0),(9,0),(10,0),
        (0,2),(5,2),(7,2),(12,2),
        (0,3),(5,3),(7,3),(12,3),
        (0,4),(5,4),(7,4),(12,4),
        (2,5),(3,5),(4,5),(8,5),(9,5),(10,5),
        (2,7),(3,7),(4,7),(8,7),(9,7),(10,7),
        (0,8),(5,8),(7,8),(12,8),
        (0,9),(5,9),(7,9),(12,9),
        (0,10),(5,10),(7,10),(12,10),
        (2,12),(3,12),(4,12),(8,12),(9,12),(10,12),
    ]

def make_rpentomino():
    return [(1,0),(2,0),(0,1),(1,1),(1,2)]

def make_diehard():
    return [(6,0),(0,1),(1,1),(1,2),(5,2),(6,2),(7,2)]

def make_acorn():
    return [(1,0),(3,1),(0,2),(1,2),(4,2),(5,2),(6,2)]


PATTERNS = {
    'glider':       [(1,0),(2,1),(0,2),(1,2),(2,2)],
    'blinker':      [(0,0),(1,0),(2,0)],
    'block':        [(0,0),(0,1),(1,0),(1,1)],
    'lwss':         [(0,1),(0,4),(1,0),(2,0),(2,4),(3,0),(3,1),(3,2),(3,3)],
    'glider_gun':   [
        (0,4),(0,5),(1,4),(1,5),
        (10,3),(10,4),(10,5),(11,2),(11,6),
        (12,1),(12,7),(13,1),(13,7),(14,4),(15,2),(15,6),
        (16,3),(16,4),(16,5),(17,4),
        (20,1),(20,2),(20,3),(21,1),(21,2),(21,3),
        (22,0),(22,4),(24,0),(24,4),
        (25,0),(25,1),(25,5),(26,2),(26,3),(26,4),(26,5),
        (34,2),(34,3),(35,2),(35,3),
    ],
}

PATTERN_FACTORIES = {
    'pulsar':     make_pulsar,
    'rpentomino': make_rpentomino,
    'diehard':    make_diehard,
    'acorn':      make_acorn,
}

# Merge static + factory patterns for choices
ALL_PATTERNS = {**PATTERNS, **{k: None for k in PATTERN_FACTORIES}}


def place_pattern(grid, pattern, w, h):
    if not pattern:
        return
    min_x = min(p[0] for p in pattern)
    max_x = max(p[0] for p in pattern)
    min_y = min(p[1] for p in pattern)
    max_y = max(p[1] for p in pattern)
    off_x = (w - (max_x - min_x + 1)) // 2 - min_x
    off_y = (h - (max_y - min_y + 1)) // 2 - min_y
    for x, y in pattern:
        gx, gy = x + off_x, y + off_y
        if 0 <= gx < w and 0 <= gy < h:
            grid[gy][gx] = 1


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Conway's Game of Life - Terminal Edition",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Patterns: ' + ', '.join(sorted(ALL_PATTERNS.keys()))
    )
    parser.add_argument('-W', '--width', type=int, default=50)
    parser.add_argument('-H', '--height', type=int, default=25)
    parser.add_argument('-d', '--density', type=float, default=0.3)
    parser.add_argument('-g', '--generations', type=int, default=200,
                        help='0 = infinite')
    parser.add_argument('--fps', type=float, default=10)
    parser.add_argument('-p', '--pattern', choices=sorted(ALL_PATTERNS.keys()))
    parser.add_argument('--seed', type=int, default=None)
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    w, h = args.width, args.height
    grid = create_random_grid(w, h, args.density)

    if args.pattern:
        grid = create_random_grid(w, h, 0)
        if args.pattern in PATTERN_FACTORIES:
            pat = PATTERN_FACTORIES[args.pattern]()
        else:
            pat = PATTERNS[args.pattern]
        place_pattern(grid, pat, w, h)

    ages = [[1 if grid[y][x] else 0 for x in range(w)] for y in range(h)]
    max_pop = w * h

    sys.stdout.write('\033[?1049h' + HIDE_CUR + CLEAR)
    gen = 0
    peak_pop = population(grid, w, h)

    try:
        while True:
            pop = population(grid, w, h)
            peak_pop = max(peak_pop, pop)
            render_frame(grid, ages, w, h, gen, pop, max_pop)
            if pop == 0:
                time.sleep(1)
                sys.stdout.write(HOME + CLEAR)
                sys.stdout.write(f'\n  {BOLD}All cells died at generation {gen}.{RESET}\n')
                sys.stdout.write(f'  Peak population was {peak_pop}. RIP.\n\n')
                sys.stdout.flush()
                time.sleep(2)
                break
            if 0 < args.generations <= gen:
                time.sleep(1)
                sys.stdout.write(HOME + CLEAR)
                sys.stdout.write(f'\n  {BOLD}Simulation complete: {gen} generations.{RESET}\n')
                sys.stdout.write(f'  Final: {pop} | Peak: {peak_pop}\n\n')
                sys.stdout.flush()
                time.sleep(2)
                break
            grid = next_generation(grid, w, h)
            ages = update_ages(ages, grid, w, h)
            gen += 1
            time.sleep(1.0 / args.fps)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write(SHOW_CUR + '\033[?1049l' + RESET)
        sys.stdout.flush()


if __name__ == '__main__':
    main()
