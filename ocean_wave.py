#!/usr/bin/env python3
"""
ocean_wave.py — ASCII Ocean Wave Simulator
A living, breathing ocean rendered in your terminal.

Features:
  - Multi-layer wave simulation (deep ocean swells + surface ripples)
  - Bioluminescent jellyfish that drift and pulse
  - Foam particles on wave crests
  - Day/night cycle with automatic ambient shift
  - Fish silhouettes swimming in the deep
  - Rain drops hitting the surface (toggle with 'r')
  - Starfield reflection on calm water (night only)
  - Keyboard controls: q/quit, r/rain, +/-speed, n/night toggle

Usage: python ocean_wave.py
       python ocean_wave.py --width 80 --height 24

No dependencies beyond Python 3.6+.
"""

import math
import random
import sys
import os
import time
import argparse
import shutil
from typing import List, Tuple, Optional


# -- ANSI helpers --

def rgb_fg(r: int, g: int, b: int) -> str:
    return f"\033[38;2;{r};{g};{b}m"

def rgb_bg(r: int, g: int, b: int) -> str:
    return f"\033[48;2;{r};{g};{b}m"

RESET = "\033[0m"
BOLD = "\033[1m"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
CLEAR = "\033[2J"
HOME = "\033[H"


# -- Noise (simple Perlin-like) --

class SimpleNoise:
    """Minimal 1D value noise for organic wave shapes."""
    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
        self.perm = list(range(256))
        self.rng.shuffle(self.perm)
        self.perm *= 2
        self.vals = [self.rng.random() for _ in range(256)]

    def _smooth(self, t: float) -> float:
        return t * t * (3 - 2 * t)

    def get(self, x: float) -> float:
        xi = int(math.floor(x)) & 255
        xf = x - math.floor(x)
        t = self._smooth(xf)
        a = self.vals[self.perm[xi]]
        b = self.vals[self.perm[xi + 1]]
        return a + (b - a) * t

    def fbm(self, x: float, octaves: int = 4) -> float:
        val, amp, freq = 0.0, 0.5, 1.0
        for _ in range(octaves):
            val += amp * self.get(x * freq)
            amp *= 0.5
            freq *= 2.0
        return val


noise = SimpleNoise(2026)


# -- Entities --

class Jellyfish:
    """A glowing jellyfish drifting in the ocean."""
    ART = [
        [r"  {W}   ", r" {W}W{W} ", r" {W}{W}{W}{W} ", r"  {W}   "],
        [r" {W}{W}{W}{W}{W} ", r"{W}{C}{C}{W}{W}{W}", r"{W}{W}{C}{C}{W}{W}", r" {W}{W}{W}{W}{W} "],
        [r"  /  \ ", r" / {T}  ", r" \  {T}/ ", r"  \  / "],
        [r"  | |  ", r"  | |  ", r"  | |  ", r"      "],
    ]

    def __init__(self, x: float, y: float, w: int, h: int, t: float):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.phase = random.uniform(0, math.pi * 2)
        self.speed = random.uniform(0.15, 0.4)
        self.drift = random.uniform(-0.05, 0.05)
        self.pulse_rate = random.uniform(1.5, 3.0)
        self.size = random.choice([0.7, 1.0, 1.3])
        self.hue = random.choice([
            (0, 220, 255),
            (180, 100, 255),
            (100, 180, 255),
            (255, 100, 200),
        ])
        self.tentacle_chars = list("~}|{")

    def update(self, dt: float, t: float):
        self.x += self.drift * dt
        self.y += math.sin(t * self.pulse_rate + self.phase) * 0.3 * dt
        if self.x < -5:
            self.x = self.w + 3
        if self.x > self.w + 5:
            self.x = -3
        self.y = max(self.y, 4)

    def draw(self, buf: List[List[str]], t: float):
        pulse = 0.5 + 0.5 * math.sin(t * self.pulse_rate + self.phase)
        r = int(self.hue[0] * pulse)
        g = int(self.hue[1] * pulse)
        b = int(self.hue[2] * pulse)
        glow = int(100 + 155 * pulse)

        ix, iy = int(self.x), int(self.y)
        for dx in range(-2, 3):
            for dy in range(-1, 1):
                px, py = ix + dx, iy + dy
                if 0 <= px < self.w and 0 <= py < self.h:
                    char = BOLD + rgb_fg(min(255, r + 40), min(255, g + 40), min(255, b + 40))
                    if dy == -1 and abs(dx) <= 1:
                        buf[py][px] = char + ")" + RESET
                    elif dy == 0:
                        buf[py][px] = char + (")" if dx < 0 else "(" if dx > 0 else "o") + RESET

        for i in range(3):
            tx = ix - 1 + i
            for ty in range(iy + 1, min(iy + 4, self.h)):
                if 0 <= tx < self.w:
                    wave = int(math.sin(t * 2 + i + ty * 0.5) * 0.8)
                    ttx = tx + wave
                    if 0 <= ttx < self.w:
                        tc = self.tentacle_chars[(int(t * 3 + ty + i)) % len(self.tentacle_chars)]
                        brightness = max(80, glow - (ty - iy) * 30)
                        buf[ty][ttx] = rgb_fg(int(r * brightness / 255), int(g * brightness / 255), int(b * brightness / 255)) + tc + RESET


