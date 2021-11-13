#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 10:44:44 2020.

@author: powel
"""
from random import randint

import numpy as np

from mazes import RandomMaze, PrimMaze, KruskalMaze, RecursiveDivisionMaze


class Maze:
    def __init__(self):
        self.maze = None

    def make_maze(self, n_x: int, n_y: int, maze_type: str = 'Prim') -> np.ndarray:
        if maze_type == 'Random':
            self.maze = RandomMaze().make_maze(n_x, n_y)
        elif maze_type == 'Prim':
            self.maze = PrimMaze().make_maze(n_x, n_y)
        elif maze_type == 'Kruskal':
            self.maze = KruskalMaze().make_maze(n_x, n_y)
        elif maze_type == 'Recursive':
            self.maze = RecursiveDivisionMaze().make_maze(n_x, n_y)
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


if __name__ == "__main__":
    N = 8
    maze = Maze().make_maze(N, N, maze_type='Prim')
    print(maze)
