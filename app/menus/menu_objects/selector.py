from typing import List, Optional, Tuple

import pygame

from .base import BaseMenuObject
from .button import Button


class Selector(BaseMenuObject):
    def __init__(
        self,
        x_rel_pos: int,
        y_rel_pos: int,
        options: List[str],
        current_value: str,
        title: Optional[str] = "",
    ) -> None:
        super().__init__()

        self.options = options
        self.current_index = options.index(str(current_value))
        self.max_index = len(options) - 1
        self.current_value = self.options[self.current_index]
        self.title = title

        x, y = self._scale_abs_pos(x_rel_pos, y_rel_pos)
        self.rect = pygame.Rect(x, y, 150, 40)
        self.rect.center = (x, y)

        left_img = pygame.image.load("images/menu-left.png").convert_alpha()
        self.left_button = Button(x_rel_pos - 0.15, y_rel_pos, left_img)

        right_img = pygame.image.load("images/menu-right.png").convert_alpha()
        self.right_button = Button(x_rel_pos + 0.15, y_rel_pos, right_img)

    def draw(
        self,
        surface: pygame.Surface,
        event_list: List[pygame.event.Event],
    ) -> Tuple[bool, str]:

        change = False
        if self.left_button.draw(surface, event_list):
            self._decrease_index()
            change = True
        if self.right_button.draw(surface, event_list):
            self._increase_index()
            change = True

        msg = self._theme.normal_font.render(
            str(self.current_value).title(),
            True,
            self._theme.text_color,
        )
        surface.blit(msg, msg.get_rect(center=self.rect.center))

        if self.title:
            title_text = self._theme.header_font.render(
                str(self.title).title(),
                True,
                self._theme.text_color,
            )
            surface.blit(
                title_text,
                title_text.get_rect(center=(self.rect.centerx, self.rect.top - 10)),
            )

        return change, self.current_value

    def _increase_index(self):
        if self.current_index == self.max_index:
            self.current_index = 0
        else:
            self.current_index += 1
        self.current_value = self.options[self.current_index]

    def _decrease_index(self):
        if self.current_index == 0:
            self.current_index = self.max_index
        else:
            self.current_index -= 1
        self.current_value = self.options[self.current_index]
