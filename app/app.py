#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 06:58:24 2020.

@author: powel
"""
import sys

import pygame
import pygame.locals

from common.events import RESTART_EVENT
from processors import DisplayProcessor
from menus import FinishedMenu, MainMenu, MazeMenu, OptionsMenu


def main():
    pygame.init()

    clock = pygame.time.Clock()
    clock.tick(30)

    display = DisplayProcessor()
    main_menu = MainMenu(display.surface)
    maze_menu = MazeMenu(display.surface)
    options_menu = OptionsMenu(display.surface)
    finshed_menu = FinishedMenu(display.surface)

    current_menu = "main"
    action = None
    maze_created = False

    while True:
        event_list = pygame.event.get()
        display.process()

        for event in event_list:
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == RESTART_EVENT:
                main()

        if current_menu == "main":
            maze_created = False
            action, current_menu = main_menu.draw(event_list)
        elif current_menu == "maze":
            if not maze_created:
                maze_menu.init_maze()
                maze_created = True
            action, current_menu = maze_menu.draw(event_list)
        elif current_menu == "options":
            action, current_menu = options_menu.draw(event_list)
        elif current_menu == "finished":
            action, current_menu = finshed_menu.draw(event_list)

        if action:
            action()


if __name__ == "__main__":
    main()
