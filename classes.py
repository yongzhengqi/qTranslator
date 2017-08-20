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

        self.initShortcut()

        self.initWindow()

        self.initTrayIcon()

    def initTrayIcon(self):
        icon = QIcon("icon.ico")

        menu = QMenu(self)
        menu.addAction("exit", self.close)
        menu.addAction("about", self.AboutThisProject)

        SystemTrayIcon = QSystemTrayIcon(icon, self)

        SystemTrayIcon.setContextMenu(menu)

        SystemTrayIcon.show()

    def initWindow(self):
        self.mainWidget = mainWidgets(self)
        self.setCentralWidget(self.mainWidget)

        # self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setWindowTitle("qTranslater")
        self.setGeometry(300, 300, 400, 200)

        self.show()

    def initShortcut(self):
        exitAction = QShortcut(QKeySequence("Ctrl+E"), self)
        exitAction.activated.connect(self.close)

        keyboard.add_hotkey("Ctrl+Space", self.hideOrShow)

    def hideOrShow(self):
        if self.isHidden():
            self.show()
            raiseWindow("qTranslater", self)

            self.setGeometry(300, 300, 400, 200)
            self.mainWidget.contentEdit.clear()
        else:
            self.hide()

        time.sleep(0.1)

    def AboutThisProject(self):
        AboutPageDialog = AboutPage()
        AboutPageDialog.exec_()


class AboutPage(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("About qTranslater")
        self.setWindowIcon(QIcon("icon.ico"))
        self.setWindowFlags(Qt.FramelessWindowHint)

        ProjectPageGuide = QLabel("Project Page:")
        ProjectPageLink = QLabel(
            """<a href="https://github.com/yongzhengqi/qTranslater">https://github.com/yongzhengqi/qTranslater</a>""")
        ProjectPageLink.setOpenExternalLinks(True)

        ProjectLicenseGuide = QLabel("Project License:")
        ProjectLicense = QLabel(
            """<a href="https://en.wikipedia.org/wiki/MIT_License" target="_blank">MIT License</a>""")
        ProjectLicense.setOpenExternalLinks(True)

        ExitButton = QPushButton("确定")
        ExitButton.clicked.connect(self.hide)

        GridLayout = QGridLayout()
        self.setLayout(GridLayout)
        GridLayout.addWidget(ProjectPageGuide, 1, 1)
        GridLayout.addWidget(ProjectPageLink, 1, 2)
        GridLayout.addWidget(ProjectLicenseGuide, 2, 1)
        GridLayout.addWidget(ProjectLicense, 2, 2)
        GridLayout.addWidget(ExitButton, 3, 1, 1, 3)
