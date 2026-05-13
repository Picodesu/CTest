#!/usr/bin/env python3
"""
量子猫模拟器 - 薛定谔的猫 2.0
Quantum Cat Simulator - Schrödinger's Cat 2.0

在这个程序中，每一只猫都处于生与死的叠加态
直到你打开盒子的那一刻，宇宙才会做出选择。

By: CTest Lab / Quantum Philosophy Division
"""

import random
import time
import sys
import hashlib
from datetime import datetime


# ============ ASCII Art ============

CAT_ALIVE = """
    /\\_/\
   ( o.o )
    > ^ <
   /|   |\\
  (_|   |_)
  [  活着  ]
"""

CAT_DEAD = """
    /\\_/\
   ( x.x )
    > ~ <
   /|   |\\
  (_|   |_)
  [  安息  ]
"""

CAT_SUPERPOSITION = """
    /\\_/\
   ( ?.? )
    > ~ <
   /|   |\\
  (_|   |_)
  [ 叠加态 ]
"""

CAT_BOX_CLOSED = """
   ___________
  |           |
  |  +-----+  |
  |  | ? ? |  |
  |  |~???~|  |
  |  +-----+  |
  |  [密封中]  |
  |___________|
"""

CAT_BOX_OPEN = """
   ___________
  |           |
  |  +-----+  |
  |  |     |  |
  |  |     |  |
  |  +-----+  |
  |  [已开启]  |
  |___________|
"""

# ============ 哲学语录 ============

OBSERVATIONS = [
    "波函数坍缩了。猫做出了它的选择。",
    "在你打开盒子的那一刻，宇宙分裂成了两个。",
    "量子态已解析。但猫似乎对此毫不在意。",
    "观测改变了一切。这就是量子世界的残酷美学。",
    "盒子打开的瞬间，可能性变成了现实。",
    "海森堡会说：你永远无法同时知道猫的心情和位置。",
    "费曼大概会说：这很简单，只是没人真正理解它。",
    "在这个宇宙里，猫活了下来。在另一个宇宙里...",
    "薛定谔本人可能已经后悔提出这个思想实验了。",
    "猫的量子态已退相干。欢迎来到经典世界。",
]

PHILOSOPHY = [
    "活着本身就是最大的概率事件。",
    "每一次观测都是一次选择，每一次选择都是一次创造。",
    "猫不在乎量子力学。猫只在乎罐头。",
    "在代码的世界里，我们都是薛定谔的程序员 -- 同时在写bug和没有写。",
    "确定性是幻觉，不确定性才是宇宙的默认设置。",
    "如果猫能编程，它们大概会写 Haskell -- 纯函数，无副作用。",
    "盒子外面的世界是经典的。盒子里面是量子的。你的代码是混沌的。",
    "观测者效应：当你盯着代码看太久，bug就会消失（或者出现更多）。",
    "叠加态是优雅的。坍缩是无奈的。",
    "在所有平行宇宙中，总有一个宇宙的你的代码一次就编译通过了。",
]


def quantum_seed():
    """用当前时间的纳秒级精度生成一个'量子随机数'"""
    now = datetime.now()
    nano = now.microsecond * 1000 + random.randint(0, 999)
    return int(hashlib.md5(f"{now.timestamp()}:{nano}".encode()).hexdigest()[:8], 16)


def opening_animation():
    """开箱动画"""
    frames = [
        CAT_BOX_CLOSED,
        '   ___________\n  |           |\n  |  +-----+  |\n  |  | ... |  |\n  |  |~..~ |  |\n  |  +-----+  |\n  |  [开启中]  |\n  |___________|',
        CAT_BOX_OPEN,
    ]
    for frame in frames:
        print(frame)
        time.sleep(0.4)
        # Move cursor up to overwrite
        sys.stdout.write("\033[F" * 9)
        sys.stdout.flush()


def show_banner():
    print("=" * 55)
    print("  [ QUANTUM CAT SIMULATOR v2.0 ]")
    print("  CTest Lab / Quantum Philosophy Division")
    print("=" * 55)
    print()
    print("  在量子世界里，这只猫同时活着和死去。")
    print("  只有当你观测的那一刻，现实才会确定。")
    print()


