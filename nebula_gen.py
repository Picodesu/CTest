#!/usr/bin/env python3
"""
nebula_gen.py - Procedural ASCII Nebula Generator / 程序化 ASCII 星云生成器

用纯 ASCII 字符和 ANSI 256 色生成独一无二的星云场景。
基于分形布朗运动 (FBM) 噪声和螺旋臂算法。

每次运行产生不同的宇宙画面。

用法: python3 nebula_gen.py
"""

import random
import math
from datetime import datetime

RST = '\033[0m'


# ---- Noise primitives ----

def _hash(x, y, seed):
    """Deterministic hash -> float in [0, 1)."""
    h = (x * 374761393 + y * 668265263 + seed * 1274126177) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1103515245 + 12345) & 0xFFFFFFFF
    return h / 0xFFFFFFFF


def _smoothstep(t):
    return t * t * (3.0 - 2.0 * t)


def value_noise(x, y, seed):
    """Smooth value noise via bilinear interpolation."""
    ix, iy = int(math.floor(x)), int(math.floor(y))
    fx, fy = _smoothstep(x - ix), _smoothstep(y - iy)

    v00 = _hash(ix, iy, seed)
    v10 = _hash(ix + 1, iy, seed)
    v01 = _hash(ix, iy + 1, seed)
    v11 = _hash(ix + 1, iy + 1, seed)

    return (v00 * (1 - fx) + v10 * fx) * (1 - fy) + (v01 * (1 - fx) + v11 * fx) * fy


def fbm(x, y, seed, octaves=5):
    """Fractal Brownian Motion - layered noise at increasing frequencies."""
    val = 0.0
    amp = 1.0
    freq = 1.0
    max_amp = 0.0
    for i in range(octaves):
        val += amp * value_noise(x * freq, y * freq, seed + i * 137)
        max_amp += amp
        amp *= 0.5
        freq *= 2.0
    return val / max_amp


# ---- Nebula generation ----

def generate():
    now = datetime.now()
    seed = int(now.timestamp()) // 60  # rotates every minute
    rng = random.Random(seed)

    W, H = 60, 20
    CX, CY = W / 2.0, H / 2.0

    # --- Color palettes (ANSI 256) ---
    palettes = [
        {
            'name': 'Violet',
            'layers': [
                (0.20, [93, 129, 135]),
                (0.40, [99, 135, 141, 171]),
                (0.60, [141, 171, 213]),
                (0.80, [177, 213, 219]),
            ],
        },
        {
            'name': 'Cyan',
            'layers': [
                (0.20, [23, 29, 30]),
                (0.40, [30, 37, 43, 49]),
                (0.60, [49, 75, 80, 114]),
                (0.80, [117, 159, 214]),
            ],
        },
        {
            'name': 'Rose',
            'layers': [
                (0.20, [89, 95, 129]),
                (0.40, [132, 138, 168]),
                (0.60, [168, 174, 213]),
                (0.80, [210, 216, 222]),
            ],
        },
    ]

    pal = rng.choice(palettes)

    # --- Spiral arm parameters ---
    n_arms = rng.randint(2, 4)
    arm_spread = rng.uniform(0.4, 0.9)
    arm_rot = rng.uniform(0, 2 * math.pi)

    # Center offset for organic asymmetry
    ox = rng.uniform(-4, 4)
    oy = rng.uniform(-2, 2)

    # --- Build density field ---
    grid = []
    for y in range(H):
        row = []
        ny = (y - CY + oy) / (H * 0.38)
        for x in range(W):
            nx = (x - CX + ox) / (W * 0.38)
            dist = math.sqrt(nx * nx + ny * ny)
            angle = math.atan2(ny, nx)

            # Base density from fractal noise
            n = fbm(x * 0.07, y * 0.10, seed, 5)

            # Spiral arm contribution
            spiral = 0.0
            for arm in range(n_arms):
                a = arm_rot + arm * (2 * math.pi / n_arms)
                diff = math.fmod(angle - a + 4 * math.pi, 2 * math.pi) - math.pi
                spiral += math.exp(-abs(diff) * arm_spread) * math.exp(-dist * 1.2)

            # Combine noise + spiral, apply radial falloff
            density = (n * 0.45 + spiral * 0.55) * max(0.0, 1.0 - dist * 0.75)
            density = max(0.0, min(1.0, density))

            star = rng.random()
            row.append((density, star))
        grid.append(row)

    # --- Render to ANSI ---
    DENSITY_CHARS = ' .,\u00b7:;+*%@#'

    out = []
    out.append('')
    out.append(f'  \033[38;5;255m\033[1m* * *  N E B U L A  #{seed % 10000:04d}  * * *{RST}')
    out.append(f'  \033[2m  {pal["name"]} Nebula  |  {now.strftime("%Y-%m-%d %H:%M")}{RST}')
    out.append('')

    for y in range(H):
        line = '  '
        for x in range(W):
            density, star = grid[y][x]

            if density < 0.06:
                # Void: sparse background stars
                if star < 0.012:
                    bc = rng.choice([250, 253, 255])
                    ch = rng.choice(['.', '*', '+'])
                    line += f'\033[38;5;{bc}m{ch}{RST}'
                else:
                    line += ' '
            else:
                # Nebula pixel
                ci = min(
                    int(density * (len(DENSITY_CHARS) - 1)),
                    len(DENSITY_CHARS) - 1,
                )
                ch = DENSITY_CHARS[ci]

                # Pick color from highest matching palette layer
                color = 255
                for thresh, colors in reversed(pal['layers']):
                    if density >= thresh:
                        idx = (x * 3 + y * 7) % len(colors)
                        color = colors[idx]
                        break

                line += f'\033[38;5;{color}m{ch}{RST}'

        out.append(line)

    out.append('')
    info = (
        f'  Seed: {seed}  |  ID: #{seed % 10000:04d}'
        f'  |  Palette: {pal["name"]}  |  Arms: {n_arms}'
    )
    out.append(f'\033[2m{info}{RST}')
    out.append('')

    return '\n'.join(out)


if __name__ == '__main__':
    print(generate())
