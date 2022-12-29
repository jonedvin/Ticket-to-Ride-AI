from PyQt6.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QLabel, QHBoxLayout, QVBoxLayout, QLineEdit, QComboBox, QPushButton
from extensions.player import Player, AI, PlayerColor
from extensions.maps import Map


class SelectionMenu(QWidget):
    NumberOfPlayers = 5
    TrainCount = 40

    def __init__(self, main_window, *args, **kwargs):
        """ Class for displaying the selection menu. """
        super().__init__(*args, **kwargs)

        self.main_window = main_window

        # Map section
        self.map_label = QLabel("Select map")

        self.map_select = QTreeWidget()
        self.map_select.setIndentation(5)
        self.map_select.headerItem().setHidden(True)

        self.map_section = QVBoxLayout()
        self.map_section.addWidget(self.map_label)
        self.map_section.addWidget(self.map_select)

        # Players section
        self.players_section = QVBoxLayout()

        self.players_label = QLabel("Add players")
        self.players_section.addWidget(self.players_label)

        self.players_column_labels = QHBoxLayout()
        self.players_column_labels.addWidget(QLabel("Name"))
        self.players_column_labels.addWidget(QLabel("Color"))
        self.players_column_labels.addWidget(QLabel("Type"))
        self.players_section.addLayout(self.players_column_labels)

        for _ in range(self.NumberOfPlayers):
            self.players_section.addLayout(QHBoxLayout())
            
            # Name
            self.players_section.itemAt(self.players_section.count()-1).addWidget(QLineEdit())

            # Colors
            self.players_section.itemAt(self.players_section.count()-1).addWidget(QComboBox())
            for color in PlayerColor:
                self.players_section.itemAt(self.players_section.count()-1).itemAt(1).widget().addItem(str(color).split(".")[1], color)

            # Types
            self.players_section.itemAt(self.players_section.count()-1).addWidget(QComboBox())
            self.players_section.itemAt(self.players_section.count()-1).itemAt(2).widget().addItem("None", None)
            self.players_section.itemAt(self.players_section.count()-1).itemAt(2).widget().addItem("Player", Player)
            self.players_section.itemAt(self.players_section.count()-1).itemAt(2).widget().addItem("AI", AI)

        self.players_section.addStretch()
        self.message_label = QLabel("")
        self.players_section.addWidget(self.message_label)

        self.button_line = QHBoxLayout()
        self.button_line.addStretch()
        self.confirm_button = QPushButton("Confirm")
        self.button_line.addWidget(self.confirm_button)
        self.players_section.addLayout(self.button_line)

        # Build window
        self.general_layout = QHBoxLayout()
        self.general_layout.addLayout(self.map_section)
        self.general_layout.addLayout(self.players_section)
        self.setLayout(self.general_layout)

        # Signals
        self.confirm_button.clicked.connect(self.confirm_game)


        # Add games
        self.map_select.addTopLevelItem(QTreeWidgetItem(["Europe"]))



    def confirm_game(self):
        """ Confirms the information provided, and starts the game if it's okay. """
        players = []

        item = 0
        start_index = 0

        # Find player one
        while type(item) != QHBoxLayout:
            item = self.players_section.itemAt(start_index)
            start_index += 1

        # Add all players
        for i in range(self.NumberOfPlayers):
            name = self.players_section.itemAt(start_index+i).itemAt(0).widget().text()
            color = self.players_section.itemAt(start_index+i).itemAt(1).widget().currentData()
            class_ = self.players_section.itemAt(start_index+i).itemAt(2).widget().currentData()

            if name and color and class_:
                players.append(class_(name, color, self.TrainCount))

        # Check that the info is valid
        if len(players) < 2:
            self.message_label.setText("Must be at least 2 players.")
            return
        colors = set()
        for player in players:
            colors.add(player.color)
        if len(colors) < len(players):
            self.message_label.setText("All players must have different colors.")
            return
        names = set()
        for player in players:
            names.add(player.name)
        if len(names) < len(players):
            self.message_label.setText("All players must have different names.")
            return

        # Start game
        self.main_window.gameplay_widget.init_game(players, Map(self.map_select.currentItem().text(0)))
        self.main_window.window_stack.setCurrentIndex(1)
