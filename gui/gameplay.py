from PyQt6.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QLabel, QHBoxLayout, QVBoxLayout, QLineEdit, QComboBox, QPushButton
from extensions.player import Player, AI, PlayerColor
from extensions.game import Game
from extensions.maps import Map
from gui.map_widget import MapWidget


class GameplayWidget(QWidget):

    def __init__(self, main_window, *args, **kwargs):
        """ Class for displaying the main gameplay screen. """
        super().__init__(*args, **kwargs)

        self.main_window = main_window
        self.game = None

        # Player button line
        self.current_player_label = QLabel("'s turn")
        self.draw_cards_button = QPushButton("Draw cards")
        self.player_button_line = QHBoxLayout()
        self.player_button_line.addWidget(self.current_player_label)
        self.player_button_line.addWidget(self.draw_cards_button)
        self.player_button_line.addStretch()

        # Map
        self.map_widget = None

        self.general_layout = QVBoxLayout()
        self.general_layout.addLayout(self.player_button_line)
        self.general_layout.addWidget(self.map_widget)
        self.setLayout(self.general_layout)

    def init_game(self, game: Game):
        """ Initializes the gameplay window with the chosen game. """
        self.game = game
        self.current_player_label.setText(f"{self.game.current_player.name}'s turn")
        self.map_widget.init_with_map(self.game.map)