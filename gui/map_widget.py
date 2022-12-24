from PyQt6.QtWidgets import QWidget
from extensions.maps import Map


# class City(QWidget)


class MapWidget(QWidget):

    def __init__(self, map: Map = None, *args, **kwargs):
        """ Class for displaying the map. """
        super().__init__(*args, **kwargs)

        self.map = None
        if map:
            self.init_with_map()

    def init_with_map(self, map: Map):
        pass

