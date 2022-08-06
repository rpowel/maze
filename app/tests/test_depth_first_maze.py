import random

from mazes import DepthFirstMaze


def test_maze_depth_first():
    random.seed(1)
    n_x = n_y = 10
    result = DepthFirstMaze().make_maze(n_x, n_y)
    print()
    print(result)
