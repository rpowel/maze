import random
from app.mazes.prim_maze import PrimMaze
import numpy as np


def test_make_maze():
    random.seed(1)
    n_x = n_y = 10
    result = PrimMaze().make_maze(n_x, n_y)
    correct = np.array(
        [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
            [1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
            [1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1],
            [1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1],
            [1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
        dtype=int,
    )
    assert np.array_equal(result, correct)
