from urllib.parse import *
from getToken import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import requests
import pygame
import json


def rshift(val, n):
    """python port for '>>>'(right shift with padding)
    """
    return (val % 0x100000000) >> n


def pronounce(text, mainWindow):
    acquirer = TokenAcquirer()
    tk = acquirer.do(text)
    text = quote(text)
    url = "https://translate.google.cn/translate_tts?ie=UTF-8&q=" + text + "&tl=en&total=1&idx=0&textlen=10&tk=" + str(
        tk) + "&client=t"

    try:
        print(url)
        doc = requests.get(url)
        # mainWindow.statusBar().showMessage("downloading audio file done...", 2000)
        with open(".\Audios\pronunciation.mp3", 'wb') as f:
            f.write(doc.content)
        # mainWindow.statusBar().showMessage(".mp3 file ready...", 2000)

        pygame.mixer.init()
        pygame.mixer.music.load(".\Audios\pronunciation.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            print("playing audio...")
        pygame.mixer.music.load(".\Audios\EmptyFile.mp3")
    except:
        pass


def query(text, resultShow, statusBar):
    acquirer = TokenAcquirer()
    tk = acquirer.do(text)
    text = quote(text)
    url = "https://translate.google.cn/translate_a/single?client=t&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&otf=2&ssel=0&tsel=0&kc=1&tk=" + str(
        tk) + "&q=" + text

    print(url)
    doc = requests.get(url)
    print("request done...")

    try:
        doc = doc.json()[1]

        textDisplay = ""

        for partOfSpeech in doc:
            textDisplay = textDisplay + str(partOfSpeech[0]) + "\n"
            for meanings in partOfSpeech[1]:
                textDisplay = textDisplay + "  " + str(meanings) + "\n"

        resultShow.setText(textDisplay)
    except:
        resultShow.setText("")
        # doc = json.dumps(doc, indent=1)
        # doc = doc.encode().decode('unicode_escape')
        # print(doc)
