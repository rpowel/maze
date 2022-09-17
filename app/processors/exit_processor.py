import sys

import pygame

from .base import BaseProcessor


class ExitProcessor(BaseProcessor):
    def process(self):
        self._logger.info("Starting Exit Process.")
        pygame.quit()
        sys.exit()
