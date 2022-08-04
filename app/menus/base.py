import abc
import pygame
from typing import Callable, List, Tuple, Type

from common.config import AppConfig
from common.logging import get_logger
from common.themes import THEME_MAP
from common.themes.base import BaseTheme


class BaseMenu(abc.ABC):
    """Base class for Menus."""

    def __init__(self):
        self._logger = get_logger(class_=self)
        self._config = AppConfig()
        self._theme: Type[BaseTheme] = THEME_MAP[self._config.get("display", "theme")]

    @abc.abstractmethod
    def draw(self, event_list: List[pygame.event.Event]) -> Tuple[Callable, str]:
        ...
