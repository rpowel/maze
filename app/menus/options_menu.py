import pygame
from typing import Callable, List, Tuple

from common.themes import THEME_LIST
from processors import OptionsProcessor, RestartProcessor
from .base import BaseMenu
from .menu_objects import Button, Selector


class OptionsMenu(BaseMenu):
    def __init__(self, window: pygame.Surface) -> None:
        super().__init__()
        self.window = window

        back_img = pygame.image.load("images/arrow-left.png").convert_alpha()
        self.back_button = Button(0.25, 0.9, back_img)

        self.theme_selector = Selector(0.5, 0.1, THEME_LIST, current_value=self._theme.name, title="Color Theme")
        self.changes = False

    def draw(self, event_list: List[pygame.event.Event]) -> Tuple[Callable, str]:
        action = ""
        menu = "options"

        if self.back_button.draw(self.window, event_list):
            self._logger.info("Back button clicked")
            if self.changes:
                action = RestartProcessor().process
            else:
                action = ""
            menu = "main"

        theme_change, theme_selection = self.theme_selector.draw(self.window, event_list)
        if theme_change:
            self.changes = True
            action = OptionsProcessor("display", "theme", theme_selection).process
            menu = "options"

        return action, menu
