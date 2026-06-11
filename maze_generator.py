"""
Maze Generator Module
=====================

This module provides a reusable maze generator that can be imported
and used in other Python projects.

Usage example
-------------

>>> from mazegen import MazeGenerator
>>> gen = MazeGenerator(
...     width=20,
...     height=15,
...     start=(0, 0),
...     end=(19, 14),
...     perfect=True,
...     seed=42
... )
>>> maze = gen.maze

Parameters
----------
width : int
    Maze width in number of cells.
height : int
    Maze height in number of cells.
start : tuple[int, int]
    Entry coordinates (x, y).
end : tuple[int, int]
    Exit coordinates (x, y).
perfect : bool
    Whether the maze has a single unique solution.
seed : int
    Random seed for reproducibility.

Accessing results
-----------------
- The maze structure is available via `generator.maze`
- The maze is a made of cells even for walls
    so every coordinates needs to be * 2 + 1
- The shortest path is marked inside the maze grid (-5)
"""

import random


def generate_maze_skeleton(width: int, height: int) -> list[list[int]]:
    """
    Create the initial maze skeleton with isolated cells and walls.

    Parameters
    ----------
    width : int
        Maze width in number of cells.
    height : int
        Maze height in number of cells.

    Returns
    -------
    list[list[int]]
        A 2D grid representing the initial maze structure.
    """
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


def add_42_pattern(
        maze: list[list[int]],
        start: tuple[int, ...],
        end: tuple[int, ...]
        ) -> bool:
    """
    Insert the '42' pattern into the maze by closing specific cells.

    The pattern is added only if it does not overlap the entry or exit
    and if there is enough space.

    Parameters
    ----------
    maze : list[list[int]]
        Maze grid.
    start : tuple[int, int]
        Entry coordinates.
    end : tuple[int, int]
        Exit coordinates.

    Returns
    -------
    bool
        True if the pattern was added successfully, False otherwise.
    """
    start_coords = (start[1] * 2 + 1, start[0] * 2 + 1)
    end_coords = (end[1] * 2 + 1, end[0] * 2 + 1)

    x, y = len(maze) // 2, len(maze[0]) // 2
    if x % 2 == 0:
        x += 1
    if y % 2 == 0:
        y += 1

    offsets = [(0, -2), (0, -4), (0, -6), (-2, -6), (-4, -6), (2, -2), (4, -2),
               (4, 2), (2, 2), (0, 2), (4, 4), (4, 6), (0, 4), (0, 6), (-2, 6),
               (-4, 6), (-4, 4), (-4, 2)]
    for ox, oy in offsets:
        target = (x + ox, y + oy)
        if target == start_coords or target == end_coords:
            return False
    for ox, oy in offsets:
        target = (x + ox, y + oy)
        if target != start_coords and target != end_coords:
            close_cells(maze, target)

    return True


def is_maze_finished(maze: list[list[int]]) -> bool:
    """
    Check whether all cells in the maze belong to the same region.

    Parameters
    ----------
    maze : list[list[int]]
        Maze grid.

    Returns
    -------
    bool
        True if the maze is fully connected, False otherwise.
    """

    indicator = maze[1][1]
    for row in maze:
        for cell in row:
            if cell > 0 and cell != indicator:
                return False
    return True


def generate_maze(
        width: int,
        height: int,
        start: tuple[int, ...],
        end: tuple[int, ...],
        perfect: bool
        ) -> list[list[int]]:
    """
    Generate a maze using a randomized merging algorithm.

    Optionally removes additional walls if the maze is not perfect.

    Parameters
    ----------
    width : int
        Maze width.
    height : int
        Maze height.
    start : tuple[int, int]
        Entry coordinates.
    end : tuple[int, int]
        Exit coordinates.
    perfect : bool
        Whether the maze must be perfect (single solution).

    Returns
    -------
    list[list[int]]
        Generated maze grid.
    """

    maze = generate_maze_skeleton(width, height)
    if width and height > 7:
        if add_42_pattern(maze, start, end) is not False:
            add_42_pattern(maze, start, end)

    candidates: list[tuple[int, int]] = []
    for i in range(1, len(maze) - 1):
        for j in range(1, len(maze[0]) - 1):
            if maze[i][j] == -1:
                candidates.append((i, j))

    while candidates and not is_maze_finished(maze):
        chosen_i, chosen_j = random.choice(candidates)

        v_haut, v_bas = (
                maze[chosen_i - 1][chosen_j],
                maze[chosen_i + 1][chosen_j]
                )
        if v_haut > 0 and v_bas > 0 and v_haut != v_bas:
            maze[chosen_i][chosen_j] = 0
            for r in range(len(maze)):
                for c in range(len(maze[0])):
                    if maze[r][c] == v_bas:
                        maze[r][c] = v_haut

        v_gauche, v_droite = (
                maze[chosen_i][chosen_j - 1],
                maze[chosen_i][chosen_j + 1]
                )
        if v_gauche > 0 and v_droite > 0 and v_gauche != v_droite:
            maze[chosen_i][chosen_j] = 0
            for r in range(len(maze)):
                for c in range(len(maze[0])):
                    if maze[r][c] == v_droite:
                        maze[r][c] = v_gauche

        candidates.remove((chosen_i, chosen_j))
    if perfect is False:
        num_to_remove = int(len(candidates) * 0.4)
        random.shuffle(candidates)
        count = 0
        for i, j in candidates:
            if count >= num_to_remove:
                break

            if i % 2 == 1 and j % 2 == 0:
                if (maze[i][j-1] >= 0 or maze[i][j-1] == -9) and \
                   (maze[i][j+1] >= 0 or maze[i][j+1] == -9):
                    if maze[i][j] == -1:
                        maze[i][j] = 0
                        count += 1

            elif i % 2 == 0 and j % 2 == 1:
                if (maze[i-1][j] >= 0 or maze[i-1][j] == -9) and \
                   (maze[i+1][j] >= 0 or maze[i+1][j] == -9):
                    if maze[i][j] == -1:
                        maze[i][j] = 0
                        count += 1
    return maze


