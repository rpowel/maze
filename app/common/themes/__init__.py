from .base import BaseTheme
from .default_theme import DefaultTheme
from .light_theme import LightTheme

THEME_MAP = {
    DefaultTheme().name: DefaultTheme(),
    LightTheme().name: LightTheme(),
}

THEME_LIST = list(THEME_MAP.keys())

__all__ = [
    "BaseTheme",
    "THEME_LIST",
    "THEME_MAP",
]
