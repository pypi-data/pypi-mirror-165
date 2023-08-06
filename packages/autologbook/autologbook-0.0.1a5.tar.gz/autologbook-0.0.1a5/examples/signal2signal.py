# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 15:45:31 2022

@author: Antonio
"""


import sys

from main_test_ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow

Signal = QtCore.pyqtSignal
Slot = QtCore.pyqtSlot


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class MyObj(QtCore.QObject):
    mySignal = Signal(str)

    def emit_mySignal(self):
        self.mySignal.emit('message')


def main():
    app = QApplication(sys.argv)
    win = MainWindow()

    # show the main window
    win.show()

    my_obj = MyObj()
    win.pushButton.pressed.connect(lambda: my_obj.mySignal.emit('daniele'))
    # win.pushButton.clicked.connect(win.lineEdit.setEnabled)

    my_obj.mySignal.connect(win.lineEdit.setText)

    # execute the main window and eventually exit when done!
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
