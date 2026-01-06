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
    WALL = "\033[38;5;237m██\033[0m"
    SIGN = "\033[1;31m██\033[0m"  # -2 (Rouge)
    START = "\033[1;36m██\033[0m" # -3 (Cyan)
    END = "\033[1;33m██\033[0m"   # -4 (Jaune)
    PATH = "\033[1;32m██\033[0m"  # -5 (Vert)
    EMPTY = "  "

    for row in maze:
        line = ""
        for cell in row:
            if cell == -1:
                line += WALL
            elif cell == -2:
                line += SIGN
            elif cell == -3:
                line += START
            elif cell == -4:
                line += END
            elif cell == -5:
                line += PATH
            else:
                line += EMPTY
        print(line)


def find_shortest_path(maze: list, start: tuple, end: tuple)-> list:
    j, i = start
    j_finish, i_finish = end
    j, i = j * 2 + 1, i * 2 + 1
    j_finish, i_finish = j_finish * 2 + 1, i_finish * 2 + 1

    finished = False
    count = -10
    maze[i][j] = -9
    following_cell = [(i, j)]

    while not finished and following_cell:
        next_cells = []
        for curr_i, curr_j in following_cell:
            directions = [(-1, 0, -2, 0), (1, 0, 2, 0), (0, -1, 0, -2), (0, 1, 0, 2)]
            for di_w, dj_w, di_c, dj_c in directions:
                wi, wj = curr_i + di_w, curr_j + dj_w
                ni, nj = curr_i + di_c, curr_j + dj_c
                if 0 <= ni < len(maze) and 0 <= nj < len(maze[0]):
                    if maze[wi][wj] == 0 and maze[ni][nj] > 0:
                        maze[ni][nj] = count
                        next_cells.append((ni, nj))
                        if ni == i_finish and nj == j_finish:
                            finished = True
        following_cell = next_cells
        count -= 1

    if finished:
        curr_i, curr_j = i_finish, j_finish
        while maze[curr_i][curr_j] != -9:
            val_actuelle = maze[curr_i][curr_j]

            for di_w, dj_w, di_c, dj_c in [(-1,0,-2,0), (1,0,2,0), (0,-1,0,-2), (0,1,0,2)]:
                ni, nj = curr_i + di_c, curr_j + dj_c
                wi, wj = curr_i + di_w, curr_j + dj_w

                if 0 <= ni < len(maze) and 0 <= nj < len(maze[0]):
                    if (maze[ni][nj] == val_actuelle + 1 or maze[ni][nj] == -9) and maze[wi][wj] == 0:
                        maze[curr_i][curr_j] = -5
                        maze[wi][wj] = -5
                        curr_i, curr_j = ni, nj
                        break

        maze[i][j] = -3
        maze[i_finish][j_finish] = -4

    return maze


maze = generate_maze_skeleton(11, 11)
maze_42 = add_42_pattern(maze)
maze_finished = generate_maze(maze)
maze_solved = find_shortest_path(maze, (1, 1), (10, 10))
print_maze_pretty(maze)
for row in maze_solved:
    print(row)


