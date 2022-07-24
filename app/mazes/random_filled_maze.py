from random import randint

import numpy as np
from numpy import zeros, full

from mazes.base import MazeBase


def _fill_square(percentage=50):
    random_ = randint(0, 101)
    if random_ > percentage:
        return 1
    return 0


class RandomMaze(MazeBase):
    @staticmethod
    def _prepare_final(maze: np.ndarray) -> np.ndarray:
        """Prepare final maze with border of walls."""
        final = full([maze.shape[0] + 2, maze.shape[1] + 2], 1, dtype=int)
        final[1:-1, 1:-1] = maze
        return final

    def make_maze(self, n_x, n_y):
        maze_arr = zeros([n_x, n_y], dtype=int)
        for i in range(n_x):
            for j in range(n_y):
                maze_arr[i, j] = _fill_square()
        final_maze = self._prepare_final(maze_arr)
        return final_maze

    # def _check_percolation(self, maze):
    #     # TODO Check percolation of random maze
    #     range_x = maze.shape[0]
    #     range_y = maze.shape[1]
