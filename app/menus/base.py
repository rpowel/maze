import abc
from typing import Callable, List, Tuple, Union

import pygame

from common.config import AppConfig
from common.logging import get_logger
from common.themes import BaseTheme, THEME_MAP


class BaseMenu(abc.ABC):
    """Base class for Menus."""

    def __init__(self):
        self._logger = get_logger(class_=self)
        self._config = AppConfig()
        self._theme: BaseTheme = THEME_MAP[self._config.get("display", "theme")]

    @abc.abstractmethod
    def draw(
        self, event_list: List[pygame.event.Event]
    ) -> Tuple[Union[None, Callable[[], None]], str]:
        ...
