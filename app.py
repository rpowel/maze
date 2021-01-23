#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 06:58:24 2020.

@author: powel
"""
import sys
from PyQt5 import QtWidgets
from numpy import where
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.colors import LinearSegmentedColormap
from random import randrange
from random import seed

from mazes import Maze
from mazegui import Ui_mazeMenu


COLORMAP = LinearSegmentedColormap.from_list(
    'maze', [(1, 1, 1), (0, 0, 0), (0, 1, 0), (1, 0, 0)], N=4)


class App:
    def __init__(self):
        self._init_window()
        self._ax = None

        self._mazeSelectButtons = [
            self.ui.randomButton,
            self.ui.primButton,
            self.ui.kuzatsButton,
            self.ui.recursiveButton,
            ]

        self.ui.drawButton.clicked.connect(self._draw_maze)
        self.ui.seedCheckBox.stateChanged.connect(self._enable_seed)

        self._exit()

    def _init_window(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.mazeMenu = QtWidgets.QDialog()
        self.ui = Ui_mazeMenu()
        self.ui.setupUi(self.mazeMenu)
        self.mazeMenu.show()

    def _exit(self):
        sys.exit(self.app.exec_())

    def _get_choice(self):
        for button in self._mazeSelectButtons:
            if button.isChecked():
                choice = button.text()
                return choice

    def _get_dimensions(self):
        n_x = self.ui.nXBox.value()
        n_y = self.ui.nYBox.value()
        return n_x, n_y

    def _make_maze(self):
        choice = self._get_choice()
        n_x, n_y = self._get_dimensions()
        maze = Maze().make_maze(n_x, n_y, maze_type=choice)
        return maze

    def _enable_seed(self):
        state = self.ui.seedValue.isEnabled()
        if state:
            self.ui.seedValue.setEnabled(False)
        else:
            self.ui.seedValue.setEnabled(True)

    def _get_seed(self):
        if self.ui.seedCheckBox.isChecked():
            seed_ = self.ui.seedValue.value()
        else:
            seed_ = randrange(999999999)
        seed(seed_)
        return seed_

    def _draw_mask(self, maze):
        j, i = where(maze == 2)
        m, k = where(maze == 3)
        i = i[0]
        j = j[0]
        k = k[0]
        m = m[0]
        diff = 0.99

        self._ax.fill(
            [i, i+diff, i+diff, i],
            [j, j, j+diff, j+diff],
            fill=False,
            hatch='////',
            )

        self._ax.fill(
            [k, k+diff, k+diff, k],
            [m, m, m+diff, m+diff],
            fill=False,
            hatch='\\\\\\\\',
            )

    def _draw_maze(self):
        self.ui.frame_2.setEnabled(False)
        self.ui.drawButton.setText("Loading...")
        seed_ = self._get_seed()
        self.ui.seedValue.setValue(seed_)
        self.app.processEvents()
        maze = self._make_maze()
        self.ui.verticalLayout_3.takeAt(0)
        self.canvas = FigureCanvas(
            Figure(
                frameon=False,
                tight_layout=True
                )
            )
        self.ui.verticalLayout_3.addWidget(self.canvas)
        self._ax = self.canvas.figure.subplots()
        self._ax.pcolormesh(maze, edgecolor=None, cmap=COLORMAP)
        self._draw_mask(maze)
        self._ax.axis('off')
        self._ax.set_facecolor('#000000')
        self.ui.drawButton.setText("Draw")
        self.ui.frame_2.setEnabled(True)


if __name__ == '__main__':
    App()
