import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, qApp


class GAction(QAction):
    def __init__(self,parent):
        super().__init__('&G', parent)
        self.setIcon(QIcon(os.path.join("res","GIcon.png")))
        self.setShortcut('Ctrl+Q')
        self.setStatusTip('Exit application')
        self.triggered.connect(qApp.quit)