import pygame

from .base import BaseTheme


class LightTheme(BaseTheme):

    @property
    def name(self) -> str:
        return "light"

    @property
    def background(self) -> pygame.Color:
        return pygame.Color(255, 255, 255)

    @property
    def button_color(self) -> pygame.Color:
        return pygame.Color(0, 0, 0)

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

    @property
    def text_color(self) -> pygame.Color:
        return pygame.Color(0, 0, 0)
