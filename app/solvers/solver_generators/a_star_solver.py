from operator import attrgetter
from typing import List, Generator, Set, Tuple, Union

import numpy as np
import numpy.typing as npt

from .base import BaseMazeSolver


class AStarSolver(BaseMazeSolver):
    def solve(
        self,
        maze: npt.NDArray[np.int_],
    ) -> Generator[npt.NDArray[np.int_], None, npt.NDArray[np.int_]]:
        self._logger.info("Starting A* Maze Solver")

        solution = np.copy(maze)

        start_cell = self._get_start_cell(maze)
        end_cell = self._get_end_cell(maze)

        current_node = AStarNode(None, start_cell, end_cell)
        open_nodes = {current_node}
        closed_nodes = set()

        while open_nodes:
            current_node = min(open_nodes, key=attrgetter("f"))
            solution[current_node.cell] = 5
            closed_nodes.add(current_node)
            open_nodes.remove(current_node)

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

    @staticmethod
    def _get_start_cell(maze: npt.NDArray[np.int_]) -> Tuple[int, int]:
        enter = np.where(maze == 2)
        return int(enter[0]), int(enter[1] + 1)

    @staticmethod
    def _get_end_cell(maze: npt.NDArray[np.int_]) -> Tuple[int, int]:
        exit_ = np.where(maze == 3)
        return int(exit_[0]), int(exit_[1] - 1)

    @staticmethod
    def _get_valid_neighbors(
        maze: npt.NDArray[np.int_],
        current_node: "AStarNode",
        closed_nodes: Set["AStarNode"],
    ) -> Set["AStarNode"]:
        neighbors = set()
        i, j = current_node.cell
        closed_cells = [node.cell for node in closed_nodes]
        end_cell = current_node.end_cell
        if (maze[i + 1, j] == 0) and (not (i + 1, j) in closed_cells):
            neighbors.add(AStarNode(current_node, (i + 1, j), end_cell))
        if (maze[i - 1, j] == 0) and (not (i - 1, j) in closed_cells):
            neighbors.add(AStarNode(current_node, (i - 1, j), end_cell))
        if (maze[i, j + 1] == 0) and (not (i, j + 1) in closed_cells):
            neighbors.add(AStarNode(current_node, (i, j + 1), end_cell))
        if (maze[i, j - 1] == 0) and (not (i, j - 1) in closed_cells):
            neighbors.add(AStarNode(current_node, (i, j - 1), end_cell))
        return neighbors

    @staticmethod
    def _optimize_open_nodes(open_nodes: Set["AStarNode"]) -> Set["AStarNode"]:
        optimal_nodes = open_nodes.copy()
        overlap_ij: List[Tuple["AStarNode", "AStarNode"]] = []
        for i, node_i in enumerate(open_nodes):
            for j, node_j in enumerate(open_nodes):
                if node_i == node_j:
                    continue
                if node_i.cell == node_j.cell:
                    overlap_ij.append((node_i, node_j))

        for node_i, node_j in overlap_ij:
            worse_node = max((node_i, node_j), key=attrgetter("g"))
            if worse_node in optimal_nodes:
                optimal_nodes.remove(worse_node)
        return optimal_nodes

    @staticmethod
    def _check_for_end(
        closed_nodes: Set["AStarNode"], end_cell: Tuple[int, int]
    ) -> bool:
        for node in closed_nodes:
            if node.cell == end_cell:
                return True
        return False


class AStarNode:
    def __init__(
        self,
        parent: Union["AStarNode", None],
        cell: Tuple[int, int],
        end_cell: Tuple[int, int],
    ) -> None:
        self.parent = parent
        self.cell = cell
        self.end_cell = end_cell

    @property
    def g(self) -> int:
        if self.parent:
            return self.parent.g + 1
        else:
            return 0

    @property
    def h(self) -> int:
        i_diff = self.end_cell[0] - self.cell[0]
        j_diff = self.end_cell[1] - self.cell[1]
        return i_diff ** 2 + j_diff ** 2

    @property
    def f(self) -> int:
        return self.g + self.h
