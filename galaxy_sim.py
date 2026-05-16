#!/usr/bin/env python3
"""
galaxy_sim.py — ASCII Galaxy Simulator 🌌

A mini N-body gravitational simulation of a spiral galaxy,
rendered as a real-time terminal animation with ANSI colors.

Stars are born in spiral arms, orbit a galactic core, and
are color-coded by temperature (blue = hot, yellow = warm, red = cool).

Usage:
    python3 galaxy_sim.py              # default: 200 stars, 30 fps
    python3 galaxy_sim.py --stars 400  # denser galaxy
    python3 galaxy_sim.py --fps 15     # slower animation
    python3 galaxy_sim.py --arms 4     # four-armed spiral
    python3 galaxy_sim.py --static     # single frame (GitHub-safe)

Controls (while running):
    Ctrl+C to exit gracefully
"""

import math
import random
import sys
import time
import os
import argparse

# ─── ANSI Colors ───────────────────────────────────────────────
RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"

# Star temperature colors (RGB via 256-color)
COLOR_BLUE   = "\033[38;5;39m"    # hot O/B stars
COLOR_WHITE  = "\033[38;5;255m"   # A stars
COLOR_YELLOW = "\033[38;5;220m"   # G/K stars like our Sun
COLOR_ORANGE = "\033[38;5;208m"   # K stars
COLOR_RED    = "\033[38;5;196m"   # M dwarfs
COLOR_CORE   = "\033[38;5;226m"   # galactic core (bright yellow)
COLOR_CORE2  = "\033[38;5;214m"   # core glow
COLOR_DUST   = "\033[38;5;94m"    # dark dust lanes
COLOR_STAT   = "\033[38;5;141m"   # stats panel
COLOR_TITLE  = "\033[38;5;201m"   # title

STAR_CHARS = ["*", "+", "·", "•", "✦", "✧", "★"]
DUST_CHARS = ["·", "∙", "∘"]

# ─── Star Temperature Map ─────────────────────────────────────
TEMP_COLORS = [
    (0.95, COLOR_RED),      # coolest
    (0.75, COLOR_ORANGE),
    (0.55, COLOR_YELLOW),
    (0.35, COLOR_WHITE),
    (0.0,  COLOR_BLUE),     # hottest
]

def get_star_color(temperature):
    """Map temperature [0,1] to ANSI color. 0=hot, 1=cool."""
    for threshold, color in TEMP_COLORS:
        if temperature >= threshold:
            return color
    return COLOR_BLUE

