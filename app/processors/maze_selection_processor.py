from random import randint
from typing import Type

import numpy as np

from common.options import MazeTypes
from mazes.base import MazeBase
from .base import BaseProcessor


class MazeSelectionProcessor(BaseProcessor):
    def __init__(self, n_x: int, n_y: int, maze_type: str = MazeTypes.PRIM) -> None:
        super().__init__()
        self.n_x = n_x
        self.n_y = n_y
        self.maze_type = maze_type

    def process(self) -> np.ndarray:
        maze_class = MazeTypes.map()[self.maze_type]

        maze = self._make_check_maze(self.n_x, self.n_y, maze_class)

        return maze

    def _make_check_maze(self, n_x: int, n_y: int, maze_class: Type[MazeBase]) -> np.ndarray:
        maze = maze_class().make_maze(n_x, n_y)
        maze = self._set_entrance(maze)
        maze = self._set_exit(maze)
        while not self.check_percolation(maze):
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

    import numpy as np

    def check_percolation(self, maze: np.ndarray) -> bool:
        """Check if maze path goes from entrance to exit."""
        maze = np.where(maze > 1, 0, maze)
        maze = 1 - maze
        ghost = np.zeros([maze.shape[0] + 2, maze.shape[1] + 2], dtype=int)
        ghost[1:-1, 1:-1] = maze
        coords, ids = self._find_clusters(ghost)
        check = self._is_percolation(coords, ids, maze.shape[1])
        return check

    @staticmethod
    def _find_clusters(grid):
        """
        Find individual clusters (i.e. neighboring occupied cells) by iterating
        through the grid and reassigning cells' labels accordingly to their
        belonging to the same (or not) cluster

        returns:
            ids: final np.array of IDs
        """

        num_of_ones = np.count_nonzero(grid)

        # 1-D array of labels (IDs) of each occupied cell. At the beginning,
        # all labels are different and are simply counted like 0,1,2,3,...
        ids = np.arange(num_of_ones)
        # 2-D array that storing (y,x) coordinates of occupied cells
        coords = [list(x) for x in np.argwhere(grid > 0)]

        while True:
            cw = []

            for i in np.arange(ids.size):
                # extract coordinates of an i-th current cell
                y, x = coords[i]

                # If only one neighbor is occupied, we change a label of the
                # current cell to the label of that neighbor. First, we need to
                # find ID of this neighbor by its known coordinates
                if grid[y - 1][x] == 1 and grid[y][x - 1] == 0:
                    ids[i] = ids[coords.index([y - 1, x])]
                elif grid[y][x - 1] == 1 and grid[y - 1][x] == 0:
                    ids[i] = ids[coords.index([y, x - 1])]

                # if both neighbors are occupied then we assign a smaller label
                elif grid[y - 1][x] == 1 and grid[y][x - 1] == 1:
                    first_neighbor_id = ids[coords.index([y - 1, x])]
                    second_neighbor_id = ids[coords.index([y, x - 1])]
                    ids[i] = np.min([first_neighbor_id, second_neighbor_id])

                    # if IDs are unequal then we store them to correct later
                    if first_neighbor_id != second_neighbor_id:
                        cw.append([first_neighbor_id, second_neighbor_id])

            # quit the loop if there are no more wrong labels
            if not cw:
                break
            # else correct labels
            else:
                for id1, id2 in cw:
                    wrong_id = np.max([id1, id2])
                    correct_id = np.min([id1, id2])
                    ids[ids == wrong_id] = correct_id

        return coords, ids

    @staticmethod
    def _is_percolation(coords, ids, grid_x_dimension):
        """
        Define whether there is a percolation in the given grid and what its type.
        Correctly works only if find_clusters() function were called before
        """
        clusters_coordinates = []
        for idx in np.unique(ids):
            clusters_coordinates.append(
                [coords[k] for k in range(len(ids)) if ids[k] == idx]
            )

        # search for percolated cluster(s)
        for cluster in clusters_coordinates:
            cluster = np.array(cluster).T
            if (1 in cluster[1]) and (grid_x_dimension in cluster[1]):
                return True
        return False
