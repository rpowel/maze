#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 10:44:44 2020.

@author: powel
"""
import os
import numpy as np
from scipy import spatial
import matplotlib.pyplot as plt
from skimage.transform import resize
import pyglet
import random
os.environ['SDL_AUDIODRIVER'] = 'dsp'

class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)


class Maze:
    def make_maze(self, n_x, n_y, maze_type='prim'):
        if maze_type == 'random':
            self.maze = RandomMaze().make_maze(n_x, n_y)
        elif maze_type == 'prim':
            self.maze = PrimMaze().make_maze(n_x, n_y)
        elif maze_type == 'kruskal':
            self.maze = KruskalMaze().make_maze(n_x, n_y)
        else:
            self.maze = None

        self._set_entrance()
        self._set_exit()

        return self.maze

    def _fill_square(self, percentage=50):
        random_ = random.randint(0, 101)
        if random_ > percentage:
            return 1
        return 0

    def _set_entrance(self):
        while True:
            x, y = random.randint(1, self.maze.shape[0]-1), 0
            if self.maze[x, y+1] == 0:
                break
        self.maze[x, y] = 2

    def _set_exit(self):
        while True:
            x, y = random.randint(1, self.maze.shape[0]-1), self.maze.shape[1]-1
            if self.maze[x, y-1] == 0:
                break
        self.maze[x, y] = 3

    def _check_percolation(self, maze):
        # TODO Check percolation of random maze
        range_x = maze.shape[0]
        range_y = maze.shape[1]


class RandomMaze:
    def make_maze(self, n_x, n_y):
        maze_arr = np.zeros([n_x, n_y], dtype=int)
        for i in range(n_x):
            for j in range(n_y):
                maze_arr[i, j] = self._fill_square()
        return maze_arr

    def _fill_square(self, percentage=50):
        random_ = random.randint(0, 101)
        if random_ > percentage:
            return 1
        return 0

class PrimMaze:
    def make_maze(self, n_x, n_y):
        while True:
            self._loop = True
            self.walls = []
            self.passage = []
            self.maze = np.full([n_x+1, n_y+1], 1, dtype=int)
            x, y = random.randint(1, n_x-1), 1
            self.passage.append([x, y])
            self.maze[x, y] = 0
            self._add_walls(x, y)

            for i in range(n_x*n_y):
                pos, wall = self._pick_wall()
                if pos is None:
                    break
                x, y = pos
                self.maze[x, y] = 0
                self.walls.pop(wall)
                self._add_walls(x, y)
                self.passage.append([x, y])

            if len(self.passage) > (n_x*n_y/4):
                break  # prevents weird mazes with only a few squares

        self._prepare_final()
        return self.maze

    def _add_walls(self, x, y):
        self.ghost_maze = np.zeros(
            [self.maze.shape[0]+2, self.maze.shape[1]+2],
            dtype=int
        )
        self.ghost_maze[1:-1, 1:-1] = self.maze

        if self.ghost_maze[x+1, y+2]:
            self.walls.append([x, y+1])
        if self.ghost_maze[x+1, y]:
            self.walls.append([x, y-1])
        if self.ghost_maze[x+2, y+1]:
            self.walls.append([x+1, y])
        if self.ghost_maze[x, y+1]:
            self.walls.append([x-1, y])

    def _pick_wall(self):
        iterations = 0
        while True:
            high = len(self.walls)
            iterations += 1
            if iterations > high*2:
                return None, None
            rand_wall = random.randint(0, high - 1)

            x_wall, y_wall = self.walls[rand_wall]
            x, y = self._find_nearest_passage([x_wall, y_wall])
            diff_x = x - x_wall
            diff_y = y - y_wall

            try:
                next_over = self.maze[x_wall-diff_x, y_wall-diff_y]
                if diff_x !=0:
                    next_right = self.maze[x_wall, y_wall-1]
                    next_left = self.maze[x_wall, y_wall+1]
                    next_right_over = self.maze[x_wall-diff_x, y_wall-1]
                    next_left_over = self.maze[x_wall-diff_x, y_wall+1]
                else:
                    next_right = self.maze[x_wall+1, y_wall]
                    next_left = self.maze[x_wall-1, y_wall]
                    next_right_over = self.maze[x_wall+1, y_wall-diff_y]
                    next_left_over = self.maze[x_wall-1, y_wall-diff_y]

            except Exception:
                continue

            if not (next_over and next_right and next_left
                    and next_left_over and next_right_over):
                self.walls.pop(rand_wall)
            else:
                return self.walls[rand_wall], rand_wall

    def _find_nearest_passage(self, pos):
        _, index = spatial.cKDTree(self.passage).query(pos)
        return self.passage[index]

    def _prepare_final(self):
        maze_temp = np.ones([self.maze.shape[0]+1, self.maze.shape[1]+1], dtype=int)
        maze_temp[1:-1, 1:-1] = self.maze[:-1, :-1]
        self.maze = maze_temp


class KruskalMaze:
    def make_maze(self, n_x, n_y):
        self.num_cells_last = -1
        len_x = (n_x+4)
        len_y = (n_y+4)
        self.maze = np.full([len_x, len_y], 1, dtype=int)
        self._make_walls()
        self._make_sets()
        self._repeat_iterations = 0
        while True:
            self._join_cells()
            if self._check_final():
                break
        self._prepare_final()
        print(self.maze)
        return self.maze

    def _make_walls(self):
        self.walls = np.arange(0, self.maze.size, dtype=int)
        self.walls = np.reshape(self.walls, self.maze.shape)
        for i in range(self.maze.shape[0]):
            if (i%2 == 1):
                self.walls[i, :] = -1
        for j in range(self.maze.shape[1]):
            if (j%2 ==1):
                self.walls[:, j] = -1
        self.walls[:, 0] = self.walls[:, -1] = -1
        self.walls[0, :] = self.walls[-1, :] = -1

    def _make_sets(self):
        self.sets = []
        for i in range(self.walls.shape[0]):
            for j in range(self.walls.shape[1]):
                wall_id = self.walls[i, j]
                self.sets.append({wall_id})

    def _pick_wall(self):
        while True:
            i = random.randint(2, self.walls.shape[0]-3)
            j = random.randint(2, self.walls.shape[1]-3)
            wall_id = self.walls[i, j]
            if ((self.walls[i+1, j] == -1) and (self.walls[i-1, j] == -1)
                and (self.walls[i, j+1] == -1) and (self.walls[i, j-1] == -1)):
                continue
            if wall_id == -1:
                return i, j

    def _check_wall(self):
        id_1 = None
        for i in range(5):
            i, j = self._pick_wall()
            set_id_left = self.walls[i-1, j]
            set_id_right = self.walls[i+1, j]
            set_id_up = self.walls[i, j+1]
            set_id_down = self.walls[i, j-1]

            set_left = self.sets[set_id_left]
            set_right = self.sets[set_id_right]
            set_up = self.sets[set_id_up]
            set_down = self.sets[set_id_down]

            rand_flt = random.random()
            if rand_flt <= 0.5:
                sym_diff = set_left^set_right
                if ((set_id_left in sym_diff) and (set_id_right in sym_diff)):
                    id_1 = set_id_left
                    id_2 = set_id_right
                    i_1, j_1 = i-1, j
                    i_2, j_2 = i+1, j

            else:
                sym_diff = set_up^set_down
                if ((set_id_up in sym_diff) and (set_id_down in sym_diff)):
                    id_1 = set_id_up
                    id_2 = set_id_down
                    i_1, j_1 = i, j+1
                    i_2, j_2 = i, j-1

            if (id_1 is not None):
                self.walls[i, j] = -2

                self.maze[i, j] = 0
                self.maze[i_1, j_1] = 0
                self.maze[i_2, j_2] = 0

                return id_1, id_2

        return None, None

    def _check_final(self):
        flat = np.ravel(self.maze)
        num_cells = len(flat[flat==0])
        if num_cells == self.num_cells_last:
            self._repeat_iterations += 1
        if self._repeat_iterations > 20:
            return True
        if num_cells != self.num_cells_last:
            self._repeat_iterations = 0
            self.num_cells_last = num_cells
        return False

    def _join_cells(self):
        id_1, id_2 = self._check_wall()
        if id_1 is None:
            return None

        for i in range(self.maze.shape[0]):
            for j in range(self.maze.shape[1]):
                if self.maze[i, j] == 0:
                    if self.maze[i+1, j] == 0:
                        self.sets[self.walls[i, j]].update(self.sets[self.walls[i+2, j]])
                        self.sets[self.walls[i+2, j]].update(self.sets[self.walls[i, j]])
                    if self.maze[i-1, j] == 0:
                        self.sets[self.walls[i, j]].update(self.sets[self.walls[i-2, j]])
                        self.sets[self.walls[i-2, j]].update(self.sets[self.walls[i, j]])
                    if self.maze[i, j+1] == 0:
                        self.sets[self.walls[i, j]].update(self.sets[self.walls[i, j+2]])
                        self.sets[self.walls[i, j+2]].update(self.sets[self.walls[i, j]])
                    if self.maze[i, j-1] == 0:
                        self.sets[self.walls[i, j]].update(self.sets[self.walls[i, j-2]])
                        self.sets[self.walls[i, j-2]].update(self.sets[self.walls[i, j]])

    def _prepare_final(self):
        maze_temp = np.ones([self.maze.shape[0]-2, self.maze.shape[1]-2], dtype=int)
        maze_temp[1:-1, 1:-1] = self.maze[2:-2, 2:-2]
        self.maze = maze_temp


class App():
    window = pyglet.window.Window()
    window.set_visible()
    pyglet.app.run()


# class App(Maze):
#     window_height = 600
#     window_width = 900

#     window_pos_x = 0
#     window_pos_y = 0

#     def __init__(self):
#         pygame.init()
#         self._running = True
#         self._init_screen()
#         self._loop()

#     def _init_screen(self):
#         os.environ['SDL_VIDEO_WINDOW_POS'] = (
#             f'{self.window_pos_x}, {self.window_pos_y}')

#         self.screen = pygame.display.set_mode(
#             [self.window_width, self.window_height])

#         self.maze_canvas = pygame.Surface((600, 600))
#         self.maze_frame = pygame.Rect(0, 0, 600, 600)

#         self.setting_canvas = pygame.Surface((300, 600))
#         self.setting_frame = pygame.Rect(0, 0, 300, 600)

#         self._draw_maze(self.maze_canvas, 20, 20)
#         self._init_settings()

#     def _init_settings(self):
#         input_1 = TextInput(initial_string='Dim_x')
#         input_2 = TextInput(initial_string='Dim_y')
#         self.inputs = [
#             input_1,
#             input_2
#             ]

#     def _draw_settings(self, x, y):
#         self.setting_canvas.fill(Colors.WHITE)
#         self.screen.blit(self.setting_canvas, (x, y))
#         x_i = x+10
#         y_i = y+10
#         for box in self.inputs:
#             self.screen.blit(box.get_surface(), (x_i, y_i))
#             y_i += 30

#     def _draw_maze(self, frame, n_x, n_y, maze_type='prim'):
#         self.maze = self.make_maze(n_x, n_y, maze_type=maze_type)
#         self.square_size_x = int(self.window_width/3*2/(n_x+3))
#         self.square_size_y = int(self.window_height/(n_y+3))
#         x = self.square_size_x/2
#         for i in range(self.maze.shape[0]):
#             y = self.square_size_y/2
#             for j in range(self.maze.shape[1]):
#                 if self.maze[i, j] == 1:
#                     color = Colors.BLACK
#                 elif self.maze[i, j] == 0:
#                     color = Colors.WHITE
#                 elif self.maze[i, j] == 2:
#                     color = Colors.GREEN
#                 elif self.maze[i, j] == 3:
#                     color = Colors.RED

#                 pygame.draw.rect(
#                     frame,
#                     color,
#                     pygame.Rect(x, y, self.square_size_x, self.square_size_y),
#                     0
#                 )
#                 y += self.square_size_y
#             x += self.square_size_x

#     def _handle_events(self):
#         events = pygame.event.get()
#         for box in self.inputs:
#             box.update(events)
#         for event in events:
#             if event.type == pygame.QUIT:
#                 self._running = False
#                 self._exit()

#     def _exit(self):
#         pygame.quit()

#     def _loop(self):
#         clock = pygame.time.Clock()
#         while self._running:
#             self._draw_settings(600, 0)
#             self.screen.blit(self.maze_canvas, (0,0), self.maze_frame)
#             pygame.display.flip()
#             self._handle_events()
#             if self._running:
#                 clock.tick(30)


if __name__ == '__main__':
    App()
