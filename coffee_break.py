#!/usr/bin/env python3
"""
咖啡因禅院 ☕ — 程序员的量子咖啡机
运行方式: python coffee_break.py

每一杯咖啡都是一次存在主义选择。
每一口都是对熵增的温柔抵抗。
"""

import random
import time
import sys
import os

# ═══════════════════════════════════════════
#  ASCII 咖啡杯艺术
# ═══════════════════════════════════════════

FILLING_STAGES = [
    r"""
      ( (
       ) )
    .─────.
    | ░░░ |
    |     |
    '─────'
""",
    r"""
      ( (
       ) )
    .─────.
    | ▓▓▓ |
    | ░░░ |
    '─────'
""",
    r"""
      ( (
       ) )
    .─────.
    | ███ |
    | ▓▓▓ |
    '─────'
""",
    r"""
      ( (
       ) )
    .─────.
    | ~~~ |
    | ███ |
    '─────'
""",
    r"""
      ( (  )
       ) )
    .─────.
    | ≈≈≈ |  咖啡已满
    | ~~~ |
    '─────'
""",
]

STEAM = [
    r"""
      ( (
       ) )
    .─────.
    | ~~~ |
    | ███ |
    '─────'
      ~ ~
""",
    r"""
      ( (
       ) )
    .─────.
    | ~~~ |
    | ███ |
    '─────'
     ~   ~
""",
    r"""
      ( (
       ) )
    .─────.
    | ~~~ |
    | ███ |
    '─────'
    ~  ~  ~
""",
]

# ═══════════════════════════════════════════
#  哲学语录库 — 每一杯咖啡的灵魂伴侣
# ═══════════════════════════════════════════

COFFEE_PHILOSOPHY = [
    '"你调试的不是代码，是你对世界的执念。"',
    '"咖啡因不会让你写出更好的代码，但会让你写出更多代码。"',
    '"如果没人 review 你的代码，那它算写了吗？"',
    '"每杯咖啡都是一次 git commit —— 撤销是不可能的。"',
    '"世界上最远的距离，是你和你的显示器之间的那杯咖啡。"',
    '"bug 是 feature 的另一种表达方式。"',
    '"你今天写的代码，明天的你会感谢或诅咒。"',
    '"咖啡凉了可以再热，但过期的 deadline 就是过期了。"',
    '"while(coffee) { code(); } —— 这才是真正的无限循环。"',
    '"代码写不下去的时候，就去倒杯咖啡。灵感在杯底等你。"',
    '"一个没有咖啡的程序员，就像一个没有单元测试的项目 —— 能跑，但随时会崩。"',
    '"咖啡是液态的编译器，把混沌的想法编译成有序的代码。"',
    '"你不是在喝咖啡，你是在把熵灌进身体里对抗虚无。"',
    '"if (mood == \"写不动\"): coffee.else: coffee.also_coffee()"',
    '"有些代码像咖啡 —— 越苦越上头。"',
    '"人生的 segfault 可以用咖啡来 soft restart。"',
    '"最好的调试工具是一杯热咖啡和一颗不放弃的心。"',
    '"当你觉得代码很烂的时候，记住：至少你的咖啡很香。"',
    '"写代码就像冲咖啡 —— 水温不对，一切白费。"',
    '"程序员的一天：起床、咖啡、debug、咖啡、debug、咖啡、睡觉、repeat。"',
]

# ═══════════════════════════════════════════
#  咖啡因等级系统
# ═══════════════════════════════════════════

CAFFEINE_LEVELS = {
    0: ("☠️  已死亡", "你的代码也已经死了。快喝咖啡。"),
    1: ("💀 濒死态", "编译器都在为你默哀。"),
    2: ("😴 植物人", "你的眼睛还睁着，但灵魂不在。"),
    3: ("🥱 低功耗", "能跑，但像 Windows Vista 一样慢。"),
    4: ("😐 正常人", "基本功能恢复，但还没到巅峰。"),
    5: ("🙂 略有精神", "开始觉得代码也没那么难了。"),
    6: ("😊 咖啡因上升中", "手指在键盘上跳舞。"),
    7: ("🤩 效率巅峰", "你就是人形编译器！"),
    8: ("⚡ 超频状态", "能看到代码的量子态。"),
    9: ("🚀 光速运行", "时间线上的你已经开始写明天的代码了。"),
    10: ("🌌 涅槃", "你已经不是程序员了，你是代码本身。"),
}

