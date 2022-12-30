from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt

from extensions.player import Player
from extensions.graph import Edge


length_to_points = {
    1: 1,
    2: 2,
    3: 4,
    4: 7,
    6: 15,
    8: 21
}


class ResultWidget(QWidget):
    def __init__(self, *args, **kwargs):
        """ Class for displaying the selection menu. """
        super().__init__(*args, **kwargs)

    def show_results(self, players: list[Player], edges: list[Edge]):
        """ Displays information on train points for each player. """
        player_points_dict = {}
        for player in players:
            player_points_dict[player] = 0

        for edge in edges:
            if edge.bought_by:
                player_points_dict[edge.bought_by] += length_to_points[edge.length]

        text = "Total points from trains:"
        for player, points in player_points_dict.items():
            text += f"\n{player.name}: {points} points"

        # Build window
        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.general_layout = QHBoxLayout()
        self.general_layout.addWidget(self.label)
        self.setLayout(self.general_layout)
