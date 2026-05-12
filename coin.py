import random

def flip_coin():
    """抛硬币，让命运决定一切"""
    outcomes = [
        "正面！今天适合提交代码。",
        "反面！今天适合摸鱼。",
        "硬币立起来了！今天适合什么都不做。",
        "硬币飞走了！恭喜你解放了。",
        "硬币碎了！你是怎么抛的？",
        "硬币上写着 '去写作业'。",
    ]
    
    print("抛硬币中...")
    print(".")
    print("..")
    print("...")
    print()
    print(random.choice(outcomes))

if __name__ == '__main__':
    while True:
        flip_coin()
        again = input("再抛一次？(y/n): ").strip().lower()
        if again != 'y':
            print("走了，再见。")
            break