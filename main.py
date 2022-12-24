from extensions.player import Player, AI, PlayerColor
from extensions.game import Game
from extensions.maps import Map
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
    window.game = Game([jon, sheila, ai], Map("Europe"))
    window.window_stack.setCurrentIndex(1)

    window.show()
    sys.exit(app.exec())