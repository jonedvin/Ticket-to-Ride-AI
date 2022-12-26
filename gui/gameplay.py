from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton
from extensions.game import Game
from extensions.player import AI
from extensions.graph import Edge, TrackType
from gui.map_widget import MapWidget


class GameplayWidget(QWidget):
    def __init__(self, main_window, *args, **kwargs):
        """ Class for displaying the main gameplay screen. """
        super().__init__(*args, **kwargs)

        self.main_window = main_window
        self.game = None
        self.last_player = None

        # Player button line
        self.current_player_label = QLabel("'s turn")
        self.current_player_label.setContentsMargins(0, 0, 0, 0)
        self.draw_cards_button = QPushButton("Draw cards")
        self.draw_cards_button.setContentsMargins(0, 0, 0, 0)
        self.player_button_line = QHBoxLayout()
        self.player_button_line.setContentsMargins(0, 0, 0, 0)
        self.player_button_line.addWidget(self.current_player_label)
        self.player_button_line.addWidget(self.draw_cards_button)
        self.player_button_line.addStretch()

        # Map
        self.map_widget = MapWidget(self.main_window)
        self.map_widget.setContentsMargins(0, 0, 0, 0)

        self.general_layout = QVBoxLayout()
        self.general_layout.setContentsMargins(10, 0, 0, 0)
        self.general_layout.addLayout(self.player_button_line)
        self.general_layout.addWidget(self.map_widget)
        self.setLayout(self.general_layout)

        self.setContentsMargins(0, 0, 0, 0)

        # Signals
        self.draw_cards_button.clicked.connect(self.draw_cards)


    def init_game(self, game: Game):
        """ Initializes the gameplay window with the chosen game. """
        self.game = game
        self.update_current_player_label()
        self.map_widget.init_with_map(self.game.map)


    def update_current_player_label(self):
        """ Updates self.current_player_label to correct name. """
        self.current_player_label.setText(f"{self.game.current_player.name}'s turn")


    def next_player(self):
        """ Changes the turn to the next player. Finishes the game if it's done. """
        # If the game is done
        if self.last_player:
            if self.game.current_player == self.last_player:
                pass
                # Finish game

        # Set next player
        next_index = self.game.players.index(self.game.current_player)+1
        if next_index >= len(self.game.players):
            next_index = 0
        self.game.current_player = self.game.players[next_index]

        # Update current player label
        self.update_current_player_label()


    def draw_cards(self):
        """ Makes AI draw cards if it's its turn, and goes to next player regardless. """
        if type(self.game.current_player) == AI:
            self.game.current_player.draw_cards()
        self.next_player()


    def buy_route(self, route: Edge):
        """ Buys the specified route for self.current_player. """
        # Tunnel check
        if route.track_type == TrackType.tunnel:
            pass
            # NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE

        # Take cards from AI
        if type(self.game.current_player) == AI:
            self.game.current_player.hand[route.color] -= route.length
        
        # Take trains used
        self.game.current_player.train_count -= route.length

        # Set route to bought
        route.bought_by = self.game.current_player
        # NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE

        # Stop loop if we reached the final round
        if self.game.current_player.train_count <= 2:
            self.last_player = self.game.current_player

        self.next_player()
