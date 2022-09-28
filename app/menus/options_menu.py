from typing import Callable, List, Tuple, Union

import pygame

from common.options import ShowMazeGeneration
from common.path import get_resource_path
from common.themes import THEME_LIST
from processors import OptionsProcessor, RestartProcessor
from .base import BaseMenu
from .menu_objects import Button, Selector


class OptionsMenu(BaseMenu):
    def __init__(self, window: pygame.surface.Surface) -> None:
        super().__init__()
        self.window = window

        self.theme_selector = Selector(
            0.5, 0.1, THEME_LIST, current_value=self._theme.name, title="Color Theme"
        )
        self.show_gen_selector = Selector(
            0.5,
            0.25,
            ShowMazeGeneration.list(),
            current_value=self._config.get("maze", "show_generation"),
            title="Show Maze Generation",
        )
        self.changes = False

        back_img = pygame.image.load(get_resource_path("images/arrow-left.png"))
        self.back_button = Button(0.25, 0.9, back_img)

        reset_img = pygame.image.load(
            get_resource_path("images/recycle.png")
        ).convert_alpha()
        self.reset_button = Button(0.75, 0.9, reset_img)

    def draw(
        self, event_list: List[pygame.event.Event]
    ) -> Tuple[Union[None, Callable[[], None]], str]:
        action = None
        menu = "options"

        if self.back_button.draw(self.window, event_list):
            self._logger.info("Back button clicked")
            if self.changes:
                action = RestartProcessor().process
            else:
                action = None
            menu = "main"

        theme_change, theme_selection = self.theme_selector.draw(
            self.window, event_list
        )
        if theme_change:
            self.changes = True
            action = OptionsProcessor("display", "theme", theme_selection).process

        show_gen_change, show_gen_selection = self.show_gen_selector.draw(
            self.window,
            event_list,
        )
        if show_gen_change:
            action = OptionsProcessor(
                "maze",
                "show_generation",
                show_gen_selection,
            ).process

        if self.reset_button.draw(self.window, event_list):
            self._logger.info("reset button clicked")
            self._config.reset()
            action = RestartProcessor().process
            menu = "main"

        return action, menu
