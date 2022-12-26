from PyQt6.QtWidgets import QWidget, QStackedLayout, QMainWindow
from gui.selection_menu import SelectionMenu
from gui.gameplay import GameplayWidget
import enum


class Display(enum.Enum):
    selection = 0
    main = 1


class MainWindow(QMainWindow):
    # Constants
    WindowWidth = 1100
    WindowHeight = 600

    def __init__(self, app):
        """
        The main window of the application.
        """
        super().__init__()

        self.app = app
        self.game = None

        # Window parametres
        self.setWindowTitle('AdminGUI')
        self.resize(self.WindowWidth, self.WindowHeight)
        self.move(60, 60)
        self.setMinimumHeight(200)

        # Window stack
        self.selection_widget = SelectionMenu(self)
        self.gameplay_widget = GameplayWidget(self, self.game)
        self.window_stack = QStackedLayout()
        self.window_stack.addWidget(self.selection_widget)
        self.window_stack.addWidget(self.gameplay_widget)

        # Build window
        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self.window_stack)
        self.setCentralWidget(self.central_widget)


        # Signals



    def closeEvent(self, event):
        """ Overrides closeEvent to quit entire program if main window is closed. """
        event.accept()
        self.app.quit()