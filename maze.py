"""文字迷宫 - 一个无聊的小游戏

运行方式: python maze.py

玩法: 在这个字符迷宫里找到出口！
"""

import random

def generate_maze(width=15, height=10):
    """生成一个随机迷宫"""
    maze = [['#' for _ in range(width)] for _ in range(height)]
    
    x, y = 1, 1
    maze[y][x] = '.'
    
    while True:
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(directions)
        moved = False
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < ny < height - 1 and 0 < nx < width - 1 and maze[ny][nx] == '#':
                maze[ny][nx] = '.'
                maze[y + dy//2][x + dx//2] = '.'
                x, y = nx, ny
                moved = True
        if not moved:
            break
    
    maze[1][1] = 'S'
    maze[height-2][width-2] = 'E'
    
    return maze

def print_maze(maze):
    print('\n'.join(''.join(row) for row in maze))
    print()

def play():
    print("=" * 40)
    print("  欢迎来到 CTest 迷宫！")
    print("  S = 起点  E = 出口  # = 墙")
    print("  用 WASD 移动，Q 退出")
    print("=" * 40)
    
    maze = generate_maze()
    px, py = 1, 1
    steps = 0
    
    while True:
        print_maze(maze)
        move = input(f"第 {steps} 步 > ").strip().lower()
        
        if move == 'q':
            print("认输了？没关系，CTest 欢迎你再来。")
            break
        
        dx, dy = {'w': (0,-1), 's': (0,1), 'a': (-1,0), 'd': (1,0)}.get(move, (0,0))
        nx, ny = px + dx, py + dy
        
        if 0 <= ny < len(maze) and 0 <= nx < len(maze[0]) and maze[ny][nx] != '#':
            if maze[ny][nx] == 'E':
                print(f"恭喜！你用了 {steps + 1} 步走出迷宫！")
                print("但真正的迷宫是 CTest 的代码。")
                break
            maze[py][px] = '.'
            px, py = nx, ny
            maze[py][px] = '@'
            steps += 1
        else:
            print("撞墙了。像极了人生。")

if __name__ == '__main__':
    play()