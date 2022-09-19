from typing import List, Generator

import numpy as np
import numpy.typing as npt

from .maze_generators import (
    MazeBase,
    DepthFirstMaze,
    KruskalMaze,
    PrimMaze,
    RecursiveDivisionMaze,
    RandomMaze,
    WilsonMaze,
)


class MazeTypes:
    DEPTH_FIRST = "depth first"
    KRUSKAL = "kruskal"
    PRIM = "prim"
    RANDOM = "random"
    RECURSIVE = "recursive"
    WILSON = "wilson"

    @classmethod
    def list(cls) -> List[str]:
        return [
            cls.DEPTH_FIRST,
            cls.KRUSKAL,
            cls.PRIM,
            cls.RECURSIVE,
            cls.WILSON,
        ]


class MazeFactory:
    def __init__(self, n_x: int, n_y: int, maze_type: str) -> None:
        self.n_x = n_x
        self.n_y = n_y
        self.maze_type = maze_type

    def process(self) -> Generator[npt.NDArray[np.int_], None, npt.NDArray[np.int_]]:
        generator: MazeBase
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
        elif self.maze_type == MazeTypes.WILSON:
            generator = WilsonMaze()
        else:
            raise NotImplementedError(f"{self.maze_type} not implemented")

        maze: npt.NDArray[np.int_] = np.zeros([self.n_x, self.n_y], dtype=int)
        for maze in generator.generate(self.n_x, self.n_y):
            yield maze

        return maze
