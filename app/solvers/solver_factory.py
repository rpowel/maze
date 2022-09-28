from typing import Generator, List

import numpy.typing as npt
from numpy import int_, zeros

from .solver_generators import AStarSolver, DijkstraSolver


class SolverTypes:
    A_STAR = "a*"
    DIJKSTRA = "dijkstra"

    @classmethod
    def list(cls) -> List[str]:
        return [
            cls.A_STAR,
            cls.DIJKSTRA,
        ]


class SolverFactory:
    def __init__(self, solver_type: str) -> None:
        self.solver_type = solver_type

    def process(
        self, maze: npt.NDArray[int_]
    ) -> Generator[npt.NDArray[int_], None, npt.NDArray[int_]]:
        if self.solver_type == SolverTypes.A_STAR:
            generator = AStarSolver().solve(maze)
        elif self.solver_type == SolverTypes.DIJKSTRA:
            generator = DijkstraSolver().solve(maze)
        else:
            raise NotImplementedError(f"Maze solver {self.solver_type} not implmented")

        solution: npt.NDArray[int_] = zeros([], dtype=int)
        for solution in generator:
            yield solution
        return solution
