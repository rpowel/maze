#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 10:44:44 2020.

@author: powel
"""
from numpy import zeros, ones, full
from random import randint, random

from mazes.kruskal_maze import KruskalMaze
from mazes.prim_maze import PrimMaze


def _fill_square(percentage=50):
    random_ = randint(0, 101)
    if random_ > percentage:
        return 1
    return 0


class Maze:
    def __init__(self):
        self.maze = None

    def make_maze(self, n_x, n_y, maze_type='Prim'):
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
        self._set_entrance()
        self._set_exit()

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


class RecursiveDivision:
    def __init__(self):
        self.maze = None
        self.space = None

    def make_maze(self, n_x, n_y):
        self.maze = full([n_x, n_y], 0, dtype=int)
        self.space = self.maze
        self.maze = self._divide_space(self.space)
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
