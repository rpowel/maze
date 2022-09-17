from typing import List

import pygame

from .base import BaseMenuObject


class Button(BaseMenuObject):
    def __init__(
        self,
        x_rel_pos: float,
        y_rel_pos: float,
        image: pygame.surface.Surface,
        image_scale: float = 0.15,
    ) -> None:
        super().__init__()

        self.image = self._scale_image(image, image_scale)
        self._color_button_image(self.image, self._theme.button_color)
        self.rect = self.image.get_rect()
        self.rect.center = self._scale_abs_pos(x_rel_pos, y_rel_pos)
        self.pressed = False

    def draw(
        self,
        surface: pygame.surface.Surface,
        event_list: List[pygame.event.Event],
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

    @staticmethod
    def _color_button_image(image: pygame.surface.Surface, new_color: pygame.Color):
        width, height = image.get_size()
        r = new_color.r
        g = new_color.g
        b = new_color.b
        for x in range(width):
            for y in range(height):
                alpha = image.get_at((x, y))[3]
                image.set_at((x, y), pygame.Color(r, g, b, alpha))
