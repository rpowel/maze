"""Base class for maze generator."""
import abc

import numpy as np


class MazeBase(abc.ABC):
    """Abstract base for maze generator."""

    @staticmethod
    @abc.abstractmethod
    def _prepare_final(maze: np.ndarray) -> np.ndarray:
        ...

    @abc.abstractmethod
    def make_maze(self, n_x: int, n_y: int) -> np.ndarray:
        ...
