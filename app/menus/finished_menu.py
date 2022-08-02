import pygame
from typing import Callable, List, Tuple

from processors import ExitProcessor
from .base import BaseMenu
from .menu_objects import Button


class FinishedMenu(BaseMenu):
    def __init__(self, window: pygame.Surface) -> None:
        super().__init__()
        self.window = window

        back_img = pygame.image.load("images/leftarrow.png").convert_alpha()
        self.back_button = Button(0.25, 0.9, back_img)

        exit_img = pygame.image.load("images/exit.png")
        self.exit_button = Button(0.75, 0.9, exit_img)

    def draw(self, event_list: List[pygame.event.Event]) -> Tuple[Callable, str]:
        action = ""
        menu = "finished"

        if self.back_button.draw(self.window, event_list):
            self._logger.info("Start button clicked.")
            action = ""
            menu = "main"
        if self.exit_button.draw(self.window, event_list):
            self._logger.info("Exit button clicked.")
            action = ExitProcessor().process
            menu = ""

        return action, menu
