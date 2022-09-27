import abc

import pygame


class BaseTheme(abc.ABC):
    @property
    @abc.abstractmethod
    def name(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def background(self) -> pygame.Color:
        ...

    @property
    @abc.abstractmethod
    def button_color(self) -> pygame.Color:
        ...

    @property
    @abc.abstractmethod
    def start_color(self) -> pygame.Color:
        ...

    @property
    @abc.abstractmethod
    def end_color(self) -> pygame.Color:
        ...

    @property
    @abc.abstractmethod
    def wall_color(self) -> pygame.Color:
        ...

    @property
    @abc.abstractmethod
    def hall_color(self) -> pygame.Color:
        ...

    @property
    @abc.abstractmethod
    def path_color(self) -> pygame.Color:
        ...

    @property
    @abc.abstractmethod
    def solution_search_color(self) -> pygame.Color:
        ...

    @property
    @abc.abstractmethod
    def solution_path_color(self) -> pygame.Color:
        ...

    @property
    @abc.abstractmethod
    def text_color(self) -> pygame.Color:
        ...

    @property
    @abc.abstractmethod
    def normal_font(self) -> pygame.font.Font:
        ...

    @property
    @abc.abstractmethod
    def header_font(self) -> pygame.font.Font:
        ...
