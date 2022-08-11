import pygame
from typing import Callable, List, Tuple

from common.path import get_resource_path
from common.themes import THEME_LIST
from processors import OptionsProcessor, RestartProcessor
from .base import BaseMenu
from .menu_objects import Button, Selector


class OptionsMenu(BaseMenu):
    def __init__(self, window: pygame.Surface) -> None:
        super().__init__()
        self.window = window

        self.theme_selector = Selector(
            0.5, 0.1, THEME_LIST, current_value=self._theme.name, title="Color Theme"
        )
        self.changes = False

        back_img = pygame.image.load(get_resource_path("images/arrow-left.png")).convert_alpha()
        self.back_button = Button(0.25, 0.9, back_img)

        reset_img = pygame.image.load(get_resource_path("images/recycle.png")).convert_alpha()
        self.reset_button = Button(0.75, 0.9, reset_img)

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

        theme_change, theme_selection = self.theme_selector.draw(
            self.window, event_list
        )
        if theme_change:
            self.changes = True
            action = OptionsProcessor("display", "theme", theme_selection).process

        if self.reset_button.draw(self.window, event_list):
            self._logger.info("reset button clicked")
            self.changes = True
            self._config.reset()

        return action, menu
