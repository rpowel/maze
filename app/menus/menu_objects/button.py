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
        self.pressed = False

    def draw(
        self, surface: pygame.Surface, event_list: List[pygame.event.Event]
    ) -> bool:
        action = False
        if self._check_mouse_pos():
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.pressed = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.pressed:
                        action = True
                        self.pressed = False
        else:
            self.pressed = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

    def _check_mouse_pos(self) -> bool:
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return True
        return False
