from typing import List

import pygame

from .base import BaseMenuObject


class MazeSquare(BaseMenuObject):
    def __init__(self, maze_val: int, rect: pygame.Rect):
        super().__init__()
        self.maze_val = maze_val
        self.rect = rect
        self.clicked = False

    def draw(self, surface: pygame.Surface, event_list: List[pygame.event.Event]) -> bool:
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action
