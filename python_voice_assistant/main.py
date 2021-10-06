# This Python file uses the following encoding: utf-8

# import all dependencies
import sys

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PySide6.QtGui import QIcon, QPixmap


# create the our window class witch extend Qwidget class
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configure the window
        self.setWindowTitle("Voice Assistant")
        self.setFixedSize(QSize(800, 600))
        self.setWindowIcon(QIcon("img/girl.png"))
        self.setObjectName("theWindow")

        # Define a layout
        self.layout = QVBoxLayout(self)
        self.layout.setObjectName("layout")

        # Display the assistant representation image
        self.image = QLabel(self, alignment=Qt.AlignCenter)
        self.pixmap = QPixmap("img/girl.png")
        self.image.setPixmap(self.pixmap)

        # Add image widget to the layout
        self.layout.addWidget(self.image)



if __name__ == "__main__":

# Instantiate QApplication to run the loop
    app = QApplication(sys.argv)

# Instantiate MainWindow to launch the window
    window = MainWindow()
    window.show()

# Read the stylesheet
    with open("style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    app.exec()
