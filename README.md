*This project has been created as part of the 42 curriculum by shaegels, alsereme.*

# A-Maze-ing – This is the way

## Description

**A-Maze-ing** is a maze generator written in Python. The program reads a configuration file, generates a random maze according to the given parameters, computes the shortest path between an entry and an exit, and exports the maze in a strict hexadecimal format suitable for automated validation.

The project focuses on algorithmic maze generation, graph traversal, data encoding, and clean software architecture. A terminal-based visual representation allows interactive exploration of the generated maze.

---
## Instructions

### Requirements

- Python **3.10** or later
- `make`
- Tools used for linting:
  - `flake8`
  - `mypy`

### Installation

```bash
make install
```

This installs the required tools.

### Execution

```bash
make run
```

Or directly:

```bash
python3 a_maze_ing.py config.txt
```

### Debug mode

```bash
make debug
```

### Code quality checks

Mandatory linting:

```bash
make lint
```

Strict linting (optional):

```bash
make lint-strict
```

### Cleaning the repository

```bash
make clean
```

---

## Configuration File Format

The configuration file is a plain text file containing one `KEY=VALUE` pair per line.
Lines starting with `#` are treated as comments.

### Mandatory keys

```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

### Description of keys

- `WIDTH` / `HEIGHT`: maze dimensions in number of cells
- `ENTRY`: entry coordinates `(x,y)`
- `EXIT`: exit coordinates `(x,y)`
- `OUTPUT_FILE`: file where the maze will be written
- `PERFECT`: if `True`, the maze contains exactly one valid path between entry and exit

---

## Maze Generation Algorithm

The maze generation is based on a **randomized union/merge approach** inspired by Kruskal’s algorithm:

1. The maze is initialized as a grid of isolated cells separated by walls.
2. Each cell is assigned a unique identifier.
3. Random walls are removed if they separate two different regions.
4. When a wall is removed, the two regions are merged.
5. The process continues until all cells belong to the same region.

A breadth-first search (BFS) is then used to compute the **shortest path** between the entry and the exit.

A special visible **“42” pattern** made of fully closed cells is inserted when the maze size allows it.

---

## Why This Algorithm

This algorithm was chosen because:

- It guarantees full connectivity of the maze
- It naturally produces a **perfect maze** (single path between any two points)
- It is easy to reason about and validate
- It maps well to graph theory concepts taught at 42

---

## Output File Format

Each maze cell is encoded using **one hexadecimal digit** representing closed walls:

| Direction | Bit value |
|---------|-----------|
| North   | 1 |
| East    | 2 |
| South   | 4 |
| West    | 8 |

- A closed wall sets the bit to `1`
- An open wall sets the bit to `0`

Cells are written row by row. After an empty line, the following are written:

1. Entry coordinates
2. Exit coordinates
3. Shortest path using `N`, `E`, `S`, `W`

---

## Reusable Maze Generator (mazegen)

The maze generation logic is implemented as a reusable Python module named
`mazegen_shaegels`, designed to be imported in future projects.

### Usage example

```bash
pip install mazegen_shaegels-0.1.0.tar.gz
```

```python
from mazegen_shaegels import MazeGenerator

generator = MazeGenerator(
    width=20,
    height=15,
    start=(0, 0),
    end=(19, 14),
    perfect=True,
    seed=42
)

maze = generator.maze
```

### Accessing results
- The maze structure is available via `generator.maze`
- The maze is a made of cells even for walls
    so every coordinates needs to be * 2 + 1
- The shortest path is marked inside the maze grid (-5)

---

## Team and Project Management

### Team roles

shaegels:
- **Algorithm & logic**: maze generation, pathfinding
- **Rendering & UX**: terminal visualization and user interactions
- **Parsing**: configuration file handling
alsereme:
- **Output encoding**: hexadecimal wall encoding and file export
- **Error validation**: all thorough error management
- **Linting**: flake8, mypy and docstrings


### Project organization

- Early focus on algorithm correctness
- Incremental addition of features (pathfinding, display, export)
- Continuous linting and refactoring

What worked well:
- Clear separation of responsibilities
- Early validation of output format

What could be improved:
- More automated tests
- Additional generation algorithms

---

## Resources

### Technical references

- Maze generation algorithms:
  - https://en.wikipedia.org/wiki/Maze_generation_algorithm
- Breadth-First Search (BFS)
- Python documentation: https://docs.python.org/3/

### AI usage

AI tools were used **only as assistance**, notably for:

- Clarifying specifications and encoding rules
- Explaining bitwise and hexadecimal representations
- Readme and docstring generation
- Final linting

All generated code and explanations were reviewed, understood, and adapted by the team.

