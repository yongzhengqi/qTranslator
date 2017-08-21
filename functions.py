from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time


def rshift(val, n):
    return (val % 0x100000000) >> n


def updateDialogStatus(targetClass):
    time.sleep(0.5)
    targetClass.noDialogRunning = 1
