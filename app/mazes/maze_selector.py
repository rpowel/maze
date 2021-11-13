#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 10:44:44 2020.

@author: powel
"""
from numpy import zeros, ones
from random import randint

from mazes.kruskal_maze import KruskalMaze
from mazes.prim_maze import PrimMaze
from mazes.recursive_division_maze import RecursiveDivision


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


if __name__ == "__main__":
    N = 8
    maze = Maze().make_maze(N, N, maze_type='Prim')
    print(maze)
