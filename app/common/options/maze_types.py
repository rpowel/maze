from typing import Dict, List, Type

from mazes.base import MazeBase
from mazes import RandomMaze, PrimMaze, KruskalMaze, RecursiveDivisionMaze


class MazeTypes:
    KRUSKAL = "kruskal"
    PRIM = "prim"
    RANDOM = "random"
    RECURSIVE = "recursive"

    @classmethod
    def list(cls) -> List[str]:
        return [
            cls.KRUSKAL,
            cls.PRIM,
            cls.RANDOM,
            cls.RECURSIVE,
        ]

    @classmethod
    def map(cls) -> Dict[str, Type[MazeBase]]:
        return {
            cls.KRUSKAL: KruskalMaze,
            cls.PRIM: PrimMaze,
            cls.RANDOM: RandomMaze,
            cls.RECURSIVE: RecursiveDivisionMaze,
        }
