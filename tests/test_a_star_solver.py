import random

import numpy as np

from mazes.maze_generators import KruskalMaze
from solvers.solver_generators import AStarSolver


def test_a_star_solver():
    random.seed(1)
    n_x = n_y = 10
    maze = [val for val in KruskalMaze().generate(n_x, n_y)][-1]

    solver = AStarSolver().solve(maze)
    result = [val for val in solver][-1]
    correct = np.array(
        [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [2, 6, 1, 5, 1, 6, 6, 6, 6, 6, 6, 3],
            [1, 6, 1, 5, 1, 6, 1, 1, 1, 1, 1, 1],
            [1, 6, 5, 5, 1, 6, 5, 5, 5, 5, 5, 1],
            [1, 6, 1, 1, 1, 6, 1, 1, 1, 5, 1, 1],
            [1, 6, 5, 5, 1, 6, 5, 5, 1, 5, 5, 1],
            [1, 6, 1, 1, 1, 6, 1, 0, 1, 0, 1, 1],
            [1, 6, 6, 6, 6, 6, 1, 0, 1, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
        dtype=int,
    )
    assert np.array_equal(result, correct)
