"""Base class for maze generator."""
import abc

import numpy as np

from common.logging import get_logger


class MazeBase(abc.ABC):
    """Abstract base for maze generator."""

    def __init__(self):
        self._logger = get_logger(class_=self)

    @staticmethod
    @abc.abstractmethod
    def _prepare_final(maze: np.ndarray) -> np.ndarray:
        ...

    @abc.abstractmethod
    def make_maze(self, n_x: int, n_y: int) -> np.ndarray:
        ...
