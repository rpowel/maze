import numpy as np
import random
from typing import List, Tuple

from .base import MazeBase


class DepthFirstMaze(MazeBase):
    def __init__(self):
        super().__init__()
        self.visited = set()
        self.stack = set()
        self.n_x = 0
        self.n_y = 0
        self.maze = None

    def make_maze(self, n_x: int, n_y: int) -> np.ndarray:
        self.n_x = n_x
        self.n_y = n_y
        self.maze = np.full([n_x, n_y], 1, dtype=int)

        start_i, start_j = self._pick_start_cell()
        self.maze[start_i, start_j] = 0
        self.visited.add((start_i, start_j))
        self.stack.add((start_i, start_j))

        num_iter = 0
        while len(self.stack) > 0 and num_iter < (n_x ** 2):
            self._logger.info(self.maze)
            num_iter += 1
            i, j = self.stack.pop()
            self._mark_visited(i, j)
            neighbors = self._get_unvisited_neighbors(i, j)
            if len(neighbors) == 0:
                continue
            self.stack.add((i, j))
            next_i, next_j = self._pick_random_neighbor(neighbors)
            mid_i = (i + next_i) // 2
            mid_j = (j + next_j) // 2
            self._mark_visited(mid_i, mid_j)
            self.stack.add((next_i, next_j))
            self._mark_visited(next_i, next_j)

        return self._prepare_final(self.maze)

    def _pick_start_cell(self) -> Tuple[int, int]:
        start_i = random.randint(0, self.n_x - 1)
        return start_i, 0

    def _mark_visited(self, i: int, j: int) -> None:
        self.visited.add((i, j))
        self.maze[i, j] = 0

    def _get_unvisited_neighbors(self, i: int, j: int) -> List[Tuple[int, int]]:
        neighbors = []
        if i >= 2:
            if not (i - 2, j) in self.visited:
                neighbors.append((i - 2, j))
        if i <= self.n_x - 3:
            if not (i + 2, j) in self.visited:
                neighbors.append((i + 2, j))
        if j >= 2:
            if not (i, j - 2) in self.visited:
                neighbors.append((i, j - 2))
        if j <= self.n_y - 3:
            if not (i, j + 2) in self.visited:
                neighbors.append((i, j + 2))
        return neighbors

    @staticmethod
    def _pick_random_neighbor(neighbors: List[Tuple[int, int]]) -> Tuple[int, int]:
        n = random.randint(0, len(neighbors) - 1)
        return neighbors[n]

    @staticmethod
    def _prepare_final(maze: np.ndarray) -> np.ndarray:
        maze_temp = np.ones([maze.shape[0] + 1, maze.shape[1] + 1], dtype=int)
        maze_temp[1:-1, 1:-1] = maze[:-1, :-1]
        return maze_temp