# ═══════════════════════════════════════════
#  核心函数
# ═══════════════════════════════════════════

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def slow_print(text, delay=0.03):
    """逐字打印，制造仪式感"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def brew_coffee():
    """冲泡一杯咖啡（带仪式感动画）"""
    print("\n  ☕ 冲泡中...\n")
    for i, stage in enumerate(FILLING_STAGES):
        clear()
        print(f"\n  ☕ 咖啡因禅院 —— 第 {i+1} 级注入\n")
        print(stage)
        time.sleep(0.6)

    # 加蒸汽
    for steam in STEAM:
        clear()
        print("\n  ☕ 咖啡因禅院 —— 冲泡完成\n")
        print(steam)
        time.sleep(0.4)

def show_caffeine_level(level):
    """显示当前咖啡因等级"""
    level = max(0, min(10, level))
    name, desc = CAFFEINE_LEVELS[level]
    bar_filled = "█" * level + "░" * (10 - level)
    print(f"\n  咖啡因等级: [{bar_filled}] {level}/10")
    print(f"  状态: {name}")
    print(f"  描述: {desc}\n")

def show_quote():
    """显示一条哲学语录"""
    quote = random.choice(COFFEE_PHILOSOPHY)
    print("  " + "─" * 44)
    print("\n  今日禅语:\n")
    slow_print(f"    {quote}", 0.02)
    print()

def show_menu():
    """显示主菜单"""
    print("  ╔══════════════════════════════════════════╗")
    print("  ║          ☕ 咖啡因禅院 ☕               ║")
    print("  ║     — 程序员的量子咖啡机 —              ║")
    print("  ╠══════════════════════════════════════════╣")
    print("  ║  [1] 冲一杯咖啡 (恢复咖啡因值)          ║")
    print("  ║  [2] 查看当前状态                        ║")
    print("  ║  [3] 听一句禅语                          ║")
    print("  ║  [4] 咖啡因过量自检                      ║")
    print("  ║  [5] 离开禅院 (退出)                     ║")
    print("  ╚══════════════════════════════════════════╝")

def overcaffeinated_check():
    """咖啡因过量自检 — 故障艺术"""
    print("\n  ⚠️  咖啡因过量自检系统启动...\n")
    time.sleep(0.5)

    checks = [
        ("检查手指抖动频率", "⚠️  频率 > 120Hz，超出人类极限"),
        ("检查代码中的随机字符", "⚠️  发现 47 处 \`asdkljh\` 类输入"),
        ("检查 git commit 消息", '⚠️  最近 10 条均为 \"aaaaa\"'),
        ("检查显示器距离", "⚠️  你的脸距屏幕 3cm，请后退"),
        ("检查咖啡杯数量", "💀  桌上有 7 个空杯子，你确定还要？"),
        ("检查时间感知", "⚠️  你认为现在是凌晨 3 点，实际是下午 2 点"),
        ("检查键盘温度", "🔥  键盘表面温度已达 47°C"),
    ]

    for check, result in checks:
        time.sleep(0.3)
        print(f"  > {check}...")
        time.sleep(0.4)
        print(f"    {result}\n")

    time.sleep(0.5)
    print("  " + "═" * 44)
    print("\n  诊断结论:")
    print("  你已经超越了「程序员」的范畴，")
    print("  正在向「纯咖啡因实体」进化。")
    print("\n  建议: 去睡觉。说真的。")
    print("  代码明天还在，但你的肝不会等你。")
    print("\n  " + "═" * 44)

def main():
    clear()
    caffeine_level = random.randint(2, 5)  # 今天的初始状态随机

    print("\n  欢迎来到咖啡因禅院。")
    print("  在这里，每一杯咖啡都是一次存在的确认。\n")
    time.sleep(1)

    while True:
        show_menu()
        show_caffeine_level(caffeine_level)

        choice = input("  请选择 (1-5): ").strip()

        if choice == '1':
            brew_coffee()
            caffeine_level = min(10, caffeine_level + random.randint(2, 4))
            clear()
            print("\n  ☕ 冲泡完成！\n")
            show_caffeine_level(caffeine_level)
            show_quote()

        elif choice == '2':
            clear()
            print("\n  ═══ 状态报告 ═══\n")
            show_caffeine_level(caffeine_level)

            # 随机生成一些程序员日常统计
            stats = {
                "今日代码行数": random.randint(10, 500),
                "今日 bug 数": random.randint(0, 42),
                "已修复 bug 数": random.randint(0, 5),
                "TODO 数量": "∞",
                "摸鱼时间占比": f"{random.randint(10, 80)}%",
                "咖啡摄入量": f"{caffeine_level} 杯",
                "Stack Overflow 访问次数": random.randint(3, 99),
            }
            for key, val in stats.items():
                print(f"    {key}: {val}")
            print()

        elif choice == '3':
            clear()
            print()
            show_quote()

        elif choice == '4':
            clear()
            overcaffeinated_check()
            print()

        elif choice == '5':
            clear()
            print("\n  你选择离开禅院。")
            print("  但禅院永远在这里。")
            print("  因为它是一个 Python 脚本。")
            print("  而你随时可以 python coffee_break.py。\n")

            # 最后的禅语
            final_words = [
                "  「记住：最好的代码是你不用写的代码。」",
                "  「记住：人生苦短，用 Python。」",
                "  「记住：今天写不出的 bug，明天依然在等你。」",
                "  「记住：没有咖啡解决不了的问题。如果有，就两杯。」",
                "  「记住：你的代码不定义你，但你的 commit message 定义了你的精神状态。」",
            ]
            print(random.choice(final_words))
            print()
            break

        else:
            print("\n  ❓ 无效选择。咖啡因可能已经影响了你的判断力。\n")

if __name__ == "__main__":
    main()
