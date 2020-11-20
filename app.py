#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 06:58:24 2020.

@author: powel
"""
import sys
from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.colors import LinearSegmentedColormap

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

    def _drawMaze(self):
        # TODO: make colormap black/white for walls/cells
        self.ui.frame_2.setEnabled(False)
        self.ui.drawButton.setText("Loading...")
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
        self._ax.axis('off')
        self._ax.set_facecolor('#000000')
        self.ui.drawButton.setText("Draw")
        self.ui.frame_2.setEnabled(True)


if __name__ == '__main__':
    App()

