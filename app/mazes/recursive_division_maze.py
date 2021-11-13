from random import random, randint

import numpy as np
from numpy import full
from mazes.base import MazeBase


class RecursiveDivision(MazeBase):
    def __init__(self):
        self.maze = None
        self.space = None

    def make_maze(self, n_x: int, n_y: int) -> np.ndarray:
        self.maze = full([n_x, n_y], 0, dtype=int)
        self.space = self.maze
        self.maze = self._divide_space(self.space)
        final_maze = self._prepare_final(self.maze)
        return final_maze

    def _divide_space(self, space):
        # TODO: check for walls right next to new door placement
        # TODO: un-duplicate some of this function
        # TODO: maybe make smaller functions in here
        if random() > 0.5 and (space.shape[1] > 3):
            wall = randint(1, space.shape[1] - 2)
            space[:, wall] = 1
            door = randint(0, space.shape[0] - 1)
            space[door, wall] = 0
            new_space1 = space[:, :wall]
            new_space2 = space[:, wall + 1:]
        elif space.shape[0] > 3:
            wall = randint(1, space.shape[0] - 2)
            space[wall, :] = 1
            door = randint(0, space.shape[1] - 1)
            space[wall, door] = 0
            new_space1 = space[:wall, :]
            new_space2 = space[wall + 1:, :]
        elif space.shape[1] > 3:
            wall = randint(1, space.shape[1] - 2)
            space[:, wall] = 1
            door = randint(0, space.shape[0] - 1)
            space[door, wall] = 0
            new_space1 = space[:, :wall]
            new_space2 = space[:, wall + 1:]
        else:
            return space
        new_space1 = self._divide_space(new_space1)
        new_space2 = self._divide_space(new_space2)
        return space

    @staticmethod
    def _prepare_final(maze: np.ndarray) -> np.ndarray:
        final = full([maze.shape[0] + 2, maze.shape[1] + 2], 1, dtype=int)
        final[1:-1, 1:-1] = maze
        return final
