from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
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