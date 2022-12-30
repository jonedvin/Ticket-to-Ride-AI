from PyQt6.QtWidgets import QWidget, QHBoxLayout, QMainWindow, QLabel, QApplication
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor, QImage
from PyQt6.QtCore import QPoint, QRect
from extensions.graph import PathSet
from gui.selection_menu import SelectionMenu
from gui.gameplay import GameplayWidget
import numpy as np
import sys
import os


class TestClass():
    def __init__(self, trains: int):
        self.trains = trains

    @property
    def trains_needed(self):
        return int(self.trains)


dict = {
    "2": TestClass(2),
    "1": TestClass(1),
    "3": TestClass(3)
}

dict_two = {
    "2": 2,
    "1": 1,
    "3": 3
}

# new_dict = sorted(dict_two, key=dict_two.get())
# for num in dict_two:
#     print(num)

best = (None, None)
if best[0]:
    print("Hi")