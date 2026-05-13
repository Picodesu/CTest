#!/usr/bin/env python3
"""
wave_art.py - 波形艺术生成器

用数学之美点亮你的终端。

用法:
    python wave_art.py                 # 今日限定图案（基于日期）
    python wave_art.py "你的名字"      # 基于任意文字生成
    python wave_art.py --seed 42       # 指定种子探索

每一次输入，都是独一无二的波形。
"""

import math
import sys
import hashlib
from datetime import date


def seed_from_input(user_input):
    """从输入生成种子"""
    if user_input is None:
        return int(date.today().strftime('%Y%m%d'))
    try:
        return int(user_input)
    except ValueError:
        h = hashlib.md5(user_input.encode('utf-8')).hexdigest()
        return int(h[:8], 16)


def lcg(r):
    """线性同余伪随机数生成器"""
    return (r * 1103515245 + 12345) & 0x7FFFFFFF


def generate_art(seed, width=76, height=36):
    """生成波形艺术"""
    canvas = [[' '] * width for _ in range(height)]
    cy = height // 2

    # 从种子解析波形参数
    r = seed
    palette = '·∘○◎◉●★☆✦✧◆◇□▪▫'

    waves = []
    n_waves = 3 + r % 4
    for i in range(n_waves):
        r = lcg(r)
        amp = 2 + r % 10
        r = lcg(r)
        freq = 0.03 + (r % 80) / 2000.0
        r = lcg(r)
        phase = (r % 628) / 100.0
        r = lcg(r)
        ch = palette[r % len(palette)]
        waves.append((amp, freq, phase, ch))

    # 绘制波形
    for amp, freq, phase, ch in waves:
        for x in range(width):
            y = cy
            y += int(amp * math.sin(freq * x * 2 + phase))
            y += int(amp * 0.4 * math.sin(freq * x * 3.7 + phase * 1.3))
            y += int(amp * 0.25 * math.cos(freq * x * 1.5 + phase * 0.7))

            if 0 <= y < height:
                canvas[y][x] = ch
            # 光晕效果
            for dy in (-1, 1):
                ny = y + dy
                if 0 <= ny < height and canvas[ny][x] == ' ':
                    canvas[ny][x] = '·'

    # 散布星辰点缀
    for _ in range(20):
        r = lcg(r)
        sx = r % width
        r = lcg(r)
        sy = r % height
        if canvas[sy][sx] == ' ':
            canvas[sy][sx] = '✦'

    return '\n'.join(''.join(row) for row in canvas)


def main():
    seed_input = None
    if '--seed' in sys.argv:
        idx = sys.argv.index('--seed')
        if idx + 1 < len(sys.argv):
            seed_input = sys.argv[idx + 1]
    elif len(sys.argv) > 1:
        seed_input = sys.argv[1]

    seed = seed_from_input(seed_input)
    today = date.today()

    print(f"""
  ╔═══════════════════════════════════════════╗
  ║         波形艺术  W a v e   A r t         ║
  ║         {today.strftime('%Y-%m-%d')}  ·  种子 #{seed:<10}     ║
  ╚═══════════════════════════════════════════╝
""")
    print(generate_art(seed))
    print(f"""
  n = {3 + seed % 4} layers  |  "数学是宇宙无声的诗"

  用法: python wave_art.py "任意文字" | --seed N
""")


if __name__ == '__main__':
    main()
