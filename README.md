# Maze

Currently implemented the following maze generation algorithms:

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
* Additional heuristics
* Circular mazes
* Extensibility is almost impossible without design patterns

## Running

For sanity purposes, it is **only** compatible with Python 3+.

```bash
$ git clone https://github.com/burrt/maze-generator.git

# activate your venv
$ cd maze-generator
$ python -m venv venv
$ source venv/bin/activate

$ pip install pip-tools
$ pip-compile requirements.in
$ pip install -r requirements.txt

$ python maze -h
$ python maze
```

### Example Configuration YAML file

Command line arguments will override the config file.

```yaml
# config.yaml

- dimension:
    - 10 # rows
    - 30 # cols
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
