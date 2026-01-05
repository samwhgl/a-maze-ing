import random

def generate_maze_skeleton(width: int, height: int)-> list:
    first_line = [-1] * (width * 2 + 1)
    last_line = [-1] * (width * 2 + 1)

    middle_line = [1 if i % 2 == 1 else -1 for i in range(width * 2 + 1)]

    maze = []
    maze.append(first_line)

    for i in range(height * 2 - 1):
        if i % 2 == 0:
            maze.append(middle_line.copy())
        else:
            maze.append(first_line.copy())

    maze.append(last_line)
    nbr = 1
    for i in range(height * 2 + 1):
        for j in range(width * 2 + 1):
            if maze[i][j] == 1:
                nbr += 1
                maze[i][j] = nbr

    # for row in maze:
    #     print(row)
    return maze

def is_maze_finished(maze: list)-> bool:
    indicator = maze[1][1]
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] not in [-1, 0, indicator]:
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

        v_haut = maze[chosen_i - 1][chosen_j]
        v_bas = maze[chosen_i + 1][chosen_j]

        if v_haut > 0 and v_bas > 0 and v_haut != v_bas:
            maze[chosen_i][chosen_j] = 0
            for r in range(len(maze)):
                for c in range(len(maze[0])):
                    if maze[r][c] == v_bas:
                        maze[r][c] = v_haut

        v_gauche = maze[chosen_i][chosen_j - 1]
        v_droite = maze[chosen_i][chosen_j + 1]

        if v_gauche > 0 and v_droite > 0 and v_gauche != v_droite:
            maze[chosen_i][chosen_j] = 0
            for r in range(len(maze)):
                for c in range(len(maze[0])):
                    if maze[r][c] == v_droite:
                        maze[r][c] = v_gauche

        candidates.remove((chosen_i, chosen_j))

    # for row in maze:
    #     print(row)
    return maze

def close_cells(maze: list, cell_number: tuple)-> list:
    i, j = cell_number
    maze[i-1][j] = -1
    maze[i+1][j] = -1
    maze[i-1][j-1] = -1
    maze[i-1][j+1] = -1
    maze[i][j] = -2
    return maze

def add_42_pattern(maze: list)-> list:
    height = len(maze) // 2
    width = len(maze[0])// 2
    if height % 2 == 1:
        x = len(maze) // 2
    if height % 2 == 0:
        x = len(maze) // 2 + 1
    if width % 2 == 1:
        y = len(maze[0]) // 2
    if width % 2 == 0:
        y = len(maze[0]) // 2 + 1
    close_cells(maze, (x, y - 2))
    close_cells(maze, (x, y - 4))
    close_cells(maze, (x, y - 6))
    close_cells(maze, (x - 2, y - 6))
    close_cells(maze, (x - 4, y - 6))
    close_cells(maze, (x + 2, y - 2))
    close_cells(maze, (x + 4, y - 2))
    close_cells(maze, (x + 4, y + 2))
    close_cells(maze, (x + 2, y + 2))
    close_cells(maze, (x , y + 2))
    close_cells(maze, (x + 4, y + 4))
    close_cells(maze, (x + 4, y + 6))
    close_cells(maze, (x , y + 4))
    close_cells(maze, (x, y + 6))
    close_cells(maze, (x - 2, y + 6))
    close_cells(maze, (x - 4, y + 6))
    close_cells(maze, (x - 4, y + 4))
    close_cells(maze, (x - 4, y + 2))


    return maze




def print_maze_pretty(maze: list):
    # Couleurs et symboles
    # \033[38;5;237m = Gris foncé (murs)
    # \033[0m = Reset couleur
    WALL = "\033[38;5;237m██\033[0m"
    PATH = "  "
    SIGN = "\033[1;31m██\033[0m"

    for row in maze:
        line = ""
        for cell in row:
            if cell == -1:
                line += WALL
            elif cell == -2:
                line += SIGN
            else:
                line += PATH
        print(line)


def find_shortest_path(maze: list, start: tuple, end: tuple)-> list:
    j, i = start
    j_finish, i_finish = end
    j = j * 2 + 1
    i = i * 2 + 1
    j_finish = j_finish * 2 + 1
    i_finish = i_finish * 2 + 1
    finished = False
    count = -4
    maze[i][j] = -3
    while not finished:
        v_haut = maze[i - 1][j]
        v_bas = maze[i + 1][j]
        v_gauche = maze[i][j - 1]
        v_droite = maze[i][j + 1]
        if v_haut == 0:
            maze[i - 2][j] = count
        if v_bas == 0:
            maze[i + 2][j] = count
        if v_gauche == 0:
            maze[i][j - 2] = count
        if v_droite == 0:
            maze[i][j + 2] = count
        count -= 1
        if maze[i_finish][j_finish] == count:
            finished = True





maze = generate_maze_skeleton(18, 19)
maze_42 = add_42_pattern(maze)
maze_finished = generate_maze(maze)
print_maze_pretty(maze)


