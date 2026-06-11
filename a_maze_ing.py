"""
Main entry point for the A-Maze-ing project.

This module handles:
- Configuration parsing
- Terminal visualization
- User interactions
"""

import os
from output_file import output_file
# from mazegen_shaegels import MazeGenerator
from maze_generator import MazeGenerator
import sys


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


def print_maze(
        maze: list[list[int]],
        theme: dict[str, str],
        show_path: bool
        ) -> None:
    """
    Render the maze in the terminal using ASCII blocks and colors.

    Parameters
    ----------
    maze : list[list[int]]
        The maze grid encoded with integer cell values.
    theme : dict[str, str]
        Dictionary mapping maze elements (walls, path, start, end) to
        ANSI-colored string representations.
    show_path : bool
        Whether the solution path should be displayed.
    """
    EMPTY = "  "
    error_message = 0
    for row in maze:
        line = ""
        for cell in row:
            if cell == -1:
                line += theme["wall"]
            elif cell == -2:
                line += theme["sign"]
                error_message += 1
            elif cell == -3:
                line += theme["start"]
            elif cell == -4:
                line += theme["end"]
            elif cell == -5:
                line += theme["path"] if show_path else EMPTY
            else:
                line += EMPTY
        print(line)
    if error_message == 0:
        print("Error: could not draw 42 pattern in maze", file=sys.stderr)


def parsing(input: str) -> dict[str, str]:
    """
    Parse the maze configuration file.

    The configuration file must contain exactly six key-value pairs:
    WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT.

    Parameters
    ----------
    input : str
        Path to the configuration file.

    Returns
    -------
    dict[str, str]
        Dictionary containing configuration values as strings.

    Raises
    ------
    Exception
        If the configuration file is malformed or incomplete.
    """
    i = 0
    dic: dict[str, str] = {}
    with open(input, "r") as file:
        t_text = file.read()
        text = t_text.splitlines()
        for lines in text:
            if lines.startswith('#'):
                pass
            else:
                line = lines.split('=')
                if len(line) != 2:
                    raise Exception("Invalid configuration")
                start = line[0]
                match start:
                    case "WIDTH":
                        dic['width'] = line[1]
                    case "HEIGHT":
                        dic['height'] = line[1]
                    case "ENTRY":
                        dic['entry'] = line[1]
                    case "EXIT":
                        dic['exit'] = line[1]
                    case "OUTPUT_FILE":
                        dic['output'] = line[1]
                    case "PERFECT":
                        dic['perfect'] = line[1]
                i += 1
    if i != 6:
        raise Exception("Invalid configuration")
    return dic


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: no inputfil given", file=sys.stderr)
        quit()
    inputfile = sys.argv[1]
    try:
        input_data = parsing(inputfile)
        width = int(input_data['width'])
        height = int(input_data['height'])
        if width <= 0 or height <= 0:
            raise Exception("Impossible maze parameters")
        start = tuple(int(x) for x in input_data['entry'].split(','))
        if len(start) != 2:
            raise Exception("Bad syntax")
        end = tuple(int(x) for x in input_data['exit'].split(','))
        if len(end) != 2:
            raise Exception("Bad syntax")
        for (x, y) in [start, end]:
            if x >= width or x < 0 or y >= height or y < 0:
                raise Exception("Impossible maze parameters")
        if start == end:
            raise Exception("Impossible maze parameters")
        print(start, file=sys.stderr)
        outputfile = input_data['output']
        if input_data['perfect'] == "True":
            perfect = True
        elif input_data['perfect'] == "False":
            perfect = False
        else:
            raise Exception("Invalid configuration")
    except FileNotFoundError:
        print(f"Error: File not found: {inputfile}", file=sys.stderr)
        quit()
    except PermissionError:
        print(f"Error: Permission error: {inputfile}", file=sys.stderr)
        quit()
    except ValueError:
        print("Error: Bad syntax", file=sys.stderr)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        quit()

    generator = MazeGenerator(width, height, start, end, perfect)

    user_choice = 0
    show_path = True
    current_theme_idx = 0
    print_maze(generator.maze, THEMES[current_theme_idx], show_path)

    while user_choice != 5:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_maze(generator.maze, THEMES[current_theme_idx], show_path)
        try:
            output_file(generator.maze, width, height,
                        start, end, outputfile)
        except Exception:
            quit()

        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path")
        print("3. Rotate maze colors")
        print("4. Enter a seed (Optional)")
        print("5. Quit")

        try:
            user_choice = int(input("Choice? (1-5): "))
        except ValueError:
            user_choice = 0

        if user_choice == 1:
            generator = MazeGenerator(width, height, start, end, perfect)
            try:
                output_file(generator.maze, width, height,
                            start, end, outputfile)
            except Exception:
                quit()

        elif user_choice == 2:
            show_path = not show_path
        elif user_choice == 3:
            current_theme_idx = (current_theme_idx + 1) % 3
        elif user_choice == 4:
            try:
                seed = int(input("Seed choice:(int)"))
            except ValueError:
                print("Error: invalid seed value", file=sys.stderr)
                user_choice = 4
            generator = MazeGenerator(width, height, start, end, perfect, seed)
            try:
                output_file(generator.maze, width, height,
                            start, end, outputfile)
            except Exception:
                quit()
        elif user_choice == 5:

            quit()
