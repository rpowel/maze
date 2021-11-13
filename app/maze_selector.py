#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 10:44:44 2020.

@author: powel
"""
import random
from random import randint

import numpy as np

from mazes import RandomMaze, PrimMaze, KruskalMaze, RecursiveDivisionMaze, MazeBase
from percolation import check_percolation


class Maze:
    def __init__(self):
        self.maze = None

    def make_maze(self, n_x: int, n_y: int, maze_type: str = 'Prim') -> np.ndarray:
        if maze_type == 'Random':
            maze_class = RandomMaze
        elif maze_type == 'Prim':
            maze_class = PrimMaze
        elif maze_type == 'Kruskal':
            maze_class = KruskalMaze
        elif maze_type == 'Recursive':
            maze_class = RecursiveDivisionMaze
        else:
            raise ValueError("Invalid maze_type")

        maze = self._make_check_maze(n_x, n_y, maze_class)

        return maze

    def _make_check_maze(self, n_x: int, n_y: int, maze_class: MazeBase) -> np.ndarray:
        maze = maze_class().make_maze(n_x, n_y)
        maze = self._set_entrance(maze)
        maze = self._set_exit(maze)
        while not check_percolation(maze):
            maze = maze_class().make_maze(n_x, n_y)
            maze = self._set_entrance(maze)
            maze = self._set_exit(maze)
        return maze

    @staticmethod
    def _set_entrance(maze: np.ndarray) -> np.ndarray:
        while True:
            x, y = randint(1, maze.shape[0] - 1), 0
            if maze[x, y + 1] == 0:
                break
        maze[x, y] = 2
        return maze

    @staticmethod
    def _set_exit(maze: np.ndarray) -> np.ndarray:
        while True:
            x, y = randint(1, maze.shape[0] - 1), maze.shape[1] - 1
            if maze[x, y - 1] == 0:
                break
        maze[x, y] = 3
        return maze


if __name__ == "__main__":
    random.seed(1)
    N = 10
    maze = Maze().make_maze(N, N, maze_type='Recursive')
    print(maze.__repr__())
