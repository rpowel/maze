from typing import List, Optional

import pygame

from .base import BaseMenuObject


class Button(BaseMenuObject):
    def __init__(
        self,
        x_rel_pos: int,
        y_rel_pos: int,
        image: pygame.Surface,
        image_scale: Optional[float] = 0.15
    ) -> None:
        super().__init__()

        self.image = self._scale_image(image, image_scale)
        self._color_button_image(self.image, self._theme.button_color)
        self.rect = self.image.get_rect()
        self.rect.center = self._scale_abs_pos(x_rel_pos, y_rel_pos)
        self.mask = pygame.mask.from_surface(self.image)
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
                    action = True
                    self.pressed = False
        else:
            self.pressed = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

    def _check_mouse_pos(self) -> bool:
        pos_x, pos_y = pygame.mouse.get_pos()
        # if self.rect.collidepoint(pos):
        #     return True
        try:
            if self.mask.get_at((pos_x - self.rect.x, pos_y - self.rect.y)):
                return True
        except IndexError:
            pass
        return False

    def _color_button_image(self, image: pygame.Surface, new_color: pygame.Color) -> pygame.Surface:
        width, height = image.get_size()
        r, g, b, _ = new_color
        for x in range(width):
            for y in range(height):
                alpha = image.get_at((x, y))[3]
                image.set_at((x, y), pygame.Color(r, g, b, alpha))
