import pygame
from typing import Tuple

from .base import BaseProcessor


class DisplayProcessor(BaseProcessor):
    def __init__(self):
        super().__init__()
        self.window_width, self.window_height = self._get_screen_size()
        self.surface = self._init_display(self.window_width, self.window_height)

    def process(self) -> None:
        """Update display for new frame."""
        pygame.display.update()
        self._draw_background()

    def _get_screen_size(self) -> Tuple[int, int]:
        """Get display size from config as (`width`, `height`)."""
        width = int(self._config.get("display", "WINDOW_WIDTH"))
        height = int(self._config.get("display", "WINDOW_HEIGHT"))
        self._logger.info(f"Window width: {width}, height: {height}")
        return width, height

    def _init_display(self, px_x: int, px_y: int) -> pygame.Surface:
        """Initialize window/screen for display."""
        surface = pygame.display.set_mode((px_x, px_y))
        return surface

    def _draw_background(self):
        # image = pygame.image.load("images/landscape.jpg").convert_alpha()
        # image = pygame.transform.scale(image, (int(self.window_width), int(self.window_height)))
        color = pygame.Color(67, 70, 75)
        background = pygame.Surface(
            (self.window_width, self.window_height),
        )
        background.fill(color)

        self.surface.blit(background, (0, 0))
