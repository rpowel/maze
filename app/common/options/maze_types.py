from typing import Dict, List, Type

from mazes.base import MazeBase
from mazes import DepthFirstMaze, RandomMaze, PrimMaze, KruskalMaze, RecursiveDivisionMaze


class MazeTypes:
    KRUSKAL = "kruskal"
    PRIM = "prim"
    RANDOM = "random"
    RECURSIVE = "recursive"
    DEPTH_FIRST = "depth first"

    @classmethod
    def list(cls) -> List[str]:
        return [
            cls.KRUSKAL,
            cls.PRIM,
            cls.RANDOM,
            cls.RECURSIVE,
            cls.DEPTH_FIRST,
        ]

    @classmethod
    def map(cls) -> Dict[str, Type[MazeBase]]:
        return {
            cls.KRUSKAL: KruskalMaze,
            cls.PRIM: PrimMaze,
            cls.RANDOM: RandomMaze,
            cls.RECURSIVE: RecursiveDivisionMaze,
            cls.DEPTH_FIRST: DepthFirstMaze,
        }
