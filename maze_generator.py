import random
import os



def generate_maze_skeleton(width: int, height: int)-> list:
    first_line = [-1] * (width * 2 + 1)
    maze = [first_line.copy()]
    middle_line = [1 if i % 2 == 1 else -1 for i in range(width * 2 + 1)]

    for i in range(height * 2 - 1):
        maze.append(middle_line.copy() if i % 2 == 0 else first_line.copy())

    maze.append(first_line.copy())

    nbr = 1
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 1:
                nbr += 1
                maze[i][j] = nbr
    return maze

def is_maze_finished(maze: list)-> bool:
    indicator = maze[1][1]
    for row in maze:
        for cell in row:
            if cell > 0 and cell != indicator:
                return False
    return True

def generate_maze(maze: list):
    candidates = []
    for i in range(1, len(maze) - 1):
        for j in range(1, len(maze[0]) - 1):
            if maze[i][j] == -1:
                candidates.append((i, j))

    while candidates and not is_maze_finished(maze):
        chosen_i, chosen_j = random.choice(candidates)
        v_haut, v_bas = maze[chosen_i - 1][chosen_j], maze[chosen_i + 1][chosen_j]
        if v_haut > 0 and v_bas > 0 and v_haut != v_bas:
            maze[chosen_i][chosen_j] = 0
            for r in range(len(maze)):
                for c in range(len(maze[0])):
                    if maze[r][c] == v_bas: maze[r][c] = v_haut

        v_gauche, v_droite = maze[chosen_i][chosen_j - 1], maze[chosen_i][chosen_j + 1]
        if v_gauche > 0 and v_droite > 0 and v_gauche != v_droite:
            maze[chosen_i][chosen_j] = 0
            for r in range(len(maze)):
                for c in range(len(maze[0])):
                    if maze[r][c] == v_droite: maze[r][c] = v_gauche

        candidates.remove((chosen_i, chosen_j))
    return maze

def close_cells(maze: list, cell_number: tuple)-> list:
    i, j = cell_number
    for r in range(i-1, i+2):
        for c in range(j-1, j+2):
            if 0 <= r < len(maze) and 0 <= c < len(maze[0]):
                maze[r][c] = -1
    maze[i][j] = -2
    return maze

def add_42_pattern(maze: list)-> list:
    x, y = len(maze) // 2, len(maze[0]) // 2
    if x % 2 == 0: x += 1
    if y % 2 == 0: y += 1
    offsets = [(0,-2), (0,-4), (0,-6), (-2,-6), (-4,-6), (2,-2), (4,-2), (4,2), (2,2), (0,2), (4,4), (4,6), (0,4), (0,6), (-2,6), (-4,6), (-4,4), (-4,2)]
    for ox, oy in offsets:
        close_cells(maze, (x + ox, y + oy))
    return maze

THEMES = [
    {
        "wall": "\033[38;5;237m██\033[0m",
        "sign": "\033[1;31m██\033[0m",
        "start": "\033[1;36m██\033[0m",
        "end": "\033[1;33m██\033[0m",
        "path": "\033[1;32m██\033[0m"
    },
    {
        "wall": "\033[38;5;234m██\033[0m",
        "sign": "\033[38;5;198m██\033[0m",
        "start": "\033[38;5;45m██\033[0m",
        "end": "\033[38;5;214m██\033[0m",
        "path": "\033[38;5;118m██\033[0m"
    },
    {
        "wall": "\033[38;5;94m██\033[0m",
        "sign": "\033[38;5;124m██\033[0m",
        "start": "\033[38;5;193m██\033[0m",
        "end": "\033[38;5;220m██\033[0m",
        "path": "\033[38;5;28m██\033[0m"
    }
]


def print_maze(maze: list, theme: dict, show_path: bool):
    EMPTY = "  "
    for row in maze:
        line = ""
        for cell in row:
            if cell == -1: line += theme["wall"]
            elif cell == -2: line += theme["sign"]
            elif cell == -3: line += theme["start"]
            elif cell == -4: line += theme["end"]
            elif cell == -5: line += theme["path"] if show_path else EMPTY
            else: line += EMPTY
        print(line)

def find_shortest_path(maze: list, start: tuple, end: tuple)-> list:
    sc, sl = start
    ec, el = end
    i, j = sl * 2 + 1, sc * 2 + 1
    fi, fj = el * 2 + 1, ec * 2 + 1

    finished, count = False, -10
    maze[i][j], following_cell = -9, [(i, j)]

    while not finished and following_cell:
        next_cells = []
        for ci, cj in following_cell:
            for diw, djw, dic, djc in [(-1,0,-2,0), (1,0,2,0), (0,-1,0,-2), (0,1,0,2)]:
                wi, wj, ni, nj = ci+diw, cj+djw, ci+dic, cj+djc
                if 0 <= ni < len(maze) and 0 <= nj < len(maze[0]):
                    if maze[wi][wj] == 0 and maze[ni][nj] > 0:
                        maze[ni][nj] = count
                        next_cells.append((ni, nj))
                        if ni == fi and nj == fj: finished = True
        following_cell, count = next_cells, count - 1

    if finished:
        ci, cj = fi, fj
        while maze[ci][cj] != -9:
            val = maze[ci][cj]
            for diw, djw, dic, djc in [(-1,0,-2,0), (1,0,2,0), (0,-1,0,-2), (0,1,0,2)]:
                wi, wj, ni, nj = ci+diw, cj+djw, ci+dic, cj+djc
                if 0 <= ni < len(maze) and 0 <= nj < len(maze[0]):
                    if (maze[ni][nj] == val + 1 or maze[ni][nj] == -9) and maze[wi][wj] == 0:
                        maze[ci][cj] = -5
                        maze[wi][wj] = -5
                        ci, cj = ni, nj
                        break
        maze[i][j], maze[fi][fj] = -3, -4
    return maze


if __name__ == "__main__":
    dim = 15
    maze = generate_maze_skeleton(dim, dim)
    add_42_pattern(maze)
    generate_maze(maze)
    find_shortest_path(maze, (0, 0), (14, 14))

    user_choice = 0
    show_path = True
    current_theme_idx = 0

    while user_choice != 4:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_maze(maze, THEMES[current_theme_idx], show_path)

        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path")
        print("3. Rotate maze colors")
        print("4. Quit")

        try:
            user_choice = int(input("Choice? (1-4): "))
        except ValueError:
            user_choice = 0

        if user_choice == 1:
            maze = generate_maze_skeleton(dim, dim)
            add_42_pattern(maze)
            generate_maze(maze)
            find_shortest_path(maze, (0, 0), (dim-1, dim-1))
        elif user_choice == 2:
            show_path = not show_path
        elif user_choice == 3:
            current_theme_idx = (current_theme_idx + 1) % 3
        elif user_choice == 4:
            quit()
