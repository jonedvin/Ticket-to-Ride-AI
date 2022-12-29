from PyQt6.QtWidgets import QWidget, QLabel, QStackedLayout
from PyQt6.QtGui import QMouseEvent, QPixmap, QColor, QImage
from extensions.maps import Map
import numpy as np
import enum
import os


class MapType(enum.Enum):
    pretty = 0
    color = 1


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
        self.pretty_label = QLabel()
        self.color_label = QLabel()
        self.general_layout = QStackedLayout()
        self.general_layout.addWidget(self.pretty_label)
        self.general_layout.addWidget(self.color_label)
        self.setLayout(self.general_layout)


    def mousePressEvent(self, event: QMouseEvent):
        ##### Get position and find route ########
        clicked_x = event.pos().x()
        clicked_y = event.pos().y()

        # Check if inside city circle
        for node in self.map.nodes:
            cathetus_one = abs(clicked_x - node.x)
            cathetus_two = abs(clicked_y - node.y)
            hypotenuse = np.sqrt(cathetus_one**2 + cathetus_two**2)
            if hypotenuse <= self.CityRadius:
                print(f"Inside circle of {node}")
                return super().mousePressEvent(event)

        # Get color
        color = QColor(self.color_img.pixel(clicked_x, clicked_y)).name()

        # No need to search when clicking sea, land or border
        if color in ["#c4e2ec", "#dec6aa", "#b0a091"]:
            return super().mousePressEvent(event)

        # Find edge
        for edge in self.map.edges:
            if edge.hex_id == color:
                print(edge)

        return super().mousePressEvent(event)


    def init_with_map(self, map: Map):
        """ Initializes the widget based on given map. """
        self.map = map
        self.setFixedSize(map.width, map.height)

        self.pretty_canvas = QPixmap(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "maps", map.filename))
        self.pretty_label.setPixmap(self.pretty_canvas)

        self.color_canvas = QPixmap(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "maps", map.color_filename))
        self.color_label.setPixmap(self.color_canvas)
        self.color_img = QImage(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "maps", map.color_filename))
