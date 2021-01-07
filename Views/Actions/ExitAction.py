from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, qApp


class ExitAction(QAction):
    def __init__(self,parent):
        super().__init__('&Exit', parent)
        self.setShortcut('Ctrl+Q')
        self.setStatusTip('Exit application')
        self.triggered.connect(qApp.quit)