from PyQt6.QtWidgets import QWidget, QHBoxLayout, QMainWindow, QLabel, QApplication
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor, QImage
from PyQt6.QtCore import QPoint, QRect
from gui.selection_menu import SelectionMenu
from gui.gameplay import GameplayWidget
import sys
import numpy as np
import os


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.app = app

        # self.pixmap = QPixmap(500, 400)
        # self.pixmap.fill()
        # painter = QPainter(self.pixmap)
        # self.point_one = QPoint(100, 100)
        # self.point_two = QPoint(200, 50)
        # self.rect_ = QRect(self.point_one, self.point_two)
        # painter.drawRect(self.rect_)
        # painter.setPen(QPen(QColor("#ff0000")))

        # a = self.rect_.height()
        # b = self.rect_.width()
        # c = np.sqrt(a**2 + b**2)

        # angle = int(np.arccos(b/c))
        # painter.drawArc(self.rect_, angle*16, (angle+180)*16)

        

        self.pretty_canvas = QPixmap(os.path.join(os.path.dirname(os.path.abspath(__file__)), "maps/europe.jpg"))
        self.color_img = QImage(os.path.join(os.path.dirname(os.path.abspath(__file__)), "maps/europe_color.jpg"))

        self.label = QLabel()
        self.label.setPixmap(self.pretty_canvas)
        self.window_stack = QHBoxLayout()
        self.window_stack.addWidget(self.label)

        # Build window
        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self.window_stack)
        self.setCentralWidget(self.central_widget)


        self.draw_bought_trains()
    
    def draw_bought_trains(self):
        painter = QPainter(self.pretty_canvas)
        pen = QPen(QColor("#ff0000"))
        pen.setWidth(1)
        painter.setPen(pen)

        for y in range(self.color_img.height()):
            for x in range(self.color_img.width()):
                if QColor(self.color_img.pixel(x, y)).name() == "#461dc4":
                    painter.drawPoint(x, y)
        
        self.label.setPixmap(self.pretty_canvas)

        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(app)
    window.show()
    sys.exit(app.exec())