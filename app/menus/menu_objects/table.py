from typing import List, Tuple, Type

import pygame

from .base import BaseMenuObject


class Table(BaseMenuObject):
    def __init__(
        self,
        title: str,
        rel_x_pos: float,
        rel_y_pos: float,
        headers: List[str],
        data: List[Tuple[str]],
    ) -> None:
        super().__init__()
        self.title = title
        self.rect_left, self.rect_top = self._scale_abs_pos(rel_x_pos, rel_y_pos)
        self.headers = headers
        self.data = data

        self.num_columns = len(headers)
        self.num_rows = len(data) + 1

        window_width = int(self._config.get("display", "window_width"))
        window_height = int(self._config.get("display", "window_height"))
        self.col_width = (window_width - self.rect_left * 2) // self.num_columns
        self.row_height = (window_height - self.rect_top - 150) // self.num_rows

    def draw(
        self, surface: pygame.Surface, event_list: List[pygame.event.Event]
    ) -> Type[object]:
        self._draw_title(surface)
        self._draw_headers(surface)
        self._draw_data(surface)

    def _draw_title(self, surface: pygame.Surface) -> None:
        rect = pygame.Rect(
            int(self._config.get("display", "window_width")) * 0.4,
            max(
                self.rect_top - (self.row_height * (self.num_rows // 2)),
                int(self._config.get("display", "window_height")) // 2 - 40,
            ),
            self.col_width,
            self.row_height,
        )
        text = self._theme.header_font.render(
            str(self.title).title(),
            True,
            self._theme.text_color,
        )
        surface.blit(
            text,
            text.get_rect(center=rect.center),
        )

    def _draw_headers(self, surface: pygame.Surface) -> None:
        for i, row in enumerate(self.data):
            for j, val in enumerate(row):
                rect = pygame.Rect(
                    self.rect_left + (self.col_width * j),
                    self.rect_top + (self.row_height * (i + 1)),
                    self.col_width,
                    self.row_height,
                )
                text = self._theme.normal_font.render(
                    str(val).title(), True, self._theme.text_color
                )
                surface.blit(text, text.get_rect(center=rect.center))

    def _draw_data(self, surface: pygame.Surface) -> None:
        for i, header in enumerate(self.headers):
            rect = pygame.Rect(
                self.rect_left + (self.col_width * i),
                self.rect_top,
                self.col_width,
                self.row_height,
            )
            text = self._theme.header_font.render(
                header.title(), True, self._theme.text_color
            )
            surface.blit(text, text.get_rect(center=rect.center))
