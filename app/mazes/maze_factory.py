from typing import List

import numpy as np

from .maze_generators import (
    DepthFirstMaze,
    KruskalMaze,
    PrimMaze,
    RecursiveDivisionMaze,
    RandomMaze,
)


class MazeTypes:
    DEPTH_FIRST = "depth first"
    KRUSKAL = "kruskal"
    PRIM = "prim"
    RANDOM = "random"
    RECURSIVE = "recursive"

    @classmethod
    def list(cls) -> List[str]:
        return [
            cls.DEPTH_FIRST,
            cls.KRUSKAL,
            cls.PRIM,
            cls.RECURSIVE,
        ]


class MazeFactory:
    def __init__(self, n_x: int, n_y: int, maze_type: str) -> None:
        self.n_x = n_x
        self.n_y = n_y
        self.maze_type = maze_type

    def process(self) -> np.ndarray:
        if self.maze_type == MazeTypes.DEPTH_FIRST:
            generator = DepthFirstMaze()
        elif self.maze_type == MazeTypes.KRUSKAL:
            generator = KruskalMaze()
        elif self.maze_type == MazeTypes.PRIM:
            generator = PrimMaze()
        elif self.maze_type == MazeTypes.RANDOM:
            generator = RandomMaze()
        elif self.maze_type == MazeTypes.RECURSIVE:
            generator = RecursiveDivisionMaze()
        else:
            raise NotImplementedError(f"{self.maze_type} not implemented")

        maze_step = None
        for maze in generator.generate(self.n_x, self.n_y):
            maze_step = maze
            yield maze_step

        return maze_step
