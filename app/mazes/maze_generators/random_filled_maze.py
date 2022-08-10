from random import randint

import numpy as np
from numpy import zeros, full

from .base import MazeBase


class RandomMaze(MazeBase):
    def make_maze(self, n_x, n_y) -> np.ndarray:
        maze_arr = zeros([n_x, n_y], dtype=int)
        for i in range(n_x):
            for j in range(n_y):
                maze_arr[i, j] = self._fill_square()
        yield maze_arr

    @staticmethod
    def _prepare_final(maze: np.ndarray) -> np.ndarray:
        """Prepare final maze with border of walls."""
        final = full([maze.shape[0] + 2, maze.shape[1] + 2], 1, dtype=int)
        final[1:-1, 1:-1] = maze
        return final

    @staticmethod
    def _fill_square(percentage=50):
        random_ = randint(0, 101)
        if random_ > percentage:
            return 1
        return 0
