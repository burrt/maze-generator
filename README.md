# Maze

Currently implmented the following maze generation alorithms:

* Depth-first backtracking
* Modified PRIM's

Currently implemented the following path search algorithms:

* Depth-first
* Breadth-first
* Uniform Cost or Dijkstra's
* Greedy
* A* (manhattan)

Future:

* 4+ direction movement
* Additional heuritics
* Circular mazes

## Running

For sanity purposes, it is **only** compatible with Python 3+.

```bash
python maze -h
python maze
```

### Example Configuration YAML file

If the configuration file exists - any command line arguments will be ignored

```yaml
// config.yaml

// rows, cols
- dimension:
    - 10
    - 30
- start_cell:
    - 0
    - 0
- exit_cell:
    - 29
    - 29
- maze_type:
    - prim
- search_type:
    - a*
    - dfs
- break_type:
    - bfs
- logging:
    - warning
```