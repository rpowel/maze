import pygame
from typing import Callable, List, Tuple

from processors import ExitProcessor, OptionsProcessor
from .base import BaseMenu
from .menu_objects import Button, Selector


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

        self.maze_selector = Selector(0.5, 0.1, ["Prim", "Kruskal", "Recursive", "Random"])
        self.size_selector = Selector(0.5, 0.2, ["Small", "Medium", "Large"])

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
        type_change, maze_type = self.maze_selector.draw(self.window, event_list)
        if type_change:
            action = OptionsProcessor("maze", "TYPE", maze_type).process
            menu = "main"
        size_change, maze_size = self.size_selector.draw(self.window, event_list)
        if size_change:
            action = OptionsProcessor("maze", "size", maze_size).process
            menu = "main"

        return action, menu
