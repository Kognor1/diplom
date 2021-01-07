import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, qApp, QFileDialog


class OpenFilesAction(QAction):
    def __init__(self, parent,trigger_func):
        super().__init__( '&Загрузить файлы', parent)
        self.setShortcut('Ctrl+O')
        self.setStatusTip('Open Files')
        self.triggered.connect(self.__open_file_dialog_load_data)
        self.__parent=parent
        self.__trigger_func=trigger_func

    def __open_file_dialog_load_data(self):
        path = QFileDialog.getOpenFileNames(self.__parent, 'Select Files', filter="Segy (*.segy *.sgy)")
        self.__trigger_func(path)
