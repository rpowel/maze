from typing import TypeVar

from .default_theme import DefaultTheme
from .light_theme import LightTheme

THEME_MAP = {
    DefaultTheme().name: DefaultTheme(),
    LightTheme().name: LightTheme(),
}

THEME_LIST = list(THEME_MAP.keys())

ThemeType = TypeVar("ThemeType", DefaultTheme, LightTheme)

__all__ = [
    "THEME_LIST",
    "THEME_MAP",
    "ThemeType",
]