def close_cells(
        maze: list[list[int]],
        cell_number: tuple[int, int]
        ) -> list[list[int]]:
    """
    Close a cell and its surrounding walls.

    Used to draw the '42' pattern.

    Parameters
    ----------
    maze : list[list[int]]
        Maze grid.
    cell_number : tuple[int, int]
        Coordinates of the cell to close.

    Returns
    -------
    list[list[int]]
        Updated maze grid.
    """
    i, j = cell_number
    for r in range(i-1, i+2):
        for c in range(j-1, j+2):
            if 0 <= r < len(maze) and 0 <= c < len(maze[0]):
                maze[r][c] = -1
    maze[i][j] = -2
    return maze


def find_shortest_path(
        maze: list[list[int]],
        start: tuple[int, ...],
        end: tuple[int, ...]
        ) -> list[list[int]]:
    """
    Compute and mark the shortest path from entry to exit using BFS.

    Parameters
    ----------
    maze : list[list[int]]
        Maze grid.
    start : tuple[int, int]
        Entry coordinates.
    end : tuple[int, int]
        Exit coordinates.

    Returns
    -------
    list[list[int]]
        Maze grid with the path marked.
    """
    sc, sl = start
    ec, el = end
    i, j = sl * 2 + 1, sc * 2 + 1
    fi, fj = el * 2 + 1, ec * 2 + 1

    finished, count = False, -10
    maze[i][j] = -9
    following_cell: list[tuple[int, int]] = [(i, j)]

    while not finished and following_cell:
        next_cells = []
        for ci, cj in following_cell:
            for diw, djw, dic, djc in [
                    (-1, 0, -2, 0),
                    (1, 0, 2, 0),
                    (0, -1, 0, -2),
                    (0, 1, 0, 2)
                    ]:
                wi, wj, ni, nj = ci+diw, cj+djw, ci+dic, cj+djc
                if 0 <= ni < len(maze) and 0 <= nj < len(maze[0]):
                    if maze[wi][wj] == 0 and maze[ni][nj] > 0:
                        maze[ni][nj] = count
                        next_cells.append((ni, nj))
                        if ni == fi and nj == fj:
                            finished = True
        following_cell, count = next_cells, count - 1

    if finished:
        ci, cj = fi, fj
        while maze[ci][cj] != -9:
            val = maze[ci][cj]
            for diw, djw, dic, djc in [
                    (-1, 0, -2, 0),
                    (1, 0, 2, 0),
                    (0, -1, 0, -2),
                    (0, 1, 0, 2)
                    ]:
                wi, wj, ni, nj = ci+diw, cj+djw, ci+dic, cj+djc
                if 0 <= ni < len(maze) and 0 <= nj < len(maze[0]):
                    if maze[ni][nj] in (val + 1, -9) and maze[wi][wj] == 0:
                        maze[ci][cj] = -5
                        maze[wi][wj] = -5
                        ci, cj = ni, nj
                        break
        maze[i][j], maze[fi][fj] = -3, -4
    return maze


class MazeGenerator:
    """
    Maze generator class encapsulating generation and pathfinding logic.
    """
    def __init__(self,
                 width: int,
                 height: int,
                 start: tuple[int, ...],
                 end: tuple[int, ...],
                 perfect: bool,
                 seed: int | None = None) -> None:
        """
        Initialize the maze generator.

        Parameters
        ----------
        width : int
            Maze width.
        height : int
            Maze height.
        start : tuple[int, int]
            Entry coordinates.
        end : tuple[int, int]
            Exit coordinates.
        perfect : bool
            Whether the maze should be perfect.
        seed : int
            Random seed for reproducibility.
        """
        self.width = width
        self.height = height
        self.start = start
        self.end = end
        self.perfect = perfect
        if seed is not None:
            random.seed(seed)
        else:
            random.seed(None)
        self.maze = generate_maze(self.width, self.height, self.start,
                                  self.end, self.perfect)
        find_shortest_path(self.maze, self.start, self.end)
