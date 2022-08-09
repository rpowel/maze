from orm import Scores
from .base import BaseProcessor


class FinishProcessor(BaseProcessor):
    def __init__(self, maze_type: str, size_x: int, size_y: int, time_seconds: int) -> None:
        super().__init__()
        self.maze_type = maze_type
        self.size_x = size_x
        self.size_y = size_y
        self.time_seconds = time_seconds

    def process(self) -> None:
        Scores.create(
            maze_type=self.maze_type,
            size_x=self.size_x,
            size_y=self.size_y,
            time_seconds=self.time_seconds,
        )
