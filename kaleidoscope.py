#!/usr/bin/env python3
"""
Terminal Kaleidoscope - daily symmetric pattern generator
Usage: python kaleidoscope.py [size]
"""

import random
import sys
import hashlib
from datetime import datetime

PALETTES = {
    'cosmic': list('·∙●○◎◉★☆✦✧†‡∞≈∴∵♦♠♣'),
    'nature': list('❀❁❃❋✿❀✾✽✼❃✿❀❁'),
    'binary': list('01⬡⬢◇◆▲▼□■'),
    'zen': list('禅意空静心悟道法自然和'),
    'music': list('♩♪♫♬♭♮♯'),
    'math': list('∫∑∏√∞∂∇≈≠≤≥∈∉⊂⊃∪∩'),
}

def get_daily_seed():
    today = datetime.now().strftime('%Y-%m-%d')
    return int(hashlib.md5(today.encode()).hexdigest()[:8], 16)

def generate_pattern(size=16, seed=None):
    if seed is None:
        seed = get_daily_seed()
    rng = random.Random(seed)
    palette_name = rng.choice(list(PALETTES.keys()))
    palette = PALETTES[palette_name]
    quadrant = []
    for y in range(size):
        row = []
        for x in range(size):
            dist = (x**2 + y**2) ** 0.5
            noise = rng.random() * 3
            idx = int((dist + noise) * len(palette) / (size * 1.4)) % len(palette)
            row.append(palette[idx])
        quadrant.append(row)
    full = []
    for row in reversed(quadrant):
        mirrored = row[::-1]
        full.append(mirrored + row)
    for row in quadrant:
        mirrored = row[::-1]
        full.append(mirrored + row)
    return full, palette_name

def render(pattern, palette_name):
    today = datetime.now().strftime('%Y-%m-%d %A')
    lines = [f'  Terminal Kaleidoscope  {today}', f'  palette: {palette_name}', '']
    for row in pattern:
        lines.append('  ' + ''.join(row))
    lines.extend(['', f'  seed: {get_daily_seed()}', '  Different pattern every day. See you tomorrow!'])
    return '\n'.join(lines)

def to_html(pattern, palette_name):
    today = datetime.now().strftime('%Y-%m-%d %A')
    colors = {'cosmic':'#a78bfa','nature':'#34d399','binary':'#60a5fa','zen':'#fbbf24','music':'#f472b6','math':'#6ee7b7'}
    color = colors.get(palette_name, '#ffffff')
    parts = ['<!DOCTYPE html>','<html><head><meta charset="utf-8">',f'<title>Kaleidoscope {today}</title>','<style>',
        'body{background:#0a0a0a;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;margin:0;font-family:monospace}',
        f'h1{{color:{color};font-size:1.2em}}',f'.palette{{color:#888;font-size:0.9em}}',
        f'pre{{color:{color};font-size:14px;line-height:1.1;text-shadow:0 0 8px {color}44}}',
        '.seed{color:#555;font-size:0.8em;margin-top:20px}','</style></head><body>',
        f'<h1>Terminal Kaleidoscope - {today}</h1>',f"<div class='palette'>palette: {palette_name}</div>",'<pre>']
    for row in pattern:
        parts.append(''.join(row))
    parts.extend(['</pre>',f"<div class='seed'>seed: {get_daily_seed()} - different every day.</div>",'</body></html>'])
    return '\n'.join(parts)

if __name__ == '__main__':
    size = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    size = max(4, min(32, size))
    pattern, palette_name = generate_pattern(size)
    print(render(pattern, palette_name))
    html = to_html(pattern, palette_name)
    html_path = f'/tmp/kaleidoscope_{datetime.now().strftime("%Y%m%d")}.html'
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'\n  HTML saved: {html_path}')
