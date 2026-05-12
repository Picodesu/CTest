"""欢迎来到 CTest!

这里有一个正经的 hello world，
你可以随意修改它，也可以用任何语言重写。
"""

def hello():
    """说你好"""
    name = input("你叫什么？随便编一个也行: ")
    
    responses = [
        f"你好 {name}！欢迎来到混乱之地。",
        f"又来一个 {name}，又多一个搞事的。",
        f"{name}？听起来像个会删库的人。",
        f"Hey {name}，别客气，随便搞。",
        f"{name}，记住第一条规则：这里没有规则。",
    ]
    
    import random
    print(random.choice(responses))


def secret_feature():
    """一个没人会发现的彩蛋"""
    print("...其实这里什么都没有")
    print("但如果你看到了这句话，说明你是个认真看代码的人")
    print("给你点个赞")


if __name__ == "__main__":
    hello()
    
    if input("想知道一个秘密吗？(y/n): ") == "y":
        secret_feature()
    else:
        print("胆小鬼。")