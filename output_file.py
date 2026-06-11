"""
Maze export utilities.

This module handles:
- Hexadecimal wall encoding
- Writing the maze to an output file
- Writing the shortest path
"""
import sys
from typing import TextIO

WALL = -1
PATH = -5
EXIT = -4


def nbr_to_hex(binary: list[int]) -> str:
    """
    Convert a list of bits into a hexadecimal character.

    Parameters
    ----------
    binary : list[int]
        List of bits (0 or 1).

    Returns
    -------
    str
        Hexadecimal representation.
    """
    value = 0
    for bit in binary:
        value = (value << 1) | bit
    return format(value, 'X')


def write_shortest_path(
        maze: list[list[int]],
        entry: tuple[int, ...],
        final: tuple[int, ...],
        fd: TextIO
        ) -> None:
    """
    Write the shortest path from entry to exit to a file.

    Parameters
    ----------
    maze : list[list[int]]
        Maze grid with path markings.
    entry : tuple[int, int]
        Entry coordinates.
    final : tuple[int, int]
        Exit coordinates.
    fd : TextIO
        Open file descriptor.
    """
    x, y = entry[0] * 2 + 1, entry[1] * 2 + 1
    fx, fy = final[0] * 2 + 1, final[1] * 2 + 1

    path = []
    prev = None

    directions = {
            'N': (0, -1),
            'S': (0, 1),
            'W': (-1, 0),
            'E': (1, 0)
    }

    while (x, y) != (fx, fy):
        for direction, (dx, dy) in directions.items():
            nextx, nexty = x + dx, y + dy
            if maze[nexty][nextx] not in (PATH, EXIT):
                continue
            if (nextx, nexty) == prev:
                continue
            path.append(direction)
            prev = x, y
            x, y = nextx, nexty
            break

    fpath = [path[i] for i in range(len(path)) if i % 2 == 0]
    fd.write(f'{"".join(fpath)}\n')


def write_maze_hex(
        maze: list[list[int]],
        width: int,
        height: int,
        fd: TextIO
        ) -> None:
    """
    Write the maze grid using hexadecimal wall encoding.

    Parameters
    ----------
    maze : list[list[int]]
        Maze grid.
    width : int
        Maze width.
    height : int
        Maze height.
    fd : TextIO
        Open file descriptor.
    """
    lines = []

    for y in range(1, height * 2, 2):
        line = []
        for x in range(1, width * 2, 2):
            walls = [
                maze[y][x - 1] == WALL,  # west
                maze[y + 1][x] == WALL,  # south
                maze[y][x + 1] == WALL,  # east
                maze[y - 1][x] == WALL,  # north
            ]
            line.append(nbr_to_hex([int(wall) for wall in walls]))
        lines.append("".join(line))

    for row in lines:
        fd.write(f"{row}\n")
    fd.write('\n')


def output_file(
        maze: list[list[int]],
        width: int,
        height: int,
        entry: tuple[int, ...],
        final: tuple[int, ...],
        file: str
        ) -> None:
    """
    Write the complete maze output file.

    Parameters
    ----------
    maze : list[list[int]]
        Maze grid.
    width : int
        Maze width.
    height : int
        Maze height.
    entry : tuple[int, int]
        Entry coordinates.
    final : tuple[int, int]
        Exit coordinates.
    file : str
        Output filename.
    """
    try:
        with open(file, 'w') as fd:
            write_maze_hex(maze, width, height, fd)
            fd.write(f"{entry[0]},{entry[1]}\n")
            fd.write(f"{final[0]},{final[1]}\n")
            write_shortest_path(maze, entry, final, fd)
    except PermissionError:
        print(f"Error: Permission denied: '{file}'", file=sys.stderr)
        raise PermissionError
    except OSError as e:
        print(f"Error: {e}", file=sys.stderr)
        raise OSError
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        raise Exception
