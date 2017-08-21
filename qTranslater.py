import sys
from PyQt5.QtWidgets import *
from classes import *
from functions import *
from tendo import singleton

if __name__ == "__main__":
    # to make sure that there is only one instance of this program
    currentInstance = singleton.SingleInstance()

    app = QApplication(sys.argv)

    MainProg = backgroundProgram()

    sys.exit(app.exec_())