class Fish:
    """A small fish silhouette swimming in the deep."""
    SHAPES = [
        [")>>", ">>)", ">><", "><>"],
        ["><>", ">>-", ">>=", ">->"],
    ]

    def __init__(self, w: int, h: int):
        self.reset(w, h, initial=True)

    def reset(self, w: int, h: int, initial: bool = False):
        self.w = w
        self.h = h
        self.dir = random.choice([-1, 1])
        self.y = random.randint(max(h // 2 + 2, 8), h - 3)
        self.x = -4 if self.dir == 1 else w + 4
        self.speed = random.uniform(0.3, 0.8)
        self.shape_idx = random.randint(0, len(Fish.SHAPES) - 1)
        self.color = random.choice([
            (255, 200, 80),
            (200, 200, 120),
            (255, 150, 50),
        ])

    def update(self, dt: float):
        self.x += self.dir * self.speed * dt * 8
        self.y += math.sin(self.x * 0.1) * 0.05

    def draw(self, buf: List[List[str]]):
        if self.dir == 1:
            shape = Fish.SHAPES[self.shape_idx][0]
        else:
            shape = Fish.SHAPES[self.shape_idx][0][::-1]
        ix, iy = int(self.x), int(self.y)
        for i, ch in enumerate(shape):
            px, py = ix + i, iy
            if 0 <= px < self.w and 0 <= py < self.h:
                buf[py][px] = rgb_fg(*self.color) + ch + RESET

    def is_offscreen(self) -> bool:
        return (self.dir == 1 and self.x > self.w + 5) or (self.dir == -1 and self.x < -5)


class Raindrop:
    """A raindrop hitting the ocean surface."""
    def __init__(self, w: int):
        self.x = random.randint(0, w - 1)
        self.y = 0
        self.speed = random.uniform(1.5, 3.0)
        self.w = w
        self.char = random.choice(["|", ":", "."])
        self.splashed = False
        self.splash_t = 0.0

    def update(self, dt: float, h: int):
        self.y += self.speed * dt * 10
        if self.y >= h * 0.4 and not self.splashed:
            self.splashed = True
            self.splash_t = 0.0

    def draw(self, buf: List[List[str]], t: float, h: int):
        if self.splashed:
            self.splash_t += 0.1
            if self.splash_t < 1.0:
                radius = int(self.splash_t * 3)
                for dx in range(-radius, radius + 1):
                    px = int(self.x) + dx
                    py = int(h * 0.4)
                    if 0 <= px < self.w and 0 <= py < h:
                        intensity = max(0, 1.0 - self.splash_t)
                        buf[py][px] = rgb_fg(
                            int(150 * intensity), int(200 * intensity), int(255 * intensity)
                        ) + ("~" if abs(dx) == radius else ".") + RESET
            return
        iy = int(self.y)
        if 0 <= iy < h and 0 <= int(self.x) < self.w:
            buf[iy][int(self.x)] = rgb_fg(120, 160, 255) + self.char + RESET

    def is_done(self) -> bool:
        return self.splashed and self.splash_t >= 1.0


# -- Ocean Renderer --

class Ocean:
    CHARS = " .:-=+*#%@"
    WAVE_CHARS = ["~", "-", "~", "="]
    FOAM_CHARS = ["*", ".", "'", "`"]

    def __init__(self, width: int, height: int):
        self.w = width
        self.h = height
        self.t = 0.0
        self.speed = 1.0
        self.raining = False
        self.night_mode = False
        self.night_t = 0.0

        self.surface_y = int(height * 0.4)

        self.jellies: List[Jellyfish] = []
        for _ in range(random.randint(2, 4)):
            jx = random.uniform(3, width - 3)
            jy = random.uniform(self.surface_y + 3, height - 4)
            self.jellies.append(Jellyfish(jx, jy, width, height, self.t))

        self.fish: List[Fish] = []
        for _ in range(3):
            f = Fish(width, height)
            f.x = random.uniform(0, width)
            self.fish.append(f)

        self.rain: List[Raindrop] = []

        self.stars = [(random.randint(0, width - 1), random.randint(0, self.surface_y - 2))
                      for _ in range(width // 4)]

    def update(self, dt: float):
        self.t += dt * self.speed

        if self.night_mode:
            self.night_t = min(1.0, self.night_t + dt * 0.5)
        else:
            self.night_t = max(0.0, self.night_t - dt * 0.5)

        for j in self.jellies:
            j.update(dt, self.t)
        for f in self.fish:
            f.update(dt)
        self.fish = [f for f in self.fish if not f.is_offscreen()]
        if len(self.fish) < 3 and random.random() < 0.01:
            self.fish.append(Fish(self.w, self.h))

        if self.raining and random.random() < 0.3:
            self.rain.append(Raindrop(self.w))
        for r in self.rain:
            r.update(dt, self.h)
        self.rain = [r for r in self.rain if not r.is_done()]

    def _sky_color(self, y: int) -> Tuple[int, int, int]:
        night = self.night_t
        r = int(20 * (1 - night) + 5 * night)
        g = int(30 * (1 - night) + 8 * night)
        b = int(60 * (1 - night) + 25 * night)
        return r, g, b

    def _water_color(self, depth_ratio: float, t: float) -> Tuple[int, int, int]:
        wave = math.sin(t * 0.5 + depth_ratio * 3) * 15
        night = self.night_t
        sr = int((10 + wave * 0.5) * (1 - night * 0.5))
        sg = int((60 + depth_ratio * (-40) + wave) * (1 - night * 0.3))
        sb = int((120 + depth_ratio * (-60) + wave * 0.3) * (1 - night * 0.2))
        return max(0, min(255, sr)), max(0, min(255, sg)), max(0, min(255, sb))

    def render(self) -> str:
        buf: List[List[str]] = [[" " for _ in range(self.w)] for _ in range(self.h)]

        for y in range(self.surface_y):
            sr, sg, sb = self._sky_color(y)
            fade = y / max(1, self.surface_y)
            sr = int(sr * (0.5 + 0.5 * fade))
            sg = int(sg * (0.5 + 0.5 * fade))
            sb = int(sb * (0.5 + 0.5 * fade))
            for x in range(self.w):
                if self.night_t > 0.3 and (x, y) in self.stars:
                    twinkle = (math.sin(self.t * 2 + x * 0.3 + y * 0.7) + 1) / 2
                    brightness = int(100 + 155 * twinkle * self.night_t)
                    buf[y][x] = rgb_fg(brightness, brightness, min(255, brightness + 40)) + "*" + RESET
                else:
                    buf[y][x] = rgb_bg(sr, sg, sb) + " " + RESET

        for x in range(self.w):
            wave1 = noise.fbm(x * 0.08 + self.t * 0.3, 3) * 3
            wave2 = math.sin(x * 0.15 + self.t * 0.8) * 1.2
            wave3 = math.sin(x * 0.3 + self.t * 1.5) * 0.5
            disp = wave1 + wave2 + wave3

            sy = int(self.surface_y + disp)

            is_crest = disp > 2.0

            for y in range(max(0, sy), self.h):
                depth = (y - self.surface_y) / max(1, self.h - self.surface_y)
                wr, wg, wb = self._water_color(depth, self.t)

                ray_x = x * 0.05 + self.t * 0.2
                ray = max(0, math.sin(ray_x) * math.cos(depth * 3 + self.t * 0.3))
                if ray > 0.7 and depth < 0.5 and self.night_t < 0.5:
                    wr = min(255, int(wr + 30 * ray))
                    wg = min(255, int(wg + 40 * ray))
                    wb = min(255, int(wb + 20 * ray))

                caustic = math.sin(x * 0.2 + self.t * 0.4) * math.sin(y * 0.15 + self.t * 0.3)
                if caustic > 0.8 and depth < 0.15 and self.night_t < 0.5:
                    wg = min(255, wg + 25)
                    wb = min(255, wb + 15)

                char_idx = min(len(self.CHARS) - 1, int(depth * len(self.CHARS) * 0.7))
                ch = self.CHARS[char_idx]

                buf[y][x] = rgb_fg(wr, wg, wb) + ch + RESET

            if is_crest and sy < self.h:
                foam_ch = random.choice(self.FOAM_CHARS)
                buf[sy][x] = rgb_fg(220, 240, 255) + BOLD + foam_ch + RESET

            if 0 <= sy < self.h:
                wc = self.WAVE_CHARS[int(abs(disp) + self.t) % len(self.WAVE_CHARS)]
                wr, wg, wb = self._water_color(0, self.t)
                buf[sy][x] = rgb_fg(min(255, wr + 50), min(255, wg + 50), min(255, wb + 30)) + wc + RESET

        for f in self.fish:
            f.draw(buf)

        for j in self.jellies:
            j.draw(buf, self.t)

        for r in self.rain:
            r.draw(buf, self.t, self.h)

        for x in range(self.w):
            if random.random() < 0.02:
                by = self.h - 1
                buf[by][x] = rgb_fg(40, 35, 20) + random.choice([".", ",", "`"]) + RESET

        lines = []
        for row in buf:
            line = "".join(row)
            lines.append(line)
        return "\n".join(lines)


# -- Main Loop --

def main():
    parser = argparse.ArgumentParser(description="ASCII Ocean Wave Simulator")
    parser.add_argument("--width", type=int, default=None, help="Terminal width")
    parser.add_argument("--height", type=int, default=None, help="Terminal height")
    args = parser.parse_args()

    size = shutil.get_terminal_size()
    w = args.width or size.columns
    h = args.height or min(size.lines - 1, 30)

    ocean = Ocean(w, h)
    last_time = time.time()
    fps_counter = 0
    fps_time = 0.0

    import tty
    import termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setcbreak(fd)
        sys.stdout.write(HIDE_CURSOR + CLEAR)
        sys.stdout.flush()

        while True:
            try:
                import select
                if select.select([sys.stdin], [], [], 0)[0]:
                    ch = sys.stdin.read(1)
                    if ch in ("q", "Q", "\x1b"):
                        break
                    elif ch in ("r", "R"):
                        ocean.raining = not ocean.raining
                    elif ch in ("n", "N"):
                        ocean.night_mode = not ocean.night_mode
                    elif ch in ("+", "="):
                        ocean.speed = min(3.0, ocean.speed + 0.2)
                    elif ch in ("-", "_"):
                        ocean.speed = max(0.1, ocean.speed - 0.2)
            except Exception:
                pass

            now = time.time()
            dt = min(0.1, now - last_time)
            last_time = now
            ocean.update(dt)

            fps_counter += 1
            fps_time += dt
            if fps_time > 1.0:
                fps_counter = 0
                fps_time = 0.0

            frame = ocean.render()

            night_label = "Moon" if ocean.night_t > 0.5 else "Sun"
            rain_label = "Rain ON" if ocean.raining else "Rain off"
            status = f" [{night_label} x{ocean.speed:.1f} {rain_label}] q:quit r:rain n:night +/-:speed "
            status_line = rgb_fg(100, 150, 180) + status.center(w) + RESET

            sys.stdout.write(HOME + frame + "\n" + status_line)
            sys.stdout.flush()

            time.sleep(0.05)

    except KeyboardInterrupt:
        pass
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        sys.stdout.write(SHOW_CURSOR + RESET)
        sys.stdout.flush()


if __name__ == "__main__":
    main()
