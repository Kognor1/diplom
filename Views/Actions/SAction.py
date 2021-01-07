import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, qApp


class SAction(QAction):
    def __init__(self,parent):
        super().__init__('&S', parent)
        self.setIcon(QIcon(os.path.join("res","SIcon.png")))
        self.setShortcut('Ctrl+Q')
        self.setStatusTip('Exit application')
        self.triggered.connect(qApp.quit)