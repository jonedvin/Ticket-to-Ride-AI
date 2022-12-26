from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QMouseEvent, QPixmap, QPainter, QPen, QColor
from PyQt6.QtCore import QPoint
from extensions.maps import Map
import numpy as np
import os


class MapWidget(QWidget):
    CityRadius = 25

    def __init__(self, main_window, map: Map = None, *args, **kwargs):
        """ Class for displaying the map. """
        super().__init__(*args, **kwargs)

        self.main_window = main_window
        self.map = None
        if map:
            self.init_with_map()

        # Setup widget
        self.label = QLabel()
        self.label.setContentsMargins(0, 0, 0, 0)
        self.general_layout = QVBoxLayout()
        self.general_layout.addWidget(self.label)
        self.general_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.general_layout)

    def mousePressEvent(self, event: QMouseEvent):
        ##### Get position and find route ########

        # Check if inside city circle
        for node in self.map.nodes:
            cathetus_one = abs(event.pos().x() - node.x)
            cathetus_two = abs(event.pos().y() - node.y)
            hypotenuse = np.sqrt(cathetus_one**2 + cathetus_two**2)
            if hypotenuse <= self.CityRadius:
                print(f"Inside circle of {node}")
                return super().mousePressEvent(event)

        # Find which route was pressed
        #   If double route, find color

        return super().mousePressEvent(event)

    def init_with_map(self, map: Map):
        """ Initializes the widget based on given map. """
        self.map = map
        self.setFixedSize(map.width, map.height)
        self.main_window.setFixedSize(map.width, map.height+100)

        self.canvas = QPixmap(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "maps", map.filename))
        self.label.setPixmap(self.canvas)
