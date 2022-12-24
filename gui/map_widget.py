from PyQt6.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QLabel, QHBoxLayout, QVBoxLayout, QLineEdit, QComboBox, QPushButton
from extensions.player import Player, AI, PlayerColor
from extensions.game import Game
from extensions.maps import Map


class MapWidget(QWidget):

    def __init__(self, map: Map, *args, **kwargs):
        """ Class for displaying the map. """
        super().__init__(*args, **kwargs)

        self.map = map