def main():
    show_banner()

    cat_name = input("  给你的量子猫起个名字（回车随机分配）: ").strip()
    if not cat_name:
        names = ["薛定谔", "费曼", "海森堡", "玻尔", "狄拉克", "图灵", "特斯拉"]
        cat_name = random.choice(names)
        print(f"  随机分配名字: {cat_name}")

    print()
    print(f"  {cat_name} 的量子态初始化中...")
    print("  状态: 叠加态 (alive + dead)")
    print()

    opening_count = 0

    while True:
        print("  [1] 打开盒子（观测量子态）")
        print("  [2] 查看猫的量子状态报告")
        print("  [3] 进行量子纠缠实验")
        print("  [4] 退出（让猫继续叠加）")
        print()

        choice = input("  > ").strip()
        print()

        if choice == "1":
            opening_count += 1
            opening_animation()

            quantum_num = quantum_seed()
            is_alive = quantum_num % 2 == 0

            print(CAT_BOX_OPEN)
            time.sleep(0.3)

            if is_alive:
                print(CAT_ALIVE)
            else:
                print(CAT_DEAD)

            print()
            print(f"  [{cat_name}] 第 {opening_count} 次观测结果:")
            print(f"  {random.choice(OBSERVATIONS)}")
            print()
            print(f"  量子随机数: {quantum_num} ({'偶数 -> 活' if is_alive else '奇数 -> 死'})")
            print(f"  理论概率: 50.00% | 实际结果: {'存活' if is_alive else '安息'}")
            print()
            print(f"  {random.choice(PHILOSOPHY)}")
            print()
            print("  ...")
            print(f"  {cat_name} 重新进入了叠加态。盒子已关闭。")
            print()

        elif choice == "2":
            print(CAT_SUPERPOSITION)
            print()
            quantum_num = quantum_seed()
            probability = (quantum_num % 10000) / 100
            mood = random.choice(["好奇", "困倦", "饥饿", "神秘", "超然", "量子态"])
            print(f"  {cat_name} 的当前量子状态报告:")
            print(f"  + 叠加度: {probability:.2f}%")
            print(f"  + 纠缠粒子数: {quantum_num % 42 + 1}")
            print(f"  + 退相干时间: {quantum_num % 60 + 1}s")
            print(f"  + 猫的心情: {mood}")
            print()
            print("  注意: 任何进一步的观测都会改变这个结果。海森堡对此表示确认。")
            print()

        elif choice == "3":
            print("  量子纠缠实验启动...")
            print()
            time.sleep(1)

            entangled_names = [
                "另一个宇宙的" + cat_name,
                "反物质" + cat_name,
                "平行世界的" + cat_name,
                "四维空间的" + cat_name,
                "量子场论中的" + cat_name,
            ]
            entangled = random.choice(entangled_names)

            print(f"  {cat_name} 已与 {entangled} 建立量子纠缠!")
            print()
            time.sleep(0.5)

            q1 = quantum_seed()
            q2 = q1 ^ 0xFFFFFFFF

            bell = "通过" if random.random() > 0.3 else "被量子力学打破"
            print(f"  纠缠态分析:")
            print(f"  - {cat_name} 的状态值: {q1}")
            print(f"  - {entangled} 的状态值: {q2}")
            print(f"  - Bell 不等式验证: {bell}")
            print(f"  - 纠缠保真度: {random.uniform(95.0, 99.99):.2f}%")
            print()
            print(f"  {random.choice(PHILOSOPHY)}")
            print()

        elif choice == "4":
            print(f"  你选择了让 {cat_name} 继续处于叠加态。")
            print(f"  这也许是最善良的选择。")
            print(f"  在某个平行宇宙里，你做出了不同的决定。")
            print()
            print(f"  总共观测次数: {opening_count}")
            if opening_count > 0:
                print(f"  建议: 过度观测会导致量子退相干。适度观测，善待你的猫。")
            print()
            print("  再见。愿量子力学与你同在。")
            break

        else:
            print("  无效选择。你的犹豫让猫多存活了一纳秒。")
            print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  [Ctrl+C] 你强制中断了量子实验。")
        print("  猫的波函数已坍缩。希望你对自己的选择满意。")
        print()
