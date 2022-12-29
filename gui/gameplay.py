from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QCheckBox
from extensions.player import AI, Player
from extensions.graph import Edge
from extensions.maps import Map
from gui.map_widget import MapWidget, MapType


class GameplayWidget(QWidget):
    PlayersLabelWidth = 150

    def __init__(self, main_window, *args, **kwargs):
        """ Class for displaying the main gameplay screen. """
        super().__init__(*args, **kwargs)

        self.main_window = main_window

        self.players = None  # list[Player]
        self.current_player = None  # Player
        self.map = None  # Map
        self.last_player = None  # Player

        # Keep track of who did what when, so we can go back in case of a misclick
        self.starting_player = self.current_player
        self.actions = []

        self.init_gui()

    

######## Init functions ####################################################################################

    def init_gui(self):
        """ Builds the window. """
        # Player button line
        self.current_player_label = QLabel("'s turn")
        self.draw_cards_button = QPushButton("Draw cards")
        self.show_color_map = QCheckBox("Show color map")
        self.player_button_line = QHBoxLayout()
        self.player_button_line.addWidget(self.current_player_label)
        self.player_button_line.addWidget(self.draw_cards_button)
        self.player_button_line.addStretch()
        self.player_button_line.addWidget(self.show_color_map)

        # Map and players
        self.map_widget = MapWidget(self.main_window)
        self.players_last_action_label = QLabel()
        self.players_last_action_label.setFixedWidth(self.PlayersLabelWidth)
        self.map_and_players = QHBoxLayout()
        self.map_and_players.addWidget(self.map_widget)
        self.map_and_players.addWidget(self.players_last_action_label)

        self.general_layout = QVBoxLayout()
        self.general_layout.setContentsMargins(10, 0, 0, 0)
        self.general_layout.addLayout(self.player_button_line)
        self.general_layout.addWidget(self.map_widget)
        self.setLayout(self.general_layout)

        # Signals
        self.draw_cards_button.clicked.connect(self.draw_cards)
        self.show_color_map.toggled.connect(self.toggle_maps)


    def init_game(self, players: list[Player], map: Map):
        """ Initializes the game with players and map. """
        self.players = players
        self.current_player = players[0]
        self.map = map  # Map

        self.update_current_player_label()
        self.map_widget.init_with_map(self.map)
        self.main_window.setFixedSize(self.map.width+self.PlayersLabelWidth, self.map.height+100)



######## GUI functions ####################################################################################

    def toggle_maps(self):
        """ Toggles the map shown in map_widget between pretty and color. """
        if self.show_color_map.isChecked():
            self.map_widget.general_layout.setCurrentIndex(MapType.color.value)
        else:
            self.map_widget.general_layout.setCurrentIndex(MapType.pretty.value)

    def update_current_player_label(self):
        """ Updates self.current_player_label to correct name. """
        self.current_player_label.setText(f"{self.current_player.name}'s turn")
    
    def update_players_last_action_label(self):
        """ Updates self.players_last_action_label. """
        current_text_list = self.players_last_action_label.text().split("\n")
        print(current_text_list)



######## Gameplay functions ####################################################################################

    def next_player(self):
        """ Changes the turn to the next player. Finishes the game if it's done. """
        # If the game is done
        if self.last_player:
            if self.current_player == self.last_player:
                pass
                # Finish game

        # Set next player
        next_index = self.players.index(self.current_player)+1
        if next_index >= len(self.players):
            next_index = 0
        self.current_player = self.players[next_index]

        # Update current player label
        self.update_current_player_label()

        # Run AI if it's its turn
        if type(self.current_player) == AI:
            self.current_player.take_turn()


    def draw_cards(self):
        """ Makes AI draw cards if it's its turn, and goes to next player regardless. """
        self.next_player()


    def buy_route(self, route: Edge):
        """ Buys the specified route for self.current_player. """

        # Stop loop if we reached the final round
        if self.current_player.train_count <= 2:
            self.last_player = self.current_player

        self.next_player()
