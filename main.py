from extensions.player import Player, AI, PlayerColor
from extensions.maps import Map
from extensions.cards import Ticket
from PyQt6.QtWidgets import QApplication
from gui.main_gui import MainWindow
import sys


if __name__ == "__main__":

    # Start game
    # map = Map("Europe")
    # game = Game(players, map)
    # game.run()



    ##### GUI #######################################
    app = QApplication(sys.argv)

    # Start app
    window = MainWindow(app)

    # Testing block
    jon = Player("Jon", PlayerColor.black, 42)
    sheila = Player("Sheila", PlayerColor.yellow, 42)
    ai = AI("AI", PlayerColor.green, 42)
    window.gameplay_widget.init_game([jon, sheila, ai], Map("Europe"))
    window.window_stack.setCurrentIndex(1)

    # AI testig block
    # stockholm = None
    # essen = None
    # petrograd = None
    # wien = None
    # for node in window.gameplay_widget.map_widget.map.nodes:
    #     if node.name == "Stockholm":
    #         stockholm = node
    #     elif node.name == "Essen":
    #         essen = node
    #     elif node.name == "Petrograd":
    #         petrograd = node
    #     elif node.name == "Wien":
    #         wien = node

    # ai.tickets.append(Ticket(essen, petrograd, 15))
    # ai.tickets.append(Ticket(wien, petrograd, 17))
    # ai.find_optimal_path_set()
    # print()
    # print("Best path:")
    # print(ai.best_path_set)

    window.show()
    sys.exit(app.exec())