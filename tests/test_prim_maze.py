import random

import numpy as np

from mazes.maze_generators import PrimMaze


def test_make_maze():
    random.seed(1)
    n_x = n_y = 10
    result = [val for val in PrimMaze().make_maze(n_x, n_y)][0]
    correct = np.array(
        [
            [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1],
            [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
            [0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1],
            [1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1],
            [1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1],
            [1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
        dtype=int,
    )
    assert np.array_equal(result, correct)
