#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 10:44:44 2020.

@author: powel
"""
from numpy import zeros, ones, ravel, full, arange, reshape
from scipy import spatial
from random import randint, random


def _fill_square(percentage=50):
    random_ = randint(0, 101)
    if random_ > percentage:
        return 1
    return 0


class Maze:
    def __init__(self):
        self.maze = None

    def make_maze(self, n_x, n_y, maze_type='Prim'):
        maze_temp = None
        maze_generator = self.gen_maze(n_x, n_y, maze_type=maze_type)
        while True:
            try:
                maze_temp = maze_generator.__next__()
            except StopIteration:
                break
        self.maze = maze_temp
        #        self.maze = self._prepare_final()
        #        self._set_entrance()
        #        self._set_exit()
        return self.maze

    def gen_maze(self, n_x, n_y, maze_type='Prim'):
        if maze_type == 'Random':
            self.maze = RandomMaze().make_maze(n_x, n_y)
        elif maze_type == 'Prim':
            self.maze = PrimMaze().make_maze(n_x, n_y)
        elif maze_type == 'Kruskal':
            self.maze = KruskalMaze().make_maze(n_x, n_y)
        elif maze_type == 'Recursive':
            self.maze = RecursiveDivision().make_maze(n_x, n_y)
        else:
            self.maze = None

        return self.maze

    def _set_entrance(self):
        while True:
            x, y = randint(1, self.maze.shape[0] - 1), 0
            if self.maze[x, y + 1] == 0:
                break
        self.maze[x, y] = 2

    def _set_exit(self):
        while True:
            x, y = randint(1, self.maze.shape[0] - 1), self.maze.shape[1] - 1
            if self.maze[x, y - 1] == 0:
                break
        self.maze[x, y] = 3

    def _prepare_final(self):
        maze_temp = ones([self.maze.shape[0] + 1, self.maze.shape[1] + 1], dtype=int)
        maze_temp[1:-1, 1:-1] = self.maze[:-1, :-1]
        return maze_temp

    # def _check_percolation(self, maze):
    #     # TODO Check percolation of random maze
    #     range_x = maze.shape[0]
    #     range_y = maze.shape[1]


class RandomMaze:
    # TODO: Finish random mazes
    def make_maze(self, n_x, n_y):
        maze_arr = zeros([n_x, n_y], dtype=int)
        for i in range(n_x):
            for j in range(n_y):
                maze_arr[i, j] = _fill_square()
        return maze_arr


class PrimMaze:
    def __init__(self):
        self._loop = True
        self.walls = []
        self.passage = []
        self.maze = None

    def make_maze(self, n_x, n_y):
        self.maze = full([n_x + 1, n_y + 1], 1, dtype=int)
        x, y = randint(1, n_x - 1), 1
        self.passage.append([x, y])
        self.maze[x, y] = 0
        self._add_walls(x, y)

        for i in range(n_x * n_y * 10):
            pos, wall = self._pick_wall()
            if pos is None:
                break
            x, y = pos
            self.maze[x, y] = 0
            self.walls.pop(wall)
            self._add_walls(x, y)
            self.passage.append([x, y])

            if len(self.passage) > (n_x * n_y / 4):
                break  # prevents weird mazes with only a few squares

            # temp_maze = self._prepare_final()
            yield self.maze

    def _add_walls(self, x, y):
        self.ghost_maze = zeros(
            [self.maze.shape[0] + 2, self.maze.shape[1] + 2],
            dtype=int
        )
        self.ghost_maze[1:-1, 1:-1] = self.maze

        if self.ghost_maze[x + 1, y + 2]:
            self.walls.append([x, y + 1])
        if self.ghost_maze[x + 1, y]:
            self.walls.append([x, y - 1])
        if self.ghost_maze[x + 2, y + 1]:
            self.walls.append([x + 1, y])
        if self.ghost_maze[x, y + 1]:
            self.walls.append([x - 1, y])

    def _pick_wall(self):
        iterations = 0
        while True:
            high = len(self.walls)
            iterations += 1
            if iterations > high * 2:
                return None, None
            rand_wall = randint(0, high - 1)

            x_wall, y_wall = self.walls[rand_wall]
            x, y = self._find_nearest_passage([x_wall, y_wall])
            diff_x = x - x_wall
            diff_y = y - y_wall

            try:
                next_over = self.maze[x_wall - diff_x, y_wall - diff_y]
                if diff_x != 0:
                    next_right = self.maze[x_wall, y_wall - 1]
                    next_left = self.maze[x_wall, y_wall + 1]
                    next_right_over = self.maze[x_wall - diff_x, y_wall - 1]
                    next_left_over = self.maze[x_wall - diff_x, y_wall + 1]
                else:
                    next_right = self.maze[x_wall + 1, y_wall]
                    next_left = self.maze[x_wall - 1, y_wall]
                    next_right_over = self.maze[x_wall + 1, y_wall - diff_y]
                    next_left_over = self.maze[x_wall - 1, y_wall - diff_y]

            except Exception:  # TODO: Make more specific exception
                continue

            if not (next_over and next_right and next_left
                    and next_left_over and next_right_over):
                self.walls.pop(rand_wall)
            else:
                return self.walls[rand_wall], rand_wall

    def _find_nearest_passage(self, pos):
        _, index = spatial.cKDTree(self.passage).query(pos)
        return self.passage[int(index)]

    def _prepare_final(self):
        maze_temp = ones([self.maze.shape[0] + 1, self.maze.shape[1] + 1], dtype=int)
        maze_temp[1:-1, 1:-1] = self.maze[:-1, :-1]
        return maze_temp


class KruskalMaze:
    def __init__(self):
        self.num_cells_last = None
        self.maze = None
        self._repeat_iterations = None

    def make_maze(self, n_x, n_y):
        self.num_cells_last = -1
        len_x = (n_x + 4)
        len_y = (n_y + 4)
        self.maze = full([len_x, len_y], 1, dtype=int)
        self._make_walls()
        self._make_sets()
        self._repeat_iterations = 0
        while True:
            self._join_cells()
            if self._check_final():
                break
        self._prepare_final()
        return self.maze

    def _make_walls(self):
        self.walls = arange(0, self.maze.size, dtype=int)
        self.walls = reshape(self.walls, self.maze.shape)
        for i in range(self.maze.shape[0]):
            if (i % 2) == 1:
                self.walls[i, :] = -1
        for j in range(self.maze.shape[1]):
            if (j % 2) == 1:
                self.walls[:, j] = -1
        self.walls[:, 0] = self.walls[:, -1] = -1
        self.walls[0, :] = self.walls[-1, :] = -1

    def _make_sets(self):
        self.sets = []
        for i in range(self.walls.shape[0]):
            for j in range(self.walls.shape[1]):
                wall_id = self.walls[i, j]
                self.sets.append({wall_id})

    def _pick_wall(self):
        while True:
            i = randint(2, self.walls.shape[0] - 3)
            j = randint(2, self.walls.shape[1] - 3)
            wall_id = self.walls[i, j]
            if ((self.walls[i + 1, j] == -1)
                    and (self.walls[i - 1, j] == -1)
                    and (self.walls[i, j + 1] == -1)
                    and (self.walls[i, j - 1] == -1)):
                continue
            if wall_id == -1:
                return i, j

    def _check_wall(self):
        id_1 = None
        id_2 = None
        i_1 = None
        i_2 = None
        j_1 = None
        j_2 = None

        for i in range(5):
            i, j = self._pick_wall()
            set_id_left = self.walls[i - 1, j]
            set_id_right = self.walls[i + 1, j]
            set_id_up = self.walls[i, j + 1]
            set_id_down = self.walls[i, j - 1]

            set_left = self.sets[set_id_left]
            set_right = self.sets[set_id_right]
            set_up = self.sets[set_id_up]
            set_down = self.sets[set_id_down]

            rand_flt = random()
            if rand_flt <= 0.5:
                sym_diff = set_left ^ set_right
                if (set_id_left in sym_diff) and (set_id_right in sym_diff):
                    id_1 = set_id_left
                    id_2 = set_id_right
                    i_1, j_1 = i - 1, j
                    i_2, j_2 = i + 1, j

            else:
                sym_diff = set_up ^ set_down
                if (set_id_up in sym_diff) and (set_id_down in sym_diff):
                    id_1 = set_id_up
                    id_2 = set_id_down
                    i_1, j_1 = i, j + 1
                    i_2, j_2 = i, j - 1

            if id_1 is None:
                continue
            self.walls[i, j] = -2

            self.maze[i, j] = 0
            self.maze[i_1, j_1] = 0
            self.maze[i_2, j_2] = 0

            return id_1, id_2

        return None, None

    def _check_final(self):
        flat = ravel(self.maze)
        num_cells = len(flat[flat == 0])
        if num_cells == self.num_cells_last:
            self._repeat_iterations += 1
        if self._repeat_iterations > 20:
            return True
        if num_cells != self.num_cells_last:
            self._repeat_iterations = 0
            self.num_cells_last = num_cells
        return False

    def _join_cells(self):
        id_1, id_2 = self._check_wall()
        if id_1 is None:
            return None

        for i in range(self.maze.shape[0]):
            for j in range(self.maze.shape[1]):
                if self.maze[i, j] == 0:
                    if self.maze[i + 1, j] == 0:
                        self.sets[self.walls[i, j]].update(self.sets[self.walls[i + 2, j]])
                        self.sets[self.walls[i + 2, j]].update(self.sets[self.walls[i, j]])
                    if self.maze[i - 1, j] == 0:
                        self.sets[self.walls[i, j]].update(self.sets[self.walls[i - 2, j]])
                        self.sets[self.walls[i - 2, j]].update(self.sets[self.walls[i, j]])
                    if self.maze[i, j + 1] == 0:
                        self.sets[self.walls[i, j]].update(self.sets[self.walls[i, j + 2]])
                        self.sets[self.walls[i, j + 2]].update(self.sets[self.walls[i, j]])
                    if self.maze[i, j - 1] == 0:
                        self.sets[self.walls[i, j]].update(self.sets[self.walls[i, j - 2]])
                        self.sets[self.walls[i, j - 2]].update(self.sets[self.walls[i, j]])

    def _prepare_final(self):
        maze_temp = ones([self.maze.shape[0] - 2, self.maze.shape[1] - 2], dtype=int)
        maze_temp[1:-1, 1:-1] = self.maze[2:-2, 2:-2]
        self.maze = maze_temp


class RecursiveDivision:
    def __init__(self):
        self.maze = None
        self.space = None

    def make_maze(self, n_x, n_y):
        self.maze = full([n_x, n_y], 0, dtype=int)
        self.space = self.maze
        self.maze = self._divide_space(self.space)
        self.maze = self._prep_final(self.maze)
        return self.maze

    def _divide_space(self, space):
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

    def _prep_final(self, maze):
        final = full([maze.shape[0] + 2, maze.shape[1] + 2], 1, dtype=int)
        final[1:-1, 1:-1] = maze
        return final


if __name__ == "__main__":
    N = 8
    maze = Maze().make_maze(N, N, maze_type='Prim')
    print(maze)
