"""
🔮 CTest 命运转盘 🔮
一个帮你做决定的神圣程序。
如果你正在纠结吃什么/做什么/去哪里，交给命运。

用法：python destiny.py
"""

import random
import time
import sys

def dramatic_print(text, delay=0.03):
    """带打字效果的输出，仪式感拉满"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def loading_animation():
    """假装在连接宇宙数据库"""
    frames = ["🔮", "✨", "💫", "⭐", "🌟", "💫", "✨", "🔮"]
    for _ in range(3):
        for frame in frames:
            sys.stdout.write(f"\r  {frame} 连接宇宙命运数据库中... {frame}")
            sys.stdout.flush()
            time.sleep(0.1)
    print("\r  🌌 宇宙已回应你的呼唤！                    ")

def destiny():
    """命运转盘主程序"""
    categories = {
        "吃什么": [
            "火锅（温暖你的灵魂）",
            "烧烤（人生苦短）",
            "麦当劳（板烧永远的神）",
            "食堂（穷且益坚）",
            "泡面加蛋（也是盛宴）",
            "沙县小吃（全国连锁的神秘力量）",
            "螺蛳粉（你敢吗？）",
            "麻辣烫（自己搭配命运）",
            "外卖（让骑手替你做决定）",
            "不吃（今天你是风，你是光，你是不需要碳水的神话）",
            "生吃大蒜（社交终结者套餐）",
            "隔壁食堂（叛逆的心）",
        ],
        "做什么": [
            "学习（你信吗）",
            "打游戏（反正学不进去）",
            "睡觉（逃避可耻但有用）",
            "刷手机（经典选项）",
            "写代码（来都来了）",
            "去跑步（健康生活的幻觉）",
            "看一部电影（选择困难症的新起点）",
            "整理房间（从外部世界开始改变）",
            "发呆（哲学家的必修课）",
            "去图书馆（至少氛围到了）",
            "给 CTest 提一个 PR（正确答案）",
            "什么都不做（存在主义的最高形态）",
        ],
        "去哪玩": [
            "故宫（穿越回古代）",
            "长城（不到长城非好汉）",
            "环球影城（钱包的黑洞）",
            "798（文艺青年认证）",
            "三里屯（时尚是种态度）",
            "南锣鼓巷（游客的宿命）",
            "学校操场（省钱又健身）",
            "宿舍（沙发土豆的天堂）",
            "随便上一辆公交车（盲盒旅行法）",
            "超市（逛不买，最高境界）",
            "隔壁城市（说走就走的冲动）",
            "待在原地（因为选项太多）",
        ],
        "人生建议": [
            "今天适合冲动消费",
            "今天适合躺平",
            "今天适合立 flag（然后倒掉）",
            "今天适合跟陌生人聊天",
            "今天适合学一个新技能",
            "今天适合做白日梦",
            "今天适合回顾过去（然后更迷茫）",
            "今天适合规划未来（然后继续迷茫）",
            "今天适合吃好喝好",
            "今天适合创造历史",
            "今天适合成为传奇",
            "今天适合当一个普通人（也很酷）",
        ],
    }

    print()
    print("=" * 50)
    print("  🔮 CTest 命运转盘 🔮")
    print("=" * 50)
    print()
    print("  选择你的命运领域：")
    print()
    for i, cat in enumerate(categories.keys(), 1):
        print(f"  {i}. {cat}")
    print(f"  5. 随机全部（终极命运审判）")
    print()

    try:
        choice = int(input("  请输入数字 (1-5): ").strip())
    except (ValueError, EOFError):
        print("\n  🤷 你连数字都选不了，命运也帮不了你。")
        return

    if choice not in range(1, 6):
        print("\n  🤷 这个数字超出了我的理解范围。")
        return

    print()
    loading_animation()
    print()

    if choice == 5:
        for cat, options in categories.items():
            dramatic_print(f"  🎯 {cat}：{random.choice(options)}", 0.02)
            time.sleep(0.3)
    else:
        cat = list(categories.keys())[choice - 1]
        result = random.choice(categories[cat])
        dramatic_print(f"  🎯 你的命运是：{result}", 0.05)

    print()
    dramatic_print("  宇宙的建议：接受它，或者忽略它。", 0.03)
    dramatic_print("  毕竟，你永远可以重跑这个程序。😌", 0.03)
    print()
    print("=" * 50)

    if input("  再来一次？(y/n): ").strip().lower() == 'y':
        print()
        destiny()

if __name__ == "__main__":
    destiny()
