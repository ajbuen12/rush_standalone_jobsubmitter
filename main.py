from functions import Commands
from PyQt4 import QtCore, QtGui
from ui import Ui_FarmStandAlone

import os
import sys
import functools


class Main(QtGui.QFrame, Ui_FarmStandAlone, Commands):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.button_send_blender.clicked.connect(functools.partial(self.send, 'blender'))
        self.button_send_maya.clicked.connect(functools.partial(self.send, 'maya'))
        self.button_send_max.clicked.connect(functools.partial(self.send, 'max'))
        self.button_send_ae.clicked.connect(functools.partial(self.send, 'ae'))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
