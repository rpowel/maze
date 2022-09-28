from typing import Generator

import numpy as np
from numpy import typing as npt

from .base import BaseMazeSolver, SolverNode


class DijkstraSolver(BaseMazeSolver):
    def solve(
        self, maze: npt.NDArray[np.int_]
    ) -> Generator[npt.NDArray[np.int_], None, npt.NDArray[np.int_]]:

        solution = np.copy(maze)
        start_cell = self._get_start_cell(maze)
        end_cell = self._get_end_cell(maze)

        current_node = SolverNode(None, start_cell, end_cell)
        open_nodes = {current_node}
        closed_nodes = set()

        while open_nodes:
            current_node = open_nodes.pop()
            closed_nodes.add(current_node)
            solution[current_node.cell] = 5

            available_neighbors = self._get_valid_neighbors(
                maze, current_node, closed_nodes
            )
            for neighbor in available_neighbors:
                open_nodes.add(neighbor)
            open_nodes = self._optimize_open_nodes(open_nodes)
            if self._check_for_end(closed_nodes, end_cell):
                break
            yield solution

        while current_node:
            solution[current_node.cell] = 6
            yield solution
            if not current_node.parent:
                break
            current_node = current_node.parent
        return solution
