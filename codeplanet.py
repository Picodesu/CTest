#!/usr/bin/env python3
"""
CodePlanet - 程序员专属太阳系模拟器
在终端中观赏一场 ASCII 太阳系动画
Picodesu/CTest 出品
"""

import math
import time
import os
import sys
import random

# ANSI 色码
RESET = "\033[0m"
BOLD  = "\033[1m"
DIM   = "\033[2m"

YELLOW  = "\033[33m"
RED     = "\033[31m"
GREEN   = "\033[32m"
BLUE    = "\033[34m"
MAGENTA = "\033[35m"
CYAN    = "\033[36m"
WHITE   = "\033[37m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_RED    = "\033[91m"
BRIGHT_GREEN  = "\033[92m"
BRIGHT_CYAN   = "\033[96m"
ORANGE  = "\033[38;5;208m"
PURPLE  = "\033[38;5;129m"
PINK    = "\033[38;5;205m"
DGRAY   = "\033[90m"


class CodePlanet:
    """ASCII 太阳系终端模拟器"""

    # 行星定义: (名称, 符号, 色码, 轨道半径, 角速度, 描述)
    PLANETS = [
        ("Mercury",  "*",  ORANGE,   6,  0.045,  "水星 - 离太阳最近的流浪者"),
        ("Venus",    "o",  YELLOW,  11,  0.020,  "金星 - 被云层包裹的神秘邻居"),
        ("Earth",    "@",  CYAN,    16,  0.012,  "地球 - 我们的蓝色家园"),
        ("Mars",     "+",  RED,     21,  0.008,  "火星 - 等待人类的红色荒原"),
        ("Jupiter",  "O",  MAGENTA, 29,  0.004,  "木星 - 气态巨人的王者"),
        ("Saturn",   "0",  YELLOW,  37,  0.003,  "土星 - 带着光环的优雅舞者"),
    ]

    def __init__(self, width=76, height=22):
        self.width = width
        self.height = height
        self.angle = 0.0
        self.tick = 0
        self.stars = self._gen_stars(120)
        self.shooting_stars = []

    def _gen_stars(self, n):
        return [(random.randint(0, self.width - 1),
                 random.randint(0, self.height - 1),
                 random.choice([1, 2, 3])) for _ in range(n)]

    def _maybe_shooting_star(self):
        """偶尔生成流星"""
        if random.random() < 0.06:
            sx = random.randint(10, self.width - 20)
            sy = random.randint(0, self.height // 3)
            length = random.randint(4, 8)
            self.shooting_stars.append((sx, sy, length, 3))
        # 更新流星
        new = []
        for sx, sy, l, life in self.shooting_stars:
            if life > 0:
                new.append((sx + 2, sy + 1, l, life - 1))
        self.shooting_stars = new

    def _put(self, canvas, colors, x, y, ch, color):
        if 0 <= y < self.height and 0 <= x < self.width and ch != ' ':
            canvas[y][x] = ch
            colors[y][x] = color

    def render(self):
        canvas = [[' '] * self.width for _ in range(self.height)]
        colors = [[None] * self.width for _ in range(self.height)]

        # 星空（闪烁）
        for sx, sy, brightness in self.stars:
            if (sx + self.tick) % (5 + brightness) == 0:
                ch = '.' if brightness == 1 else '·' if brightness == 2 else '*'
                self._put(canvas, colors, sx, sy, ch, DGRAY if brightness == 1 else WHITE)

        # 流星
        self._maybe_shooting_star()
        for sx, sy, length, life in self.shooting_stars:
            for i in range(length):
                tx, ty = sx - i, sy - i
                if 0 <= ty < self.height and 0 <= tx < self.width:
                    ch = '\\' if i < length - 1 else '*'
                    c = BRIGHT_CYAN if i < 2 else WHITE if i < length - 2 else DGRAY
                    self._put(canvas, colors, tx, ty, ch, c)

        # 太阳
        cx, cy = self.width // 2, self.height // 2
        sun_frames = [
            ["   \\|/   ", "  -- * -- ", "   /|\\   "],
            ["   \\|/   ", "  -- o -- ", "   /|\\   "],
            ["   \\|/   ", "  -- * -- ", "   /|\\   "],
            ["   .|.   ", "  -- * -- ", "   `|'   "],
        ]
        frame = sun_frames[self.tick % len(sun_frames)]
        for i, line in enumerate(frame):
            for j, ch in enumerate(line):
                if ch != ' ':
                    self._put(canvas, colors, cx - 5 + j, cy - 1 + i, ch, BRIGHT_YELLOW)

        # 轨道线
        for name, sym, color, orbit_r, speed, desc in self.PLANETS:
            for a in range(0, 360, 2):
                rad = math.radians(a)
                ox = int(cx + orbit_r * math.cos(rad))
                oy = int(cy + orbit_r * math.sin(rad) * 0.38)
                if 0 <= oy < self.height and 0 <= ox < self.width:
                    if canvas[oy][ox] == ' ':
                        canvas[oy][ox] = '·'
                        colors[oy][ox] = DIM

        # 行星
        for name, sym, color, orbit_r, speed, desc in self.PLANETS:
            a = self.angle * speed * (50 / orbit_r)
            px = int(cx + orbit_r * math.cos(a))
            py = int(cy + orbit_r * math.sin(a) * 0.38)
            self._put(canvas, colors, px, py, sym, color)

        # 渲染输出
        lines = []
        lines.append(f"{BOLD}{YELLOW}  << CodePlanet -- Programmer's Solar System Simulator >>{RESET}")
        lines.append("")

        for y in range(self.height):
            row = ""
            for x in range(self.width):
                ch = canvas[y][x]
                c = colors[y][x]
                if c:
                    row += f"{c}{ch}{RESET}"
                else:
                    row += ch
            lines.append(row)

        # 图例
        legend = f"  {DGRAY}"
        for name, sym, color, _, _, _ in self.PLANETS:
            legend += f"{color}{sym}{RESET}{DGRAY}={name}  "
        lines.append("")
        lines.append(legend + f"  {DGRAY}[Day {self.tick}]{RESET}")
        lines.append(f"  {DIM}Press Ctrl+C to exit | A cosmic journey by Picodesu{RESET}")

        # 清屏输出
        os.system('clear' if os.name != 'nt' else 'cls')
        print('\n'.join(lines))

    def run(self, fps=8):
        try:
            os.system('clear' if os.name != 'nt' else 'cls')
            print(f"{BOLD}{YELLOW}  Launching CodePlanet...{RESET}")
            time.sleep(0.8)
            while True:
                self.render()
                self.angle += 1
                self.tick += 1
                time.sleep(1.0 / fps)
        except KeyboardInterrupt:
            print(f"\n\n  {BOLD}{YELLOW}Thanks for visiting CodePlanet!{RESET}")
            print(f"  {DGRAY}\"The cosmos is within us. We are made of star-stuff.\"")
            print(f"   -- Carl Sagan{RESET}")
            print(f"\n  {DIM}-- Picodesu/CTest{RESET}\n")


def show_info():
    print(f"""{BOLD}{YELLOW}
  ============================================================
              CodePlanet v1.0
       Programmer's Solar System Simulator
  ============================================================{RESET}
  A tiny ASCII solar system that lives in your terminal.

  Watch planets orbit the sun, stars twinkle across the
  void, and shooting stars streak through the darkness.

  It's a cosmic screensaver for the nerdy soul.

{BOLD}  Usage:{RESET}
    python3 codeplanet.py          # 启动模拟
    python3 codeplanet.py --info   # 查看说明

{BOLD}  Planets:{RESET}
    * Mercury   o Venus     @ Earth    + Mars
    O Jupiter   0 Saturn

{BOLD}  Quote:{RESET}
  {DGRAY}\"Somewhere, something incredible is waiting to be known.\"
   -- Carl Sagan{RESET}

  {DIM}-- Picodesu/CTest{RESET}
""")


if __name__ == "__main__":
    if "--info" in sys.argv or "-h" in sys.argv or "--help" in sys.argv:
        show_info()
    else:
        random.seed()
        planet = CodePlanet()
        planet.run()
