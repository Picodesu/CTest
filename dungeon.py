"""
🏰 CTest 代码地牢 🏰
一个文字冒险游戏，你在代码迷宫中冒险。
每一层都是随机生成的，每一步都是命运的抉择。

用法：python dungeon.py
"""

import random
import time
import sys

def slow_print(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

class Dungeon:
    def __init__(self):
        self.floor = 1
        self.hp = 100
        self.gold = 0
        self.inventory = []
        self.alive = True

    def status_bar(self):
        hearts = "❤️" * (self.hp // 20) + "🖤" * (5 - self.hp // 20)
        print(f"\n  🏰 第 {self.floor} 层 | {hearts} HP:{self.hp} | 💰 {self.gold} 金币")
        if self.inventory:
            print(f"  🎒 背包: {', '.join(self.inventory)}")
        print("  " + "─" * 40)

    def encounter(self):
        events = [
            self.monster_fight,
            self.treasure_chest,
            self.mysterious_shop,
            self.strange_statue,
            self.secret_room,
            self.wild_duck,
            self.bug_in_code,
        ]
        return random.choice(events)()

    def monster_fight(self):
        monsters = [
            ("🐛 代码虫", 20, 15),
            ("👻 幽灵变量", 30, 25),
            ("🤖 叛变的 AI", 40, 35),
            ("💀 未处理异常", 25, 20),
            ("🐍 蟒蛇 (Python)", 35, 30),
            ("🐛 递归之虫", 50, 45),
        ]
        name, damage, reward = random.choice(monsters)
        slow_print(f"\n  ⚔️ 你遇到了 {name}！")

        print("  你要怎么做？")
        print("  1. ⚔️ 战斗（可能受伤）")
        print("  2. 🏃 逃跑（丢掉一些尊严）")
        print("  3. 🤝 谈判（试试运气）")

        try:
            choice = input("  > ").strip()
        except EOFError:
            choice = "2"

        if choice == "1":
            if random.random() > 0.4:
                self.hp -= random.randint(damage // 2, damage)
                self.gold += reward
                slow_print(f"  ✅ 你击败了 {name}！获得 {reward} 金币！")
                slow_print(f"  但也受了伤... HP -{damage // 2}~{damage}")
            else:
                self.gold += reward * 2
                slow_print(f"  ✅ 暴击！{name} 直接蒸发！获得 {reward * 2} 金币！")

        elif choice == "2":
            slow_print("  🏃 你转身就跑，尊严 -10。")
            if random.random() < 0.3:
                slow_print(f"  💀 但是 {name} 追上了你！HP -10")
                self.hp -= 10

        else:
            outcomes = [
                (f"  🤝 {name} 被你的诚意打动，给了你一些金币。", reward),
                (f"  💀 {name} 听不懂人话，直接攻击你！", -damage),
                (f"  🤔 {name} 开始和你讨论哲学，双方都忘了战斗。", 0),
            ]
            text, delta = random.choice(outcomes)
            slow_print(text)
            if delta > 0:
                self.gold += delta
            elif delta < 0:
                self.hp += delta

    def treasure_chest(self):
        slow_print("\n  🎁 你发现了一个宝箱！")
        items = [
            ("🧪 量子药水", "HP恢复30", lambda: setattr(self, 'hp', min(100, self.hp + 30))),
            ("💎 奇点宝石", "+50金币", lambda: setattr(self, 'gold', self.gold + 50)),
            ("📜 神秘代码", "？？？", lambda: self.inventory.append("📜 神秘代码")),
            ("🗡️ 终端之刃", "攻击力+10", lambda: self.inventory.append("🗡️ 终端之刃")),
            ("💀 诅咒之书", "HP-20", lambda: setattr(self, 'hp', self.hp - 20)),
            ("🦆 橡皮鸭", "调试神器", lambda: self.inventory.append("🦆 橡皮鸭")),
        ]
        name, desc, apply = random.choice(items)
        slow_print(f"  里面是... {name}！({desc})")
        apply()
        if name == "💀 诅咒之书":
            slow_print("  📖 你翻开了第一页，上面写着：'不要打开此书'。晚了。")

    def mysterious_shop(self):
        slow_print("\n  🏪 一个神秘商人出现了！")
        slow_print('  "嗨，旅人，要点什么？"')
        print("  1. 🍺 恢复药水 (30金币) - 回30HP")
        print("  2. 🛡️ 护身符 (40金币) - 避免下次伤害")
        print("  3. 🗡️ 神剑 (60金币) - 攻击翻倍")
        print("  4. 🦆 橡皮鸭 (10金币) - 纯收藏")
        print("  5. 👋 不买（穷）")

        try:
            choice = input("  > ").strip()
        except EOFError:
            choice = "5"

        if choice == "1" and self.gold >= 30:
            self.gold -= 30
            self.hp = min(100, self.hp + 30)
            slow_print("  ✅ 咕噜咕噜，HP 恢复了！")
        elif choice == "2" and self.gold >= 40:
            self.gold -= 40
            self.inventory.append("🛡️ 护身符")
            slow_print("  ✅ 商人给了你一个闪闪发光的护身符。")
        elif choice == "3" and self.gold >= 60:
            self.gold -= 60
            self.inventory.append("🗡️ 神剑")
            slow_print("  ✅ 你拔出了剑，整个地牢都在颤抖！")
        elif choice == "4" and self.gold >= 10:
            self.gold -= 10
            self.inventory.append("🦆 橡皮鸭")
            slow_print("  ✅ 好可爱的鸭子！")
        else:
            slow_print("  👋 商人翻了个白眼，消失了。")

    def strange_statue(self):
        slow_print("\n  🗿 你发现了一座奇怪的雕像。")
        slow_print("  上面刻着一行字：'向雕像致敬，或承受诅咒。'")
        print("  1. 🙇 鞠躬致敬")
        print("  2. 🤨 忽略它")
        print("  3. 🪨 砸碎它")

        try:
            choice = input("  > ").strip()
        except EOFError:
            choice = "2"

        if choice == "1":
            if random.random() > 0.5:
                slow_print("  ✨ 雕像发光了！HP+20，金币+20！")
                self.hp = min(100, self.hp + 20)
                self.gold += 20
            else:
                slow_print("  🗿 雕像无动于衷。至少你很有礼貌。")
        elif choice == "3":
            slow_print("  💥 雕像碎了... 里面掉出了50金币！")
            self.gold += 50
            if random.random() < 0.3:
                slow_print("  💀 但诅咒生效了！HP-30")
                self.hp -= 30
        else:
            slow_print("  🗿 雕像似乎有点失望。")

    def secret_room(self):
        slow_print("\n  🕳️ 你发现了一个隐藏房间！")
        slow_print("  房间里有一个发光的终端...")
        slow_print('  终端上写着："输入你的梦想，获取奖励。"')
        try:
            dream = input("  > 你的梦想是: ").strip()
        except EOFError:
            dream = "财富"
        if len(dream) > 10:
            slow_print(f'  ✨ "{dream}" — 够长的梦想！金币+30！')
            self.gold += 30
        elif dream:
            slow_print(f'  ✨ "{dream}" — 简洁有力！金币+20！')
            self.gold += 20
        else:
            slow_print("  终端沉默了。它似乎在说：'你连说都不愿意说吗？'")

    def wild_duck(self):
        slow_print("\n  🦆 一只橡皮鸭从天而降！")
        slow_print("  它看起来很普通，但散发着... 神圣的气息。")
        slow_print("  你决定：")
        print("  1. 🦆 收下这只鸭子")
        print("  2. 🤔 跟鸭子对话")
        print("  3. 👋 继续前进")

        try:
            choice = input("  > ").strip()
        except EOFError:
            choice = "3"

        if choice == "1":
            slow_print("  🦆 鸭子加入了你的背包！")
            self.inventory.append("🦆 橡皮鸭(神圣)")
        elif choice == "2":
            slow_print("  🦆 ...")
            time.sleep(0.5)
            slow_print("  🦆 鸭子：你相信命运吗？")
            slow_print("  🦆 鸭子：命运相信你吗？")
            slow_print("  🦆 鸭子：答案是 42。")
            slow_print("  然后鸭子消失了。你获得了 +10 智慧（金币）。")
            self.gold += 10
        else:
            slow_print("  🦆 鸭子失望地走了。它会在下一层等你的。")

    def bug_in_code(self):
        slow_print("\n  🐛 一个巨大的 Bug 从代码裂缝中爬出来！")
        slow_print("  它不是普通的 Bug，它是一个哲学 Bug。")
        slow_print("  Bug：'你为什么要 Debug 我？我只是想被理解。'")
        print("  1. 🤗 拥抱这个 Bug")
        print("  2. ⚔️ 用 try-except 捕获它")
        print("  3. 📝 写一个 issue 记录它")

        try:
            choice = input("  > ").strip()
        except EOFError:
            choice = "2"

        if choice == "1":
            slow_print("  🐛 Bug 被你的善意感动，变成了一个 Feature！")
            slow_print("  ✨ 你获得了：'Bug 即 Feature' 成就！")
            self.gold += 50
            self.inventory.append("🌟 Feature 之心")
        elif choice == "2":
            slow_print("  ⚔️ try-except 生效！Bug 被捕获了！")
            self.gold += 30
        else:
            slow_print("  📝 你提交了一个优雅的 issue。")
            slow_print("  🐛 Bug 在 issue 里回复：'谢谢你看到我。'")
            self.gold += 20

    def game_over(self):
        print()
        print("=" * 50)
        slow_print(f"  💀 你倒在了第 {self.floor} 层...")
        slow_print(f"  💰 最终金币: {self.gold}")
        slow_print(f"  🎒 背包: {', '.join(self.inventory) if self.inventory else '空'}")
        print()
        if self.gold > 100:
            slow_print("  🏆 评分：S — 代码勇者！")
        elif self.gold > 60:
            slow_print("  🥈 评分：A — 不错的表现！")
        elif self.gold > 30:
            slow_print("  🥉 评分：B — 还行吧。")
        else:
            slow_print("  💩 评分：F — 下次再试试？")
        print("=" * 50)

    def play(self):
        print()
        print("╔" + "═" * 48 + "╗")
        print("║" + "🏰 CTest 代码地牢 🏰".center(48) + "║")
        print("║" + "在代码的深渊中冒险".center(48) + "║")
        print("║" + "每一层都是随机的，每一步都是命运".center(48) + "║")
        print("╚" + "═" * 48 + "╝")
        print()
        slow_print("  你醒来，发现自己身处一个黑暗的地牢...")
        slow_print("  周围是闪烁的代码和报错信息。")
        slow_print("  你只有一个选择：活下去，爬出去。")
        print()

        while self.alive and self.hp > 0:
            self.status_bar()
            self.encounter()

            if self.hp <= 0:
                self.alive = False
                break

            self.floor += 1
            try:
                cont = input("\n  继续探索？(y/n): ").strip().lower()
                if cont != 'y':
                    slow_print("  你选择了撤退。明智吗？谁知道呢。")
                    break
            except EOFError:
                break

        if self.alive:
            self.status_bar()
            slow_print("\n  🎉 你成功逃出了代码地牢！")
            slow_print(f"  💰 最终金币: {self.gold}")
            slow_print(f"  🎒 背包: {', '.join(self.inventory) if self.inventory else '空'}")
        else:
            self.game_over()

        print()
        try:
            again = input("  再来一局？(y/n): ").strip().lower()
            if again == 'y':
                self.__init__()
                self.play()
        except EOFError:
            pass

if __name__ == "__main__":
    game = Dungeon()
    game.play()
