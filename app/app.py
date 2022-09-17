import pygame
from pygame.constants import QUIT as QUIT_EVENT

from common.events import RESTART_EVENT
from menus import FinishedMenu, MainMenu, MazeMenu, OptionsMenu
from processors import DisplayProcessor, ExitProcessor


def main():
    pygame.init()
    clock = pygame.time.Clock()
    print()
    display = DisplayProcessor()
    main_menu = MainMenu(display.surface)
    maze_menu = MazeMenu(display.surface)
    options_menu = OptionsMenu(display.surface)
    finished_menu = FinishedMenu(display.surface)

    current_menu = "main"
    action = None
    maze_created = False
    score_ticks = 0
    tick_rate = 30

    while True:
        clock.tick(tick_rate)
        event_list = pygame.event.get()
        display.process()

        for event in event_list:
            if event.type == QUIT_EVENT:
                ExitProcessor().process()
            if event.type == RESTART_EVENT:
                main()

        if current_menu == "main":
            maze_created = False
            action, current_menu = main_menu.draw(event_list)

        elif current_menu == "maze":
            if not maze_created:
                maze_menu.init_maze()
                maze_created = True
                score_ticks = 0
            action, current_menu = maze_menu.draw(event_list)
            maze_menu.tick_rate = tick_rate
            score_ticks += 1

        elif current_menu == "options":
            action, current_menu = options_menu.draw(event_list)

        elif current_menu == "finished":
            finished_menu.score_ticks = maze_menu.score_ticks
            finished_menu.tick_rate = maze_menu.tick_rate
            pygame.time.wait(500)
            action, current_menu = finished_menu.draw(event_list)

        if action:
            action()


if __name__ == "__main__":
    main()
