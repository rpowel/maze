import pygame

from .base import BaseTheme


class DefaultTheme(BaseTheme):
    @property
    def solution_path_color(self) -> pygame.Color:
        return pygame.Color(0, 0, 255)

    @property
    def solution_search_color(self) -> pygame.Color:
        return pygame.Color(0, 255, 255)

    @property
    def normal_font(self) -> pygame.font.Font:
        return pygame.font.SysFont("Calibri", 20)

    @property
    def header_font(self) -> pygame.font.Font:
        font = pygame.font.SysFont("Calibri", 22)
        font.set_underline(True)
        return font

    @property
    def name(self) -> str:
        return "default"

    @property
    def text_color(self) -> pygame.Color:
        return pygame.Color(255, 255, 255)

    @property
    def background(self) -> pygame.Color:
        return pygame.Color(67, 70, 75)

    @property
    def button_color(self) -> pygame.Color:
        return pygame.Color(255, 255, 255)

    @property
    def start_color(self) -> pygame.Color:
        return pygame.Color(0, 255, 0)

    @property
    def end_color(self) -> pygame.Color:
        return pygame.Color(255, 0, 0)

    @property
    def wall_color(self) -> pygame.Color:
        return pygame.Color(0, 0, 0)

    @property
    def hall_color(self) -> pygame.Color:
        return pygame.Color(255, 255, 255)

    @property
    def path_color(self) -> pygame.Color:
        return pygame.Color(255, 0, 255)
