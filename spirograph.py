#!/usr/bin/env python3
"""
Spirograph — 万花尺 SVG 几何艺术生成器
=======================================

数学之美，一笔画成。

使用内旋轮线（hypotrochoid）方程生成万花尺图案。
三个参数 (R, r, d) 的不同组合创造出无穷无尽的几何花纹。
每日运行由日期作为种子，产生独一无二的图案。

方程:
  x(t) = (R - r) * cos(t) + d * cos((R - r) / r * t)
  y(t) = (R - r) * sin(t) - d * sin((R - r) / r * t)

Usage:
    python3 spirograph.py                    # 输出到 spirograph.svg
    python3 spirograph.py output.svg         # 指定文件名
    python3 spirograph.py output.svg 20260514  # 指定种子
"""

import math
import random
import sys
from datetime import datetime


# ── 调色板 ──────────────────────────────────────────────
PALETTE = [
    "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4",
    "#FFEAA7", "#DDA0DD", "#98D8C8", "#F7DC6F",
    "#BB8FCE", "#85C1E9", "#F1948A", "#82E0AA",
    "#F0B27A", "#AED6F1", "#D5DBDB", "#FADBD8",
]


def gcd(a: int, b: int) -> int:
    """最大公约数"""
    while b:
        a, b = b, a % b
    return a


def hypotrochoid_points(R: int, r: int, d: int, n_points: int = 2000):
    """
    计算内旋轮线上的点。

    R: 固定圆半径
    r: 滚动圆半径
    d: 笔尖到滚动圆圆心的距离
    返回: [(x, y), ...]
    """
    # 曲线闭合周期: t 从 0 到 2π * r / gcd(R, r)
    period = 2 * math.pi * r / gcd(R, r)

    points = []
    for i in range(n_points + 1):
        t = period * i / n_points
        x = (R - r) * math.cos(t) + d * math.cos((R - r) / r * t)
        y = (R - r) * math.sin(t) - d * math.sin((R - r) / r * t)
        points.append((x, y))
    return points


def points_to_svg_path(points):
    """将点列表转换为SVG path字符串"""
    if not points:
        return ""
    first = points[0]
    parts = [f"M {first[0]:.2f},{first[1]:.2f}"]
    for x, y in points[1:]:
        parts.append(f"L {x:.2f},{y:.2f}")
    parts.append("Z")
    return " ".join(parts)


def generate_spirograph(seed: int, width: int = 800, height: int = 600):
    """
    根据种子生成完整的万花尺SVG。

    返回: (svg_string, metadata_dict)
    """
    random.seed(seed)
    cx, cy = width / 2, height / 2

    # ── 随机参数 ──────────────────────────────────────
    n_curves = random.randint(3, 6)
    layers = []

    for i in range(n_curves):
        R = random.randint(120, 220)
        r = random.randint(15, 70)
        # d 可以大于 r（产生外凸花瓣）也可以小于 r（内收）
        d = random.randint(int(r * 0.3), int(r * 1.5))
        color = random.choice(PALETTE)
        opacity = round(random.uniform(0.45, 0.85), 2)
        stroke_w = round(random.uniform(0.6, 2.2), 1)

        pts = hypotrochoid_points(R, r, d, n_points=3000)
        # 平移到画布中心
        pts = [(x + cx, y + cy) for x, y in pts]
        path_data = points_to_svg_path(pts)

        layers.append({
            "path": path_data,
            "color": color,
            "opacity": opacity,
            "stroke_w": stroke_w,
            "R": R, "r": r, "d": d,
        })

    # ── 装配 SVG ──────────────────────────────────────
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    curve_descs = " | ".join(
        f"R={l['R']} r={l['r']} d={l['d']}" for l in layers
    )

    paths_xml = []
    for l in layers:
        paths_xml.append(
            f'  <path d="{l["path"]}" '
            f'fill="none" stroke="{l["color"]}" '
            f'stroke-opacity="{l["opacity"]}" '
            f'stroke-width="{l["stroke_w"]}" '
            f'stroke-linecap="round" />'
        )

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<!-- Spirograph — 万花尺几何艺术 -->
<!-- Seed: {seed} | {date_str} -->
<!-- {curve_descs} -->
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 {width} {height}"
     width="{width}" height="{height}">
  <defs>
    <radialGradient id="bg" cx="50%" cy="50%" r="70%">
      <stop offset="0%"   stop-color="#16213e" />
      <stop offset="100%" stop-color="#0a0a1a" />
    </radialGradient>
  </defs>

  <!-- 深空背景 -->
  <rect width="100%" height="100%" fill="url(#bg)" />

  <!-- 万花尺图案 -->
{chr(10).join(paths_xml)}

  <!-- 信息栏 -->
  <text x="20" y="{height - 20}"
        fill="#555" font-family="monospace" font-size="11">
    spirograph.py | seed {seed} | {n_curves} curves | CTest
  </text>
</svg>'''

    meta = {
        "seed": seed,
        "n_curves": n_curves,
        "curves": [(l["R"], l["r"], l["d"], l["color"]) for l in layers],
    }
    return svg, meta


def main():
    # 解析参数
    now = datetime.now()
    if len(sys.argv) >= 3:
        output = sys.argv[1]
        seed = int(sys.argv[2])
    elif len(sys.argv) == 2:
        output = sys.argv[1]
        seed = int(now.strftime("%Y%m%d"))
    else:
        output = "spirograph.svg"
        seed = int(now.strftime("%Y%m%d%H"))  # 精确到小时，一天一个

    svg_content, meta = generate_spirograph(seed)

    with open(output, "w", encoding="utf-8") as f:
        f.write(svg_content)

    # 打印摘要
    print(f"=== Spirograph Generated ===")
    print(f"  File   : {output}")
    print(f"  Seed   : {seed}")
    print(f"  Curves : {meta['n_curves']}")
    for i, (R, r, d, c) in enumerate(meta["curves"]):
        print(f"    [{i+1}] R={R}  r={r}  d={d}  {c}")
    print(f"  Time   : {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Done. Open in browser or push to GitHub for preview!")


if __name__ == "__main__":
    main()
