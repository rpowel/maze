import abc

from common.config import AppConfig
from common.logging import get_logger
from common.themes import BaseTheme, THEME_MAP


class BaseProcessor(abc.ABC):
    """Base class for processors."""

    def __init__(self):
        self._logger = get_logger(class_=self)
        self._config = AppConfig()
        self._theme: BaseTheme = THEME_MAP[self._config.get("display", "theme")]

    @abc.abstractmethod
    def process(self) -> None:
        ...
