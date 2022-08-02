import abc

from common.config import AppConfig
from common.logging import get_logger


class BaseProcessor(abc.ABC):
    """Base class for processors."""
    def __init__(self):
        self._logger = get_logger(class_=self)
        self._config = AppConfig()

    @abc.abstractmethod
    def process(self) -> None:
        ...
