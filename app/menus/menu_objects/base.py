import abc
from typing import List, Tuple, Union

import pygame

from common.config import AppConfig
from common.logging import get_logger
from common.themes import BaseTheme, THEME_MAP


class BaseMenuObject(abc.ABC):
    """Base class for menu objects."""

    def __init__(self):
        self._logger = get_logger(class_=self)
        self._config = AppConfig()
        self._theme: BaseTheme = THEME_MAP[self._config.get("display", "theme")]

    @abc.abstractmethod
    def draw(
        self,
        surface: pygame.surface.Surface,
        event_list: List[pygame.event.Event],
    ) -> Union[None, bool, Tuple[bool, str]]:
        ...

    def _scale_image(
        self, image: pygame.surface.Surface, scale: float
    ) -> pygame.surface.Surface:
        """Scale images relative to window resolution."""
        window_width = int(self._config.get("display", "WINDOW_WIDTH"))
        ui_scale = int(self._config.get("display", "UI_SCALING")) / 100

        image_width = image.get_width()
        image_height = image.get_height()
        image_aspect_ratio = image_width / image_height

        scaled_image = pygame.transform.smoothscale(
            image,
            (
                int(window_width * scale * ui_scale),
                int(window_width * scale * ui_scale / image_aspect_ratio),
            ),
        )

        return scaled_image

    def _scale_abs_pos(self, x_rel_pos: float, y_rel_pos: float) -> Tuple[int, int]:
        """Get absolute item position from relative position."""
        window_width = int(self._config.get("display", "WINDOW_WIDTH"))
        window_height = int(self._config.get("display", "WINDOW_HEIGHT"))

        x_pos = int(window_width * x_rel_pos)
        y_pos = int(window_height * y_rel_pos)

        return x_pos, y_pos