# ─── Star Class ────────────────────────────────────────────────
class Star:
    __slots__ = ['x', 'y', 'vx', 'vy', 'mass', 'temperature', 'char', 'arm', 'phase']

    def __init__(self, x, y, vx, vy, mass, temperature, arm=0, phase=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.temperature = temperature
        self.char = random.choice(STAR_CHARS)
        self.arm = arm
        self.phase = phase

# ─── Galaxy Simulation ────────────────────────────────────────
class GalaxySimulator:
    def __init__(self, width=80, height=40, num_stars=200, num_arms=2,
                 rotation_speed=0.008, fps=30):
        self.width = width
        self.height = height
        self.num_stars = num_stars
        self.num_arms = num_arms
        self.rotation_speed = rotation_speed
        self.fps = fps
        self.stars = []
        self.time_step = 0
        self.core_mass = 500.0
        self.G = 0.5  # gravitational constant
        self.damping = 0.9995  # tiny energy loss for stability
        self._init_stars()

    def _init_stars(self):
        """Create stars distributed along logarithmic spiral arms."""
        for i in range(self.num_stars):
            arm = i % self.num_arms
            arm_angle = (2 * math.pi * arm) / self.num_arms

            # Logarithmic spiral: r = a * e^(b*theta)
            b = 0.3  # spiral tightness
            r_min = 2.0
            r_max = min(self.width, self.height) * 0.45
            r = r_min + (r_max - r_min) * (random.random() ** 0.6)

            a = r_min / math.exp(b * 0)
            theta = math.log(r / a) / b if r > a else random.uniform(0, 2 * math.pi)

            # Add scatter for natural look
            scatter_r = r * random.uniform(-0.15, 0.15)
            scatter_theta = random.uniform(-0.4, 0.4)

            final_r = max(1.5, r + scatter_r)
            final_theta = arm_angle + theta + scatter_theta

            x = final_r * math.cos(final_theta)
            y = final_r * math.sin(final_theta) * 0.5  # compress Y for terminal aspect ratio

            # Orbital velocity (roughly Keplerian)
            v_mag = math.sqrt(self.G * self.core_mass / max(final_r, 1.0)) * 0.7
            vx = -v_mag * math.sin(final_theta)
            vy =  v_mag * math.cos(final_theta) * 0.5

            # Star properties
            mass = random.uniform(0.1, 2.0)
            temperature = random.betavariate(2, 3)  # bias toward cooler stars
            phase = random.uniform(0, math.pi * 2)

            self.stars.append(Star(x, y, vx, vy, mass, temperature, arm, phase))

        # Add a few "blobs" near the core (bulge stars)
        for _ in range(self.num_stars // 10):
            x = random.gauss(0, 3)
            y = random.gauss(0, 1.5)
            r = math.sqrt(x*x + y*4)
            v_mag = math.sqrt(self.G * self.core_mass / max(r, 1.0)) * 0.5
            theta = math.atan2(y * 2, x)
            vx = -v_mag * math.sin(theta) * random.uniform(0.3, 0.8)
            vy =  v_mag * math.cos(theta) * 0.5 * random.uniform(0.3, 0.8)
            temp = random.uniform(0.7, 1.0)  # bulge stars are older/cooler
            self.stars.append(Star(x, y, vx, vy, 0.5, temp, -1, 0))

    def update(self):
        """Advance simulation by one time step."""
        self.time_step += 1
        frame_angle = self.rotation_speed
        cos_a = math.cos(frame_angle)
        sin_a = math.sin(frame_angle)

        for s in self.stars:
            # Gravitational force from core
            r2 = s.x * s.x + s.y * s.y + 1.0  # softening factor
            r = math.sqrt(r2)
            F = self.G * self.core_mass / r2

            ax = -F * s.x / r
            ay = -F * s.y / r

            s.vx += ax
            s.vy += ay
            s.vx *= self.damping
            s.vy *= self.damping
            s.x += s.vx
            s.y += s.vy

            # Rotate in reference frame
            new_x = s.x * cos_a - s.y * sin_a
            new_y = s.x * sin_a + s.y * cos_a
            s.x = new_x
            s.y = new_y

    def render(self):
        """Render the galaxy to an ANSI frame."""
        canvas = [[' '] * self.width for _ in range(self.height)]

        for s in self.stars:
            sx = int(s.x * (self.width / 2) / (self.width * 0.5) + self.width / 2)
            sy = int(s.y * (self.height / 2) / (self.height * 0.5) + self.height / 2)

            if 0 <= sx < self.width and 0 <= sy < self.height:
                canvas[sy][sx] = s.char

        lines = []

        # Title
        title = "G A L A X Y   S I M U L A T O R"
        title_pad = (self.width - len(title)) // 2
        lines.append(f"{COLOR_TITLE}{' ' * max(0, title_pad)}{BOLD}{title}{RESET}")

        # Canvas
        for y in range(self.height):
            row_chars = []
            for x in range(self.width):
                ch = canvas[y][x]
                if ch == ' ':
                    row_chars.append(ch)
                elif ch in STAR_CHARS:
                    dx = (x - self.width / 2) / (self.width / 2)
                    dy = (y - self.height / 2) / (self.height / 2)
                    dist = math.sqrt(dx * dx + dy * dy * 4)

                    if dist < 0.08:
                        color = COLOR_CORE if random.random() > 0.3 else COLOR_CORE2
                        char = random.choice(["*", "✦", "★", "●"])
                    elif dist < 0.15:
                        color = COLOR_WHITE
                        char = ch
                    else:
                        idx = y * self.width + x
                        temp = (hash(f"{idx}{self.time_step // 5}") % 100) / 100.0
                        color = get_star_color(temp)
                        char = ch

                    row_chars.append(f"{color}{char}{RESET}")
                else:
                    row_chars.append(ch)

            lines.append(''.join(row_chars))

        # Stats panel
        total_energy = sum(0.5 * s.mass * (s.vx**2 + s.vy**2) for s in self.stars)
        blue_count = sum(1 for s in self.stars if s.temperature < 0.35)
        red_count = sum(1 for s in self.stars if s.temperature > 0.75)

        stats = [
            f"{COLOR_STAT}{BOLD}{'─' * self.width}{RESET}",
            (f" {COLOR_STAT}Stars: {len(self.stars)} | "
             f"Core: {self.core_mass:.0f} M | "
             f"Blue: {blue_count} | Red: {red_count} | "
             f"Step: {self.time_step} | "
             f"Energy: {total_energy:.0f} J{RESET}"),
            (f" {COLOR_STAT}Arms: {self.num_arms} | "
             f"Speed: {self.rotation_speed:.3f} rad/frame | "
             f"FPS: {self.fps}{RESET}"),
            f"{COLOR_STAT}{BOLD}{'─' * self.width}{RESET}",
            f" {DIM}Ctrl+C to exit | tip: --stars 400 --arms 4{RESET}",
        ]
        lines.extend(stats)

        return '\n'.join(lines)

    def run(self):
        """Main animation loop."""
        try:
            sys.stdout.write("\033[?25l")  # hide cursor
            sys.stdout.flush()

            while True:
                self.update()
                frame = self.render()
                sys.stdout.write("\033[H\033[J")
                sys.stdout.write(frame)
                sys.stdout.flush()
                time.sleep(1.0 / self.fps)

        except KeyboardInterrupt:
            pass
        finally:
            sys.stdout.write("\033[?25h")  # show cursor
            sys.stdout.write(RESET)
            sys.stdout.flush()
            print(f"\n{'='*50}")
            print(f"  Galaxy simulation ended after {self.time_step} steps")
            print(f"  Stars simulated: {len(self.stars)}")
            print(f"  Spiral arms: {self.num_arms}")
            print(f"  Thanks for visiting the cosmos! 🌌")
            print(f"{'='*50}\n")


# ─── Static Renderer (for GitHub preview) ──────────────────────
def render_static(width=80, height=30, num_stars=200, num_arms=2):
    """Render a single frame as plain text (no ANSI, safe for GitHub)."""
    sim = GalaxySimulator(width, height, num_stars, num_arms, fps=999)
    for _ in range(50):
        sim.update()

    canvas = [[' '] * width for _ in range(height)]
    for s in sim.stars:
        sx = int(s.x * (width / 2) / (width * 0.5) + width / 2)
        sy = int(s.y * (height / 2) / (height * 0.5) + height / 2)
        if 0 <= sx < width and 0 <= sy < height:
            canvas[sy][sx] = s.char

    lines = []
    lines.append("G A L A X Y   S I M U L A T O R")
    lines.append("=" * width)
    for row in canvas:
        lines.append(''.join(row))
    lines.append("=" * width)
    lines.append(f"Stars: {len(sim.stars)} | Arms: {num_arms} | Core mass: {sim.core_mass}")
    lines.append("Run with: python3 galaxy_sim.py")
    return '\n'.join(lines)


# ─── CLI ───────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="ASCII Galaxy Simulator — watch a spiral galaxy spin in your terminal!",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 galaxy_sim.py                  # Default 200-star galaxy
  python3 galaxy_sim.py --stars 500      # Dense galaxy cluster
  python3 galaxy_sim.py --arms 4 --fps 20  # Four-armed spiral, slower
  python3 galaxy_sim.py --static         # Single frame (no animation)
        """
    )
    parser.add_argument('--stars', type=int, default=200,
                        help='Number of stars (default: 200)')
    parser.add_argument('--arms', type=int, default=2,
                        help='Number of spiral arms (default: 2)')
    parser.add_argument('--fps', type=int, default=30,
                        help='Frames per second (default: 30)')
    parser.add_argument('--speed', type=float, default=0.008,
                        help='Rotation speed in rad/frame (default: 0.008)')
    parser.add_argument('--static', action='store_true',
                        help='Render a single static frame (no animation)')
    parser.add_argument('--width', type=int, default=80,
                        help='Terminal width (default: 80)')
    parser.add_argument('--height', type=int, default=30,
                        help='Terminal height (default: 30)')

    args = parser.parse_args()

    if args.static:
        print(render_static(args.width, args.height, args.stars, args.arms))
    else:
        sim = GalaxySimulator(
            width=args.width,
            height=args.height,
            num_stars=args.stars,
            num_arms=args.arms,
            rotation_speed=args.speed,
            fps=args.fps,
        )
        print(f"\n  Initializing galaxy with {args.stars} stars...")
        print(f"  {args.arms} spiral arms | Core mass: {sim.core_mass}")
        print(f"  Press Ctrl+C to exit\n")
        time.sleep(1.5)
        sim.run()


if __name__ == '__main__':
    main()
