from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from functions import *
import keyboard
import time
import os


class QizyLineEdit(QLineEdit):
    def __init__(self, topFrame):
        super(QizyLineEdit, self).__init__()

        self.topFrameTmp = topFrame

    def focusOutEvent(self, QFocusEvent):
        if self.topFrameTmp.isHidden() == False:
            self.topFrameTmp.hide()

class mainWidgets(QWidget):
    def __init__(self, topFrame):
        super(mainWidgets, self).__init__()

        self.InitWidgets(topFrame)

        self.initShortCuts(topFrame)

    def initShortCuts(self, topFrame):
        pronounceAction = QShortcut(QKeySequence("Ctrl+P"), self)
        pronounceAction.activated.connect(lambda: pronounce(self, topFrame))

    def InitWidgets(self, topFrame):
        contentLabel = QLabel("Words：")

        self.currentWord = ""

        self.resultShow = QLabel()

        self.contentEdit = QizyLineEdit(topFrame)
        self.contentEdit.returnPressed.connect(lambda: query(self, topFrame))
        self.contentEdit.setFocus()

        speakButton = QPushButton("pronounce")
        speakButton.setFocusPolicy(Qt.NoFocus)
        speakButton.clicked.connect(lambda: pronounce(self, topFrame))

        self.MainGrid = QGridLayout()
        self.MainGrid.setSpacing(10)

        self.MainGrid.addWidget(contentLabel, 1, 1)
        self.MainGrid.addWidget(self.contentEdit, 1, 2)
        self.MainGrid.addWidget(speakButton, 1, 3)
        self.MainGrid.addWidget(self.resultShow, 2, 1, 1, 3)

        self.setLayout(self.MainGrid)


class baseFrame(QMainWindow):
    def __init__(self):
        super(baseFrame, self).__init__()

        self.mainWidget = mainWidgets(self)

        self.setCentralWidget(self.mainWidget)

        #self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.FramelessWindowHint)

        exitAction = QShortcut(QKeySequence("Ctrl+E"), self)
        exitAction.activated.connect(self.close)

        keyboard.add_hotkey("Ctrl+Space", self.hideOrShow)

        self.setWindowTitle("qTranslater")
        self.setGeometry(300, 300, 400, 200)

        self.show()

    def hideOrShow(self):
        if self.isHidden():
            self.show()
            raiseWindow("qTranslater")

            self.setGeometry(300, 300, 400, 200)
            self.mainWidget.contentEdit.clear()
        else:
            self.hide()

        time.sleep(0.1)
