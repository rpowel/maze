import pygame

from common.events import RESTART_EVENT
from .base import BaseProcessor


class RestartProcessor(BaseProcessor):
    def process(self) -> None:
        self._logger.info("Starting Restart Process.")
        pygame.event.post(pygame.event.Event(RESTART_EVENT))
