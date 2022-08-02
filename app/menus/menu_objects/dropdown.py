import pygame
from typing import List

from .base import BaseMenuObject
from common.colors import Colors


class DropDown(BaseMenuObject):
    def __init__(
        self,
        x_rel_pos: float,
        y_rel_pos: float,
        name: str,
        options: List[str],
    ):
        super().__init__()
        x, y = self._scale_abs_pos(x_rel_pos, y_rel_pos)
        self.rect = pygame.Rect(x, y, 150, 40)
        self.rect.center = (x, y)
        self.font = pygame.font.SysFont("Calibri", 20)
        self.name = name
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, surface: pygame.Surface, event_list: List[pygame.event.Event]) -> int:
        selected_row = self.update(event_list)
        pygame.draw.rect(surface, Colors.WHITE, self.rect, 0)
        msg = self.font.render(self.name, 1, (0, 0, 0))
        surface.blit(msg, msg.get_rect(center=self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pygame.draw.rect(
                    surface,
                    Colors.GREEN if i == self.active_option else Colors.WHITE,
                    rect,
                    0,
                )
                msg = self.font.render(str(text), 1, (0, 0, 0))
                surface.blit(msg, msg.get_rect(center=rect.center))

        if selected_row > -1:
            selection = self.options[selected_row]
        else:
            selection = None
        # print(selection)
        return selection

    def update(self, event_list: List[pygame.event.Event]) -> int:
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)

        self.active_option = -1
        rect_list = []
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            rect_list.append(rect)
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._logger.info(f"Selected option: {self.active_option}")
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.draw_menu = False
                    return self.active_option

        return -1
