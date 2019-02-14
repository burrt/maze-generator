import yaml
import logging
import argparse

description = """
              Maze generation with some different path search algorithms.
              If no options are specified, it will default to PRIM's with A* search.
              There are many options that you can configure, read carefully.
              """

class MazeConfig:
    # default settings
    maze_dimension = [10, 30]
    maze_start_cell = [0, 0]
    maze_exit_cell = [29, 29]
    maze_type = 'prim'
    maze_search_type = ['a*', 'dfs']
    maze_break_type = 'bfs'
    maze_logging = 'warning'


    # process cmd args
    def process_cmd_args(self):
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument("-d", "--dimension",
                            nargs=2,
                            type=int,
                            default=self.maze_dimension,
                            help="Maze dimension")
        parser.add_argument("--start-cell",
                            nargs=2,
                            type=int,
                            default=self.maze_start_cell,
                            help="Start cell - must be less than maze dimension")
        parser.add_argument("--exit-cell",
                            nargs=2,
                            type=int,
                            default=self.maze_exit_cell,
                            help="Exit cell - must be less than maze dimension")
        parser.add_argument("-m", "--maze-type",
                            choices=self.maze_exit_cell,
                            default='prim',
                            help="Maze generation algorithms: depth-first, PRIM's")
        parser.add_argument("-s", "--search-type",
                            nargs='*',
                            choices=['dfs', 'bfs', 'ucs', 'a*', 'gs'],
                            default=self.maze_search_type,
                            help="Path search algorithms: depth-first, breadth-first, uniform-cost, A*")
        parser.add_argument("-b", "--break-type",
                            choices=self.maze_break_type,
                            default='bfs',
                            help="Breaking deadends for imperfect maze: depth-first, breadth-first")
        parser.add_argument("-v", "--verbose",
                            choices=['warning', 'info', 'debug'],
                            default=self.maze_logging,
                            help="Print debugging - warning, info, debug")
        args = parser.parse_args()

        # set logging level
        if args.verbose == 'warning':
            self.maze_logging = logging.WARNING
        elif args.verbose == 'info':
            self.maze_logging = logging.INFO
        else:
            self.maze_logging = logging.DEBUG
        logging.basicConfig(format='%(levelname)s: %(message)s',
                            level=self.maze_logging)

        # check start and exit coords
        logging.debug("old start: {0}".format(args.start_cell))
        logging.debug("old exit: {0}".format(args.exit_cell))

        # set all cmd args
        self.maze_dimension = args.dimension
        self.maze_start_cell = args.start_cell
        self.maze_exit_cell = args.exit_cell
        self.maze_type = args.maze_type
        self.maze_search_type = args.search_type
        self.maze_break_type = args.break_type


    # process yaml config file
    def process_yaml_file(self, filepath):
        # read in config.yaml
        with open(filepath, 'r') as f:
            try:
                yaml_file = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                print(exc)

        if yaml_file:
            yaml_file = yaml_file[0]
            if 'dimension' in yaml_file:
                self.maze_dimension = yaml_file['dimension']
            if 'start_cell' in yaml_file:
                self.maze_start_cell = yaml_file['start_cell']
            if 'exit_cell' in yaml_file:
                self.maze_exit_cell = yaml_file['exit_cell']
            if 'maze_type' in yaml_file:
                self.maze_type = yaml_file['maze_type']
            if 'search_type' in yaml_file:
                self.maze_search_type = yaml_file['search_type']
            if 'break_type' in yaml_file:
                self.maze_break_type = yaml_file['break_type']
            if 'logging' in yaml_file:
                self.maze_logging = yaml_file['logging']
