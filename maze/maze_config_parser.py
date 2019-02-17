import math
import yaml
import logging
import argparse

description = """
              Maze generation with some different path search algorithms.
              If no options are specified, it will default to PRIM's with A* search.
              There are many options that you can configure, read carefully.
              """

class MazeConfig:
    def __init__(self):
        # default settings
        self.maze_dimension = [10, 30]
        self.maze_start_cell = [0, 0]
        self.maze_exit_cell = [29, 29]
        self.maze_type = 'prim'
        self.maze_search_type = ['a*', 'dfs']
        self.maze_break_type = 'bfs'
        self.maze_logging = 'warning'


    def set_logging_level(self, user_setting):
        """Set the logging level to be used by maze"""

        if user_setting == 'warning':
            self.maze_logging = logging.WARNING
            print('warning')
        elif user_setting == 'info':
            self.maze_logging = logging.INFO
        else:
            self.maze_logging = logging.DEBUG


    def process_cmd_args(self):
        """Process command line arguments if YAML configuration file doesn't exist"""

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
        self.set_logging_level(args.verbose)

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


    def process_yaml_file(self, filepath):
        """Process the YAML configuration file if it exists"""

        with open(filepath, 'r') as f:
            try:
                yaml_file = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                logging.exception(exc)

        if yaml_file:
            yaml_file = {k: v for d in yaml_file for k, v in d.items()}
            if 'dimension' in yaml_file:
                self.maze_dimension = yaml_file['dimension']
            if 'start_cell' in yaml_file:
                self.maze_start_cell = yaml_file['start_cell']
            if 'exit_cell' in yaml_file:
                self.maze_exit_cell = yaml_file['exit_cell']
            if 'maze_type' in yaml_file:
                self.maze_type = yaml_file['maze_type'][0]
            if 'search_type' in yaml_file:
                self.maze_search_type = yaml_file['search_type']
            if 'break_type' in yaml_file:
                self.maze_break_type = yaml_file['break_type'][0]
            if 'logging' in yaml_file:
                self.maze_logging = yaml_file['logging'][0]

        # set logging level
        self.set_logging_level(self.maze_logging)


    def reset_to_defaults(self, start_cell, exit_cell):
        logging.warn("Start and exit coordinates are equal - resetting to default coordinates")
        return [0, 0], [self.maze_dimension[0]-1, self.maze_dimension[1]-1]


    def adjust_cell(self, cell, is_start_cell):
        """Cell is a list (coordinate) - find the closest boundary of the maze"""

        adjusted_cell = cell.copy()
        maze_rows = self.maze_dimension[0]
        maze_cols = self.maze_dimension[1]

        # HACK to 'pretend' these are coordinates
        maze_rows = maze_rows - 1
        maze_cols = maze_cols - 1

        # if negative coordinates - default to (0, 0)
        adjusted_cell[0] = 0 if adjusted_cell[0] < 0 else adjusted_cell[0]
        adjusted_cell[1] = 0 if adjusted_cell[1] < 0 else adjusted_cell[1]

        # attempt to find shortest distance to N, E, S, W walls
        north_distance = math.inf
        east_distance = 0
        south_distance = 0
        west_distance = math.inf

        # handle coordinates outside the boundary maze
        if adjusted_cell[0] < maze_rows:
            north_distance = adjusted_cell[0]
            south_distance = maze_rows - adjusted_cell[0]
        else:
            north_distance = maze_rows
            south_distance = adjusted_cell[0] - maze_rows
            adjusted_cell[0] = maze_rows
        if adjusted_cell[1] < maze_cols:
            east_distance = maze_cols - adjusted_cell[1]
            west_distance = adjusted_cell[1]
        else:
            east_distance = adjusted_cell[1] - maze_cols
            west_distance = maze_cols
            adjusted_cell[1] = maze_cols

        vertical_distance = min(north_distance, south_distance)
        horizontal_distance = min(west_distance, east_distance)

        # assume start/exit cells lie within the maze boundaries here
        if vertical_distance < horizontal_distance:
            if south_distance < north_distance:
                adjusted_cell[0] = maze_rows
            else:
                adjusted_cell[0] = 0
        else:
            if east_distance < west_distance:
                adjusted_cell[1] = maze_cols
            else:
                adjusted_cell[1] = 0

        logging.info("Adjusted cell: {0}".format(adjusted_cell))
        return adjusted_cell
