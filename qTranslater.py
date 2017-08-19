import sys
from PyQt5.QtWidgets import *
from classes import *

if __name__ == "__main__":
    app = QApplication(sys.argv)

    MainProg = baseFrame()

    sys.exit(app.exec_())

#https://github.com/FindHao/ciba/blob/master/entry.py
