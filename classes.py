from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from functions import *
import os


class Main(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("qTranslater")
        self.setWindowIcon(QIcon("icon.png"))

        self.InitWidget()

        self.setLayout(self.MainGrid)
        self.show()

    def InitWidget(self):
        contentLabel = QLabel("Words：")

        self.resultShow = QLabel()

        contentEdit = QLineEdit()
        contentEdit.returnPressed.connect(lambda: query(contentEdit.text(), self.resultShow, self))

        speakButton = QPushButton("pronounce")
        speakButton.clicked.connect(lambda: pronounce(contentEdit.text(), self))

        self.MainGrid = QGridLayout()
        self.MainGrid.setSpacing(10)

        self.MainGrid.addWidget(contentLabel, 1, 1)
        self.MainGrid.addWidget(contentEdit, 1, 2)
        self.MainGrid.addWidget(speakButton, 1, 3)
        self.MainGrid.addWidget(self.resultShow, 2, 1)

