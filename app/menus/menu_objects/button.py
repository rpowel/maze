import pygame
from typing import List

from .base import BaseMenuObject


class Button(BaseMenuObject):
    def __init__(
        self,
        x_rel_pos: int,
        y_rel_pos: int,
        image: pygame.Surface,
    ) -> None:
        super().__init__()

        self.image = self._scale_image(image, 0.15)
        self.rect = self.image.get_rect()
        self.rect.center = self._scale_abs_pos(x_rel_pos, y_rel_pos)
        self.clicked = False

    def draw(
        self, surface: pygame.Surface, event_list: List[pygame.event.Event]
    ) -> bool:
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
