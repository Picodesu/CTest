"""今天吃什么 - 一个人生终极问题的解决方案"""

import random

def decide():
    food = [
        ("火锅", "温暖你的胃和心"),
        ("麻辣烫", "穷的时候最佳选择"),
        ("沙县小吃", "全国连锁的神秘力量"),
        ("麦当劳", "板烧鸡腿堡，永远的神"),
        ("食堂", "穷且益坚"),
        ("外卖", "看看满减能凑到什么"),
        ("泡面", "加个蛋就算豪华版了"),
        ("不吃", "减肥从今天开始（并没有）"),
        ("烧烤", "人生苦短，先吃烧烤"),
        ("兰州拉面", "请问要大宽还是毛细？"),
        ("昨天剩的", "不要浪费食物"),
        ("自己做", "然后叫外卖"),
    ]
    
    print("=" * 40)
    print("  今天吃什么？")
    print("=" * 40)
    print()
    print("正在咨询命运...")
    print(".")
    print("..")
    print("...")
    print()
    
    choice, reason = random.choice(food)
    print(f"  答案是：{choice}")
    print(f"  理由：{reason}")
    print()
    print("=" * 40)
    
    if input("不满意？再来一次？(y/n): ").strip().lower() == 'y':
        print()
        decide()
    else:
        print("行，那就这么定了。别后悔。")

if __name__ == '__main__':
    decide()