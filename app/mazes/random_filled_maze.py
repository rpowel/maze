from numpy import zeros
from random import randint


def _fill_square(percentage=50):
    random_ = randint(0, 101)
    if random_ > percentage:
        return 1
    return 0


class RandomMaze:
    # TODO: Finish random mazes
    def make_maze(self, n_x, n_y):
        maze_arr = zeros([n_x, n_y], dtype=int)
        for i in range(n_x):
            for j in range(n_y):
                maze_arr[i, j] = _fill_square()
        return maze_arr

    # def _check_percolation(self, maze):
    #     # TODO Check percolation of random maze
    #     range_x = maze.shape[0]
    #     range_y = maze.shape[1]
