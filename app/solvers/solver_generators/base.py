import abc

from common.logging import get_logger


class BaseMazeSolver(abc.ABC):
    """Abstract base for maze solver."""

    def __init__(self):
        self._logger = get_logger(class_=self)
