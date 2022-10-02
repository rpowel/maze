from typing import List, Tuple, Callable, Union, Generator

import numpy as np
import numpy.typing as npt
import pygame

from common.options import ShowMazeGeneration
from common.path import get_resource_path
from mazes import MazeFactory
from processors import FinishProcessor
from solvers import SolverFactory
from .base import BaseMenu
from .menu_objects import Button, MazeSquare


class MazeMenu(BaseMenu):
    def __init__(self, window: pygame.surface.Surface) -> None:
        super().__init__()
        self.window: pygame.surface.Surface = window
        self.maze: npt.NDArray[np.int_] = np.array([])
        self.maze_buttons: npt.NDArray[np.int_] = np.array([])
        self.square_size: int = 0
        self.num_active: int = 0
        self.buffer = 10  # 10px
        self.buffer_ = 10

        self.maze_type: str = ""
        self.grid_size_x: int = 0
        self.grid_size_y: int = 0
        self.show_generation: bool = (
            self._config.get("maze", "show_generation") == ShowMazeGeneration.TRUE
        )
        self.maze_generator: Union[
            None, Generator[npt.NDArray[np.int_], None, npt.NDArray[np.int_]]
        ] = None
        self.finished_generating: bool = False

        self.solver_type: str = ""
        self.solver_generator: Union[
            None, Generator[npt.NDArray[np.int_], None, npt.NDArray[np.int_]]
        ] = None
        self.solve = False
        self.finished_solving: bool = False

        self.score_ticks: int = 0
        self.tick_rate: int = 30

        back_img = pygame.image.load(
            get_resource_path("images/arrow-left.png")
        ).convert_alpha()
        self.back_button = Button(0.25, 0.9, back_img)

        solver_img = pygame.image.load(
            get_resource_path("images/solution.png")
        ).convert_alpha()
        self.solve_button = Button(0.5, 0.9, solver_img)

        self.time_rect = pygame.Rect(
            self.window.get_rect().right - 150,
            self.window.get_rect().bottom - 100,
            100,
            100,
        )

    def init_maze(self) -> None:
        self.maze_type = self._config.get("maze", "type").lower()
        self.solver_type = self._config.get("maze", "solver").lower()
        self.grid_size_x = int(self._config.get("maze", "size_x"))
        self.grid_size_y = int(self._config.get("maze", "size_y"))
        self.show_generation = (
            self._config.get("maze", "show_generation") == ShowMazeGeneration.TRUE
        )
        self._logger.info(
            f"Initializing maze. Type: {self.maze_type}, "
            + f"Size: {self.grid_size_x}x{self.grid_size_y}"
        )

        self._get_sqare_size(max((self.grid_size_x, self.grid_size_y)))

        self.maze_generator = None
        self.finished_generating = False

        self.solver_generator = None
        self.solve = False
        self.finished_solving = False

        self._generate_maze()

        self.maze_buttons = np.empty(self.maze.shape, dtype=MazeSquare)
        for i in range(self.maze.shape[0]):
            for j in range(self.maze.shape[1]):
                self.maze_buttons[i, j] = MazeSquare(
                    self.maze[i, j], self._get_rect(i, j)
                )

    def draw(
        self, event_list: List[pygame.event.Event]
    ) -> Tuple[Union[None, Callable[[], None]], str]:
        self.score_ticks += 1
        if self.back_button.draw(self.window, event_list):
            self.finished_generating = True
            self.finished_solving = True
            return None, "main"

        if self.finished_generating and not self.finished_solving:
            if self.solve_button.draw(self.window, event_list):
                self.solve = True

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

        return None, "maze"

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
        if maze_val == 5:
            return self._theme.solution_search_color
        if maze_val == 6:
            return self._theme.solution_path_color
        else:
            raise ValueError(f"No color for maze square value, {maze_val=}")

    def _get_sqare_size(self, num_cols: int) -> None:
        self.buffer = self.buffer_
        window_width = self.window.get_width()
        usable_display_size = window_width - self.buffer * 2
        self.square_size = usable_display_size // (num_cols + 2)

        self.buffer = (window_width - (self.square_size * (num_cols + 2))) // 2

    def _get_rect(self, i: int, j: int) -> pygame.Rect:
        rect = pygame.Rect(
            (i * self.square_size + self.buffer, j * self.square_size + self.buffer),
            (self.square_size, self.square_size),
        )
        rect.topleft = (
            i * self.square_size + self.buffer,
            j * self.square_size + self.buffer,
        )
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

    def _generate_maze(self) -> None:
        if not self.maze_generator:
            self.maze_generator = MazeFactory(
                self.grid_size_x,
                self.grid_size_y,
                maze_type=self.maze_type,
            ).process()
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

        elif self.solve and (not self.finished_solving):
            if not self.solver_generator:
                self.solver_generator = SolverFactory(
                    solver_type=self.solver_type,
                ).process(self.maze.T)
                self.finished_solving = False
            try:
                self.maze = next(self.solver_generator).T
            except StopIteration as stop:
                self.finished_solving = True
                self.maze = stop.value.T
