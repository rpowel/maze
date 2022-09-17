from typing import Callable, List, Tuple, Union

import pygame

from common.options import MazeSizes
from common.path import get_resource_path
from mazes.maze_factory import MazeTypes
from processors import ExitProcessor, OptionsProcessor
from .base import BaseMenu
from .menu_objects import Button, Selector


class MainMenu(BaseMenu):
    def __init__(self, window: pygame.surface.Surface) -> None:
        super().__init__()
        self.window = window

        start_img = pygame.image.load(
            get_resource_path("images/play.png")
        ).convert_alpha()
        self.start_button = Button(0.25, 0.9, start_img)

        options_img = pygame.image.load(
            get_resource_path("images/menu.png")
        ).convert_alpha()
        self.option_button = Button(0.5, 0.9, options_img)

        exit_img = pygame.image.load(
            get_resource_path("images/exit.png")
        ).convert_alpha()
        self.exit_button = Button(0.75, 0.9, exit_img)

        self.maze_selector = Selector(
            0.5,
            0.1,
            MazeTypes.list(),
            self._config.get("maze", "type"),
            title="Maze Type",
        )
        self.size_x_selector = Selector(
            0.3,
            0.25,
            MazeSizes.list(),
            self._config.get("maze", "size_x"),
            title="Maze Size X",
        )
        self.size_y_selector = Selector(
            0.7,
            0.25,
            MazeSizes.list(),
            self._config.get("maze", "size_y"),
            title="Maze Size Y",
        )

    def draw(
        self, event_list: List[pygame.event.Event]
    ) -> Tuple[Union[None, Callable[[], None]], str]:
        action = None
        menu = "main"

        if self.start_button.draw(self.window, event_list):
            self._logger.info("Start button clicked.")
            action = None
            menu = "maze"
        if self.option_button.draw(self.window, event_list):
            self._logger.info("Options button clicked.")
            action = None
            menu = "options"
        if self.exit_button.draw(self.window, event_list):
            self._logger.info("Exit button clicked.")
            action = ExitProcessor().process
            menu = ""
        type_change, maze_type = self.maze_selector.draw(self.window, event_list)
        if type_change:
            action = OptionsProcessor("maze", "type", maze_type).process
            menu = "main"
        size_change, maze_size = self.size_x_selector.draw(self.window, event_list)
        if size_change:
            action = OptionsProcessor("maze", "size_x", maze_size).process
            menu = "main"
        size_change, maze_size = self.size_y_selector.draw(self.window, event_list)
        if size_change:
            action = OptionsProcessor("maze", "size_y", maze_size).process
            menu = "main"

        return action, menu
