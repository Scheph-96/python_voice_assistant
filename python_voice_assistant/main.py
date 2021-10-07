# This Python file uses the following encoding: utf-8

# import all dependencies
import sys

from PySide6.QtWidgets import QApplication
from util.GUI.GUI import MainWindow


if __name__ == "__main__":
    # Instantiate QApplication to run the loop
    app = QApplication(sys.argv)

    # Instantiate MainWindow to launch the window
    window = MainWindow()
    window.show()

    # Read the stylesheet
    with open("util/GUI/style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    app.exec()
