from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from functions import *
from urllib.parse import *
from getToken import *
import requests
import keyboard
import time
import pygame
import json
import win32gui
import os
import sys


class QizyLineEdit(QLineEdit):
    def __init__(self, topFrame):
        super(QizyLineEdit, self).__init__()

        self.topFrameTmp = topFrame

    def focusOutEvent(self, QFocusEvent):
        while self.topFrameTmp.processRunning:
            print(self.topFrameTmp.processRunning)

        import threading
        process = threading.Thread(target=updateDialogStatus, args=(self.topFrameTmp.parent,))
        process.start()

        if self.topFrameTmp.isHidden() == 0:
            self.topFrameTmp.hide()


class mainWidgets(QDialog):
    def __init__(self, parent, getSelectedWord):
        super(mainWidgets, self).__init__()

        self.parent = parent
        self.parent.noDialogRunning = 0
        self.processRunning = 1

        self.initWidgets()

        self.initWindow()

        self.initShortCuts()

        if getSelectedWord:
            clipboard = QGuiApplication.clipboard()

            self.contentEdit.setText(clipboard.text())

            self.query()

        self.processRunning = self.processRunning - 1

    def initWindow(self):
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setWindowTitle("qTranslater - Dialog")

        self.show()
        #self.activateWindow()

        while self.raiseWindow() == False:
            print("calling win32gui api failed")

    def initShortCuts(self):
        pronounceAction = QShortcut(QKeySequence("Ctrl+P"), self)
        pronounceAction.activated.connect(self.pronounce)

        exitAction = QShortcut(QKeySequence("Ctrl+E"), self)
        exitAction.activated.connect(self.close)

        self.closeCurrentDialogAction = QShortcut(QKeySequence("Ctrl+Space"), self)
        self.closeCurrentDialogAction.activated.connect(self.hide)

    def initWidgets(self):
        self.currentWord = ""

        self.resultShow = QLabel()

        self.contentEdit = QizyLineEdit(self)
        self.contentEdit.returnPressed.connect(self.query)
        self.contentEdit.setFocus()

        self.MainGrid = QGridLayout()
        self.MainGrid.setSpacing(10)

        self.MainGrid.addWidget(self.contentEdit, 1, 1)
        self.MainGrid.addWidget(self.resultShow, 2, 1)

        self.setLayout(self.MainGrid)

    def raiseWindow(self):
        self.processRunning = self.processRunning + 1

        try:
            windowID = win32gui.FindWindow(None, "qTranslater - Dialog")
            win32gui.SetForegroundWindow(windowID)
            self.processRunning = self.processRunning - 1
            return True
        except:
            self.processRunning = self.processRunning - 1
            return False

    def pronounce(self):
        self.processRunning = self.processRunning + 1

        if self.currentWord != self.contentEdit.text():
            self.query()

        text = self.contentEdit.text()

        acquirer = TokenAcquirer()
        tk = acquirer.do(text)
        text = quote(text)
        url = "https://translate.google.cn/translate_tts?ie=UTF-8&q=" + text + "&tl=en&total=1&idx=0&textlen=10&tk=" + str(
            tk) + "&client=t"

        try:
            doc = requests.get(url)
            with open(".\Audios\pronunciation.mp3", 'wb') as f:
                f.write(doc.content)

            pygame.mixer.init()
            pygame.mixer.music.load(".\Audios\pronunciation.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pass
            pygame.mixer.music.load(".\Audios\EmptyFile.mp3")
        except:
            print("pronounce failed")

        self.processRunning = self.processRunning - 1

    def query(self):
        self.processRunning = self.processRunning + 1

        text = self.contentEdit.text()
        self.currentWord = text

        acquirer = TokenAcquirer()
        tk = acquirer.do(text)
        text = quote(text)
        url = "https://translate.google.cn/translate_a/single?client=t&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&otf=2&ssel=0&tsel=0&kc=1&tk=" + str(
            tk) + "&q=" + text

        doc = requests.get(url)

        textDisplay = ""

        try:
            textDisplay = doc.json()[0][0][0]
            textDisplay = textDisplay + "\n\n"
        except:
            pass

        try:
            doc = doc.json()[1]

            for partOfSpeech in doc:
                textDisplay = textDisplay + str(partOfSpeech[0]) + "\n"
                for meanings in partOfSpeech[1]:
                    textDisplay = textDisplay + "  " + str(meanings) + "\n"
        except:
            pass

        if textDisplay == "":
            textDisplay = "Words Not Found"

        self.resultShow.setText(textDisplay)

        self.processRunning = self.processRunning - 1


class backgroundProgram(QMainWindow):
    def __init__(self):
        super(backgroundProgram, self).__init__()

        self.initTrayIcon()

        self.initShortcut()

        self.noDialogRunning = 1

    def initShortcut(self):
        keyboard.add_hotkey("Ctrl+Space", self.showDialog)
        keyboard.add_hotkey("Ctrl+Shift", self.showDialogWithSelectedWord)

    def initTrayIcon(self):
        icon = QIcon("icon.ico")

        menu = QMenu(self)
        menu.addAction("exit", self.close)
        menu.addAction("about", self.AboutThisProject)

        SystemTrayIcon = QSystemTrayIcon(icon, self)

        SystemTrayIcon.setContextMenu(menu)

        SystemTrayIcon.show()

    def showDialog(self):
        if self.noDialogRunning:
            MainProg = mainWidgets(self, 0)
            MainProg.exec_()

    def showDialogWithSelectedWord(self):
        if self.noDialogRunning:
            time.sleep(0.2)

            try:
                keyboard.press_and_release("Ctrl+C")
            except:
                print("calling keyboard api failed...")

            time.sleep(0.1)

            MainProg = mainWidgets(self, 1)
            MainProg.exec_()

    def AboutThisProject(self):
        if self.noDialogRunning:
            AboutPageDialog = AboutPage(self)
            AboutPageDialog.exec_()


class AboutPage(QDialog):
    def __init__(self, parent):
        super(AboutPage, self).__init__()

        self.parent = parent
        self.parent.noDialogRunning = 0

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

        self.show()

    def hideEvent(self, QHideEvent):
        self.parent.noDialogRunning = 1
