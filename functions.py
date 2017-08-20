from urllib.parse import *
from getToken import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import requests
import pygame
import json
import win32gui


def rshift(val, n):
    return (val % 0x100000000) >> n


def query(fatherFrame, topFrame):
    text = fatherFrame.contentEdit.text()
    fatherFrame.currentWord = text
    resultShow = fatherFrame.resultShow

    topFrame.statusBar().showMessage("Generating Token...", 2000)
    acquirer = TokenAcquirer()
    tk = acquirer.do(text)
    text = quote(text)
    url = "https://translate.google.cn/translate_a/single?client=t&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&otf=2&ssel=0&tsel=0&kc=1&tk=" + str(
        tk) + "&q=" + text
    topFrame.statusBar().showMessage("Generating Token done", 2000)

    topFrame.statusBar().showMessage("Requesting from google.cn...", 2000)
    doc = requests.get(url)
    topFrame.statusBar().showMessage("Requesting done", 2000)

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

    resultShow.setText(textDisplay)


def pronounce(fatherFrame, topFrame):
    if fatherFrame.currentWord != fatherFrame.contentEdit.text():
        query(fatherFrame, topFrame)

    text = fatherFrame.contentEdit.text()

    topFrame.statusBar().showMessage("Generating Token...", 2000)
    acquirer = TokenAcquirer()
    tk = acquirer.do(text)
    text = quote(text)
    url = "https://translate.google.cn/translate_tts?ie=UTF-8&q=" + text + "&tl=en&total=1&idx=0&textlen=10&tk=" + str(
        tk) + "&client=t"
    topFrame.statusBar().showMessage("Generating Token done", 2000)

    try:
        topFrame.statusBar().showMessage("Requesting from google.cn...", 2000)
        doc = requests.get(url)
        with open(".\Audios\pronunciation.mp3", 'wb') as f:
            f.write(doc.content)
        topFrame.statusBar().showMessage("Requesting done", 2000)

        pygame.mixer.init()
        pygame.mixer.music.load(".\Audios\pronunciation.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            topFrame.statusBar().showMessage("Playing audios...")
        topFrame.statusBar().showMessage("Playing audios done", 2000)
        pygame.mixer.music.load(".\Audios\EmptyFile.mp3")
    except:
        topFrame.statusBar().showMessage("Can't pronounce this word.", 2000)


def raiseWindow(name):
    print("raiseing windows...")
    windowID = win32gui.FindWindow(None, name)
    win32gui.SetForegroundWindow(windowID)
    print("raiseing done")
