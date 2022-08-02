import abc
import pygame
from typing import Callable, List, Tuple

from common.config import AppConfig
from common.logging import get_logger


class BaseMenu(abc.ABC):
    """Base class for Menus."""

    def __init__(self):
        print(self.__class__.__name__)
        self._logger = get_logger(class_=self)
        self._config = AppConfig()

    @abc.abstractmethod
    def draw(self, event_list: List[pygame.event.Event]) -> Tuple[Callable, str]:
        ...
