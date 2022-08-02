from typing import Sequence, List, Tuple, Callable
import numpy as np
import pygame

from common.colors import Colors
from processors.maze_selection_processor import MazeSelectionProcessor
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

        back_img = pygame.image.load("images/leftarrow.png").convert_alpha()
        self.back_button = Button(0.25, 0.9, back_img)

    def init_maze(self) -> None:
        type_ = self._config.get("maze", "TYPE")
        grid_size = self._config.get("maze", "SIZE")
        self._logger.info(f"Initializing maze. Type: {type_}, Size: {grid_size}")

        if grid_size == "small":
            n = 20
        elif grid_size == "medium":
            n = 35
        elif grid_size == "large":
            n = 50
        else:
            n = 20

        self._get_sqare_size(n)
        self.maze = MazeSelectionProcessor(n, n, maze_type=type_).process().T

        self.maze_buttons = np.empty(self.maze.shape, dtype=MazeSquare)
        for i in range(self.maze.shape[0]):
            for j in range(self.maze.shape[1]):
                self.maze_buttons[i, j] = MazeSquare(self.maze[i, j], self._get_rect(i, j))

    def draw(self, event_list: List[pygame.event.Event]) -> Tuple[Callable, str]:
        if self.back_button.draw(self.window, event_list):
            return "", "main"

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
            return "", "finished"

        return "", "maze"

    @staticmethod
    def _decide_color(maze_val: int) -> pygame.Color:
        if maze_val == 0:
            return Colors.WHITE
        if maze_val == 1:
            return Colors.BLACK
        if maze_val == 2:
            return Colors.GREEN
        if maze_val == 3:
            return Colors.RED
        if maze_val == 4:
            return Colors.PURPLE

    def _get_sqare_size(self, num_cols: int) -> None:
        window_width = int(self._config.get("display", "WINDOW_WIDTH"))
        self.buffer = window_width // 10
        maze_display_size = window_width - (self.buffer * 2)
        self.square_size = maze_display_size // num_cols
        self.buffer -= self.square_size // 2

    def _get_rect(self, i: int, j: int) -> pygame.Rect:
        rect = pygame.Rect(
            (i * self.square_size + self.buffer, j * self.square_size + self.buffer),
            (self.square_size, self.square_size),
        )
        rect.center = (i * self.square_size + self.buffer, j * self.square_size + self.buffer)
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
        i, j = np.where(self.maze == 3)
        i = i[0]
        j = j[0]

        if not self.maze[i - 1, j]:
            return False
        return True
