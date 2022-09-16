from typing import Callable, List, Tuple

import pygame

from common.path import get_resource_path
from orm import Scores
from processors import ExitProcessor
from .base import BaseMenu
from .menu_objects import Button, Table


class FinishedMenu(BaseMenu):
    def __init__(self, window: pygame.Surface) -> None:
        super().__init__()
        self.window = window

        back_img = pygame.image.load(
            get_resource_path("images/arrow-left.png")
        ).convert_alpha()
        self.back_button = Button(0.25, 0.9, back_img)

        exit_img = pygame.image.load(
            get_resource_path("images/exit.png")
        ).convert_alpha()
        self.exit_button = Button(0.75, 0.9, exit_img)
        self.score_ticks = 0
        self.tick_rate = 30

        self.title_rect = pygame.Rect(
            self.window.get_rect().right * 0.5 - 50, 0, 100, 100
        )
        self.time_rect = pygame.Rect(
            self.window.get_rect().right * 0.5 - 50, 50, 100, 100
        )
        self.type_rect = pygame.Rect(
            self.window.get_rect().right * 0.5 - 50, 100, 100, 100
        )
        self.size_x_rect = pygame.Rect(
            self.window.get_rect().right * 0.5 - 50, 150, 100, 100
        )
        self.size_y_rect = pygame.Rect(
            self.window.get_rect().right * 0.5 - 50, 200, 100, 100
        )

    def draw(self, event_list: List[pygame.event.Event]) -> Tuple[Callable, str]:
        action = ""
        menu = "finished"
        time_seconds = (self.score_ticks // self.tick_rate) % 60
        time_minutes = (self.score_ticks // self.tick_rate) // 60

        title = "Maze Finished!"
        time = f"Time: {str(time_minutes).zfill(2)}:{str(time_seconds).zfill(2)}"
        maze_type = f"Type: {self._config.get('maze', 'type')}"
        maze_size_x = f"X Size: {self._config.get('maze', 'size_x')} Cells"
        maze_size_y = f"Y Size: {self._config.get('maze', 'size_y')} Cells"

        title_msg = self._theme.header_font.render(
            title,
            True,
            self._theme.text_color,
        )
        time_msg = self._theme.header_font.render(
            time,
            True,
            self._theme.text_color,
        )
        type_msg = self._theme.header_font.render(
            maze_type.title(),
            True,
            self._theme.text_color,
        )
        size_x_msg = self._theme.header_font.render(
            maze_size_x,
            True,
            self._theme.text_color,
        )
        size_y_msg = self._theme.header_font.render(
            maze_size_y,
            True,
            self._theme.text_color,
        )

        self.window.blit(title_msg, title_msg.get_rect(center=self.title_rect.center))
        self.window.blit(time_msg, time_msg.get_rect(center=self.time_rect.center))
        self.window.blit(type_msg, type_msg.get_rect(center=self.type_rect.center))
        self.window.blit(
            size_x_msg,
            size_x_msg.get_rect(center=self.size_x_rect.center),
        )
        self.window.blit(
            size_y_msg,
            size_y_msg.get_rect(center=self.size_y_rect.center),
        )

        if self.back_button.draw(self.window, event_list):
            self._logger.info("Start button clicked.")
            action = ""
            menu = "main"
        if self.exit_button.draw(self.window, event_list):
            self._logger.info("Exit button clicked.")
            action = ExitProcessor().process
            menu = ""

        data = Scores.top_n_scores(
            maze_type=self._config.get("maze", "type"),
            size_x=self._config.get("maze", "size_x"),
            size_y=self._config.get("maze", "size_y"),
            num_limit=5,
        )
        headers = ["Type", "Size X", "Size Y", "Time", "Date Finished"]
        score_table = Table("High Scores", 0.05, 0.5, headers, data)
        score_table.draw(self.window, event_list)

        return action, menu
