from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QCheckBox
from PyQt6.QtCore import Qt
from extensions.player import AI, Player, LastAction
from extensions.graph import Edge, TrackType, Color
from extensions.maps import Map
from gui.map_widget import MapWidget, MapType
import random


class GameplayWidget(QWidget):
    PlayersLabelWidth = 200

    def __init__(self, main_window, *args, **kwargs):
        """ Class for displaying the main gameplay screen. """
        super().__init__(*args, **kwargs)

        self.main_window = main_window

        self.players = None  # list[Player]
        self.current_player = None  # Player
        self.map = None  # Map
        self.last_player = None  # Player
        self.longest_name_count = 0

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
        self.draw_cards_button.setFixedHeight(30)
        self.show_color_map = QCheckBox("Show color map")
        self.player_button_line = QHBoxLayout()
        self.player_button_line.addWidget(self.current_player_label)
        self.player_button_line.addWidget(self.draw_cards_button)
        self.player_button_line.addStretch()
        self.player_button_line.addWidget(self.show_color_map)

        # Map and players
        self.map_widget = MapWidget(self)
        self.players_last_action_label = QLabel()
        self.players_last_action_label.setFixedWidth(self.PlayersLabelWidth)
        self.players_last_action_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.map_and_players = QHBoxLayout()
        self.map_and_players.addWidget(self.map_widget)
        self.map_and_players.addWidget(self.players_last_action_label)
        self.map_and_players.addStretch()

        self.general_layout = QVBoxLayout()
        self.general_layout.setContentsMargins(10, 0, 0, 0)
        self.general_layout.addLayout(self.player_button_line)
        self.general_layout.addLayout(self.map_and_players)
        self.setLayout(self.general_layout)

        # Signals
        self.draw_cards_button.clicked.connect(self.current_player_drew_cards)
        self.show_color_map.toggled.connect(self.toggle_maps)


    def init_game(self, players: list[Player], map: Map):
        """ Initializes the game with players and map. """
        self.players = players
        self.current_player = players[0]
        self.map = map  # Map

        for player in players:
            self.longest_name_count = max(len(player.name), self.longest_name_count)

            if type(player) == AI:
                player.set_gameplay_widget(self)
                player.draw_tickets(max_tickets=5, min_tickets=2)

        self.update_current_player_label()
        self.update_players_last_action_label()
        self.map_widget.init_with_map(self.map)

        # Set window size
        height = self.map_widget.pretty_canvas.rect().height() + self.draw_cards_button.rect().height() + 30
        width = self.map_widget.pretty_canvas.rect().width() + self.PlayersLabelWidth + 30
        self.main_window.setFixedSize(width, height)



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
        text = ""
        for player in self.players:
            last_action = player.last_action.name if player.last_action else ""
            text += f"{player.name+':': <10} {last_action}\n"
        
        # Show AI tickets and hand if debugging
        for player in self.players:
            if type(player) == AI and self.main_window.debug:
                text += f"\n\n{player.name}:"

                for ticket in player.tickets:
                    text += f"\n{ticket}"
                
                text += "\n"
                for color, count in player.hand.items():
                    text += f"\n{color}: {count}"

        self.players_last_action_label.setText(text)



######## Gameplay functions ####################################################################################

    def current_player_drew_cards(self):
        """ 
        Sets self.current_player.last_action to LastAction.drew_cards, 
        and runs self.next_player()
        """
        self.current_player.last_action = LastAction.drew_cards
        self.next_player()


    def next_player(self):
        """ Changes the turn to the next player. Finishes the game if it's done. """
        # If the game is done
        if self.last_player:
            if self.current_player == self.last_player:
                self.main_window.result_widget.show_results(self.players, self.map.edges)
                # self.main_window.window_stack.setCurrentIndex(2)

        # Set next player
        next_index = self.players.index(self.current_player)+1
        if next_index >= len(self.players):
            next_index = 0
        self.current_player = self.players[next_index]

        # Update current player label
        self.update_current_player_label()
        self.update_players_last_action_label()

        # Run AI if it's its turn
        if type(self.current_player) == AI:

            possible_route = self.current_player.take_turn()
            if type(possible_route) == Edge:
                self.buy_route(possible_route)
            else:
                self.next_player()


    def buy_route(self, route: Edge):
        """ Buys the specified route for self.current_player. """
        # AI block
        if type(self.current_player) == AI:

            # Check if they can buy tunnel
            extra_count = 0
            if route.track_type == TrackType.tunnel:
                for i in range(3):
                    if Color(random.randint(1, len(Color))) == route.color:
                        extra_count += 1
            
            if not self.current_player.has_enough_trains(route, extra_count=extra_count):
                self.current_player.last_action = LastAction.failed_tunnel
                self.next_player()
                return


            # Take cards for route
            self.current_player.hand[Color.locomotive] -= route.locomotive_count
            self.current_player.hand[route.color] -= route.length - route.locomotive_count
            if self.current_player.hand[route.color] < 0:
                self.current_player.hand[Color.locomotive] -= abs(self.current_player.hand[route.color])
                self.current_player.hand[route.color] = 0

        # Buy route
        route.bought_by = self.current_player
        self.current_player.train_count -= route.length
        self.current_player.bought_routes.append(route)

        # Display bought route
        self.map_widget.draw_bought_route(self.current_player, route)

        # Stop loop if we reached the final round
        if self.current_player.train_count <= 2:
            self.last_player = self.current_player

        # Check if AI has finished any tickets with this buy
        if type(self.current_player) == AI:
            for ticket in self.current_player.tickets:
                if not ticket.is_completed:
                    ticket.is_returning = False
                    ticket.check_if_complete(self.current_player)

        self.current_player.last_action = LastAction.bought_route
        self.next_player()
