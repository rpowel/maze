import pygame
from typing import Callable, List, Tuple

from processors import ExitProcessor
from .base import BaseMenu
from .menu_objects import Button


class MainMenu(BaseMenu):
    def __init__(self, window: pygame.Surface) -> None:
        super().__init__()
        self.window = window

        start_img = pygame.image.load("images/play.png").convert_alpha()
        self.start_button = Button(0.25, 0.9, start_img)

        options_img = pygame.image.load("images/menu.png").convert_alpha()
        self.option_button = Button(0.5, 0.9, options_img)

        exit_img = pygame.image.load("images/exit.png")
        self.exit_button = Button(0.75, 0.9, exit_img)

    def draw(self, event_list: List[pygame.event.Event]) -> Tuple[Callable, str]:
        action = ""
        menu = "main"

        if self.start_button.draw(self.window, event_list):
            self._logger.info("Start button clicked.")
            action = ""
            menu = "maze"
        if self.option_button.draw(self.window, event_list):
            self._logger.info("Options button clicked.")
            action = ""
            menu = "options"
        if self.exit_button.draw(self.window, event_list):
            self._logger.info("Exit button clicked.")
            action = ExitProcessor().process
            menu = ""

        return action, menu
