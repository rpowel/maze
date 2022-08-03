import pygame
from typing import Callable, List, Tuple

from processors import OptionsProcessor
from .base import BaseMenu
from .menu_objects import Button, DropDown


class OptionsMenu(BaseMenu):
    def __init__(self, window: pygame.Surface) -> None:
        super().__init__()
        self.window = window

        back_img = pygame.image.load("images/arrow-left.png").convert_alpha()
        self.back_button = Button(0.25, 0.9, back_img)

        self.window_height_dropdown = DropDown(0.25, 0.25, "Window Height", ["400", "500"])

    def draw(self, event_list: List[pygame.event.Event]) -> Tuple[Callable, str]:
        action = ""
        menu = "options"

        if self.back_button.draw(self.window, event_list):
            self._logger.info("Back button clicked")
            action = ""
            menu = "main"

        selection = self.window_height_dropdown.draw(self.window, event_list)
        if selection:
            action = OptionsProcessor("display", "window_height", selection).process
            menu = "options"

        return action, menu
