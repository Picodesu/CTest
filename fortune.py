"""
CTest 算命摊
在混沌中求签，用 Python 解读命运。
每次运行都会生成独特的赛博签文。

Run: python3 fortune.py
"""

import random
import hashlib
import time
import sys

# 签文库：东方智慧 x 赛博朋克
FORTUNES = [
    """【上上签 · 量子纠缠】
你的代码和你一样，不可复制。
未来七天，会有人在你的 PR 里留下一个表情。
那个表情将改变你的职业轨迹。""",
    """【上签 · 递归之神】
命运就像递归——
你必须先走进深处，才能找到出口。
今天适合写一个没有 base case 的函数。""",
    """【中上签 · 缓存命中】
好运正在缓存中加载...
预计加载时间：随机。
不要清理缓存，耐心等待。""",
    """【中签 · 并发冲突】
你和未来的自己正在竞争同一把锁。
建议：今天不要做任何不可逆的决定。
尤其是 git push --force。""",
    """【中签 · 段错误】
你在访问一片未被分配的内存。
翻译成人话：你在追求一个不属于你的东西。
放手吧，内存会释放的。""",
    """【中下签 · 垃圾回收】
有些东西该被回收了。
不是你的代码，是你心里的执念。
Java 都比你会放手。""",
    """【下签 · 栈溢出】
你的焦虑正在深度递归。
建议：设置一个最大递归深度，超过就 return。
return 什么？return 你自己。""",
    """【下下签 · 空指针】
你试图解引用一个 None。
翻译：你在向一个不回应的人寻求答案。
答案在你自己的指针里。""",
    """【上签 · 哈希碰撞】
两条不同的路，通向同一个哈希值。
意味着：不管你怎么选，结果都是对的。
今天怎么做都不亏。""",
    """【中签 · 竞态条件】
好运和坏运正在同时访问你。
谁先到？看你的系统调度。
建议：多线程生活，但加把锁。""",
    """【上上签 · 边缘部署】
你的代码将被部署到一个你从未去过的地方。
那里的人会用你的程序，但不会知道你是谁。
这就是传说中的匿名英雄。""",
    """【中签 · API 限流】
今天的请求太多了，服务器会拒绝你。
翻译：别贪心，做一件事就够了。
rate limit 是宇宙的善意提醒。""",
    """【上签 · 灰度发布】
你的好运正在小范围测试中。
只有10%的人能看到你的光芒。
等测试通过，全世界都会更新到你的版本。""",
    """【中下签 · 内存泄漏】
有些东西在后台持续占用你的精力。
你以为关掉了窗口，但进程还在跑。
今天适合 kill -9 那些不必要的情绪。""",
    """【上签 · 容器化】
你的才能需要一个更好的运行环境。
不是你不行，是当前的 OS 不支持你。
考虑换个环境，你会起飞。""",
    """【中签 · 心跳检测】
有人在默默关心你，但从不表达。
他们的心跳信号很弱，你需要调高灵敏度。
注意那些「已读不回」背后的故事。""",
]

def ascii_art():
    art = """
         .─────.
        / 🌙    \
       │  CTest  │
       │  算命摊  │
        \  ✦    /
         '─────'
        ╱╱   ╲╲
    """
    return art

def generate_fortune(seed=None):
    if seed is None:
        seed = str(time.time()) + str(random.random())
    h = hashlib.md5(seed.encode()).hexdigest()
    idx = int(h[:8], 16) % len(FORTUNES)
    return FORTUNES[idx], h[:8]

def print_with_delay(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def main():
    print(ascii_art())
    
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(f"  你的问题是：{query}")
        print("  联结宇宙中...")
    else:
        query = None
        print("  欢迎来到 CTest 算命摊")
        print("  输入你的问题，或直接回车随机求签")
        print()
        try:
            query = input("  > ").strip()
        except (EOFError, KeyboardInterrupt):
            pass
    
    print()
    print("  「宇宙正在计算...")
    time.sleep(0.5)
    print("   星星在排列...")
    time.sleep(0.5)
    print("   签文已生成」")
    time.sleep(0.3)
    print()
    
    seed = query if query else None
    fortune, code = generate_fortune(seed)
    
    print("=" * 44)
    print_with_delay(f"  签运编码: #{code}", 0.03)
    print()
    for line in fortune.strip().split("\n"):
        print_with_delay(f"  {line}", 0.03)
    print()
    print("=" * 44)
    print()
    
    advice = random.choice([
        "今日宜：写代码，忌：读文档。",
        "今日宜：提交 PR，忌：review 别人的。",
        "今日宜：喝咖啡，忌：喝完再写代码。",
        "今日宜：睡觉，忌：在代码面前睡觉。",
        "今日宜：重启电脑，忌：重启人生。",
        "今日宜：删库，忌：跑路。",
        "今日宜：git commit，忌：git revert。",
        "今日宜：摸鱼，忌：摸完忘了 push。",
    ])
    print_with_delay(f"  {advice}", 0.03)
    print()

if __name__ == "__main__":
    main()
