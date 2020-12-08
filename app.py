#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 06:58:24 2020.

@author: powel
"""
import sys
from PyQt5 import QtWidgets
from numpy import zeros, arange, meshgrid, where
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.colors import LinearSegmentedColormap
from random import randrange
from random import seed

from mazes import Maze
from mazegui import Ui_mazeMenu


COLORMAP = LinearSegmentedColormap.from_list(
    'maze', [(1, 1, 1), (0, 0, 0), (0, 1, 0), (1, 0, 0)], N = 4)


class App():
    def __init__(self):
        self._initWindow()
        self._ax = None

        self._mazeSelectButtons = [
            self.ui.randomButton,
            self.ui.primButton,
            self.ui.kuzatsButton
            ]

        self.ui.drawButton.clicked.connect(self._drawMaze)
        self.ui.seedCheckBox.stateChanged.connect(self._enableSeed)

        self._exit()

    def _initWindow(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.mazeMenu = QtWidgets.QDialog()
        self.ui = Ui_mazeMenu()
        self.ui.setupUi(self.mazeMenu)
        self.mazeMenu.show()

    def _exit(self):
        sys.exit(self.app.exec_())

    def _getChoice(self):
        for button in self._mazeSelectButtons:
            if button.isChecked():
                choice = button.text()
                return choice

    def _getDimensions(self):
        nX = self.ui.nXBox.value()
        nY = self.ui.nYBox.value()
        return nX, nY

    def _makeMaze(self):
        choice = self._getChoice()
        nX, nY = self._getDimensions()
        maze = Maze().make_maze(nX, nY, maze_type=choice)
        return maze

    def _enableSeed(self):
        state = self.ui.seedValue.isEnabled()
        if state:
            self.ui.seedValue.setEnabled(False)
        else:
            self.ui.seedValue.setEnabled(True)

    def _getSeed(self):
        if self.ui.seedCheckBox.isChecked():
            seed_ = self.ui.seedValue.value()
        else:
            seed_ = randrange(999999999)
        seed(seed_)
        return seed_

    def _drawMask(self, maze):
        j, i = where(maze == 2)
        l, k = where(maze == 3)
        i = i[0]
        j = j[0]
        k = k[0]
        l = l[0]
        diff = 0.99

        self._ax.fill(
            [i, i+diff, i+diff, i],
            [j, j, j+diff, j+diff],
            fill=False,
            hatch='////',
            )

        self._ax.fill(
            [k, k+diff, k+diff, k],
            [l, l, l+diff, l+diff],
            fill=False,
            hatch='\\\\\\\\',
            )

    def _drawMaze(self):
        self.ui.frame_2.setEnabled(False)
        self.ui.drawButton.setText("Loading...")
        seed_ = self._getSeed()
        self.ui.seedValue.setValue(seed_)
        self.app.processEvents()
        maze = self._makeMaze()
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
        self._drawMask(maze)
        self._ax.axis('off')
        self._ax.set_facecolor('#000000')
        self.ui.drawButton.setText("Draw")
        self.ui.frame_2.setEnabled(True)


if __name__ == '__main__':
    App()
