from PyQt6.QtWidgets import QWidget, QLabel, QStackedLayout
from PyQt6.QtGui import QMouseEvent, QPixmap, QColor, QImage, QPainter, QPen
from extensions.maps import Map
from extensions.player import AI, Player
from extensions.graph import Edge
import numpy as np
import enum
import os


class MapType(enum.Enum):
    pretty = 0
    color = 1


class MapWidget(QWidget):
    CityRadius = 25
    FillRouteMargin = 100

    def __init__(self, gameplay_widget, map: Map = None, *args, **kwargs):
        """ Class for displaying the map. """
        super().__init__(*args, **kwargs)

        self.gameplay_widget = gameplay_widget
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
        if type(self.gameplay_widget.current_player) == AI:
            return super().mousePressEvent(event)

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

                # Cannot buy route that's already bought
                if edge.bought_by:
                    break

                # Buy route
                self.gameplay_widget.buy_route(edge)
                break

        return super().mousePressEvent(event)


    def draw_bought_route(self, player: Player, route: Edge):
        """ Colors the route in the shape from self.color_img, on self.pretty_canvas. """
        painter = QPainter(self.pretty_canvas)
        painter.setPen(QPen(QColor(player.get_color)))

        min_x = max(min(route.end_nodes[0].x, route.end_nodes[1].x) - self.FillRouteMargin, 0)
        max_x = min(max(route.end_nodes[0].x, route.end_nodes[1].x) + self.FillRouteMargin, self.map.width)
        min_y = max(min(route.end_nodes[0].y, route.end_nodes[1].y) - self.FillRouteMargin, 0)
        max_y = min(max(route.end_nodes[0].y, route.end_nodes[1].y) + self.FillRouteMargin, self.map.height)

        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                if QColor(self.color_img.pixel(x, y)).name() == route.hex_id:
                    painter.drawPoint(x, y)

        self.pretty_label.setPixmap(self.pretty_canvas)


    def init_with_map(self, map: Map):
        """ Initializes the widget based on given map. """
        self.map = map

        self.pretty_canvas = QPixmap(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "maps", map.filename))
        self.pretty_label.setPixmap(self.pretty_canvas)

        self.color_canvas = QPixmap(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "maps", map.color_filename))
        self.color_label.setPixmap(self.color_canvas)
        self.color_img = QImage(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "maps", map.color_filename))

        self.setFixedSize(self.pretty_canvas.rect().width(), self.pretty_canvas.rect().height())
