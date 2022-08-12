from typing import Sequence, List, Tuple, Callable

import numpy as np
import pygame

from common.options import ShowMazeGeneration
from mazes import MazeFactory
from processors import FinishProcessor
from .base import BaseMenu
from .menu_objects import Button, MazeSquare


class MazeMenu(BaseMenu):
    def __init__(self, window: pygame.Surface) -> None:
        super().__init__()
        self.window = window
        self.maze: np.ndarray = None
        self.maze_buttons: Sequence[MazeSquare] = None
        self.square_size: int = None
        self.num_active: int = 0
        self.buffer = 10  # 10px
        self.buffer_ = 10

        self.maze_type = None
        self.grid_size_x = None
        self.grid_size_y = None
        self.show_generation = None
        self.maze_generator = None
        self.finished_generating = False

        self.score_ticks = 0
        self.tick_rate = 30

        back_img = pygame.image.load("images/arrow-left.png").convert_alpha()
        self.back_button = Button(0.25, 0.9, back_img)

        self.time_rect = pygame.Rect(
            self.window.get_rect().right - 150,
            self.window.get_rect().bottom - 100,
            100,
            100,
        )

    def init_maze(self) -> None:
        self.maze_type = self._config.get("maze", "type").lower()
        self.grid_size_x = int(self._config.get("maze", "size_x"))
        self.grid_size_y = int(self._config.get("maze", "size_y"))
        self.show_generation = self._config.get("maze", "show_generation") == ShowMazeGeneration.TRUE
        self._logger.info(f"Initializing maze. Type: {self.maze_type}, Size: {self.grid_size_x}x{self.grid_size_y}")

        self._get_sqare_size(max(self.grid_size_x, self.grid_size_y))
        self.maze_generator = None
        self._generate_maze()

        self.maze_buttons = np.empty(self.maze.shape, dtype=MazeSquare)
        for i in range(self.maze.shape[0]):
            for j in range(self.maze.shape[1]):
                self.maze_buttons[i, j] = MazeSquare(self.maze[i, j], self._get_rect(i, j))

    def draw(self, event_list: List[pygame.event.Event]) -> Tuple[Callable, str]:
        self.score_ticks += 1
        if self.back_button.draw(self.window, event_list):
            self.finished_generating = True
            return "", "main"

        self._generate_maze()

        time_seconds = (self.score_ticks // self.tick_rate) % 60
        time_minutes = (self.score_ticks // self.tick_rate) // 60
        time = f"{str(time_minutes).zfill(2)}:{str(time_seconds).zfill(2)}"
        time_msg = self._theme.normal_font.render(time, True, self._theme.text_color)
        self.window.blit(time_msg, time_msg.get_rect(center=self.time_rect.center))

        for i in range(self.maze.shape[0]):
            for j in range(self.maze.shape[1]):
                rect = self._get_rect(i, j)
                pygame.draw.rect(
                    self.window,
                    self._decide_color(maze_val=self.maze[i, j]),
                    rect,
                )

                if self.maze_buttons[i, j].draw(None, None):
                    if self._check_click(i, j):
                        self.maze[i, j] = 4
                        self.maze_buttons[i, j].maze_val = 4
                        self.num_active += 1

        if self._check_finished():
            self._logger.info("Maze finished")
            processor = FinishProcessor(
                maze_type=self.maze_type,
                size_x=self.grid_size_x,
                size_y=self.grid_size_y,
                time_seconds=(self.score_ticks // self.tick_rate),
            ).process
            return processor, "finished"

        return "", "maze"

    def _decide_color(self, maze_val: int) -> pygame.Color:
        if maze_val == 0:
            return self._theme.hall_color
        if maze_val == 1:
            return self._theme.wall_color
        if maze_val == 2:
            return self._theme.start_color
        if maze_val == 3:
            return self._theme.end_color
        if maze_val == 4:
            return self._theme.path_color

    def _get_sqare_size(self, num_cols: int) -> None:
        self.buffer = self.buffer_
        window_width = self.window.get_width()
        usable_display_size = (window_width - self.buffer * 2)
        self.square_size = usable_display_size // (num_cols + 2)

        self.buffer = (window_width - (self.square_size * (num_cols + 2))) / 2

    def _get_rect(self, i: int, j: int) -> pygame.Rect:
        rect = pygame.Rect(
            (i * self.square_size + self.buffer, j * self.square_size + self.buffer),
            (self.square_size, self.square_size),
        )
        rect.topleft = (i * self.square_size + self.buffer, j * self.square_size + self.buffer)
        return rect

    def _check_click(self, i: int, j: int) -> bool:
        if self.maze[i, j] != 0:
            return False
        if not (
            self.maze[i + 1, j] in (2, 4)
            or self.maze[i - 1, j] in (2, 4)
            or self.maze[i, j + 1] in (2, 4)
            or self.maze[i, j - 1] in (2, 4)
        ):
            return False
        return True

    def _check_finished(self) -> bool:
        if not self.finished_generating:
            return False
        elif self.num_active < 2:
            return False
        i, j = np.where(self.maze == 3)
        i = i[0]
        j = j[0]

        if not self.maze[i - 1, j]:
            return False
        return True

    def _generate_maze(self):
        if not self.maze_generator:
            self.maze_generator = MazeFactory(self.grid_size_x, self.grid_size_y, maze_type=self.maze_type).process()
            self.finished_generating = False
            self.num_active = 0
        if not self.finished_generating:
            if self.show_generation:
                try:
                    self.maze = next(self.maze_generator).T
                    self.score_ticks = 0
                except StopIteration as stop:
                    self.finished_generating = True
                    self.maze = stop.value.T
                    self.score_ticks = 0
            else:
                self.maze = [step for step in self.maze_generator][-1].T
                self.score_ticks = 0
                self.finished_generating = True
