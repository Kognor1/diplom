#!/usr/local/bin/python36
import os
import sys
from PyQt5 import QtWebEngineWidgets, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

from Views import ExitAction, OpenFilesAction, GAction, SAction
from Views.Controllers import BokehController
from bokeh_fc import TestBokeh
from string import Template

from Views.Widgets import BokehWidget, SelectFileDataWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__bokeh_controller = BokehController(self)
        _widget = MainWidget(self.__bokeh_controller)
        self.setGeometry(0, 0, 1600, 900)
        self.setCentralWidget(_widget)


class MainWidget(QWidget):
    def __init__(self, __bokeh_controller, parent=None):
        super(MainWidget, self).__init__(parent, )
        self.__select_data_widget = SelectFileDataWidget(self.click_data)
        self.main_v_layout = QVBoxLayout()
        self.main_h_layout = QHBoxLayout()
        self.main_v_layout.addWidget(self.__generate_menu_bar())
        self.main_v_layout.addWidget(self.__generate_tool_bar())

        self.main_h_layout.addWidget(self.__select_data_widget, stretch=25)
        # TODO хз по идее контролера здесь не должно быть во  view, но как тогда пробросить фк клика на
        self.__bokeh_controller = __bokeh_controller
        self.bokeh_widget = self.__bokeh_controller.get_bokeh_widget()
        self.main_h_layout.addWidget(self.bokeh_widget, stretch=75)
        self.main_v_layout.addLayout(self.main_h_layout)
        self.setLayout(self.main_v_layout)

    def __generate_menu_bar(self):
        self.__main_menu_bar = QMenuBar()
        self.__main_menu_bar_menu = self.__main_menu_bar.addMenu('&Menu')
        self.__main_menu_ba_normalize = self.__main_menu_bar.addMenu('&Normalize Data')
        self.__main_menu_bar_filtering = self.__main_menu_bar.addMenu('&Filtering')
        self.__main_menu_bar_layout = self.__main_menu_bar.addMenu('&Layout')
        self.__main_menu_bar_print_seism = self.__main_menu_bar.addMenu('&Print Seismogram')

        self.__main_menu_bar_menu.addAction(
            OpenFilesAction(self,
                            self.__select_data_widget.get_open_file_dialog_load_data_func())
        )

        self.__main_menu_bar_menu.addAction(ExitAction(self))
        self.__main_menu_ba_normalize.addAction(ExitAction(self))
        self.__main_menu_bar_filtering.addAction(ExitAction(self))
        self.__main_menu_bar_layout.addAction(ExitAction(self))
        self.__main_menu_bar_print_seism.addAction(ExitAction(self))

        return self.__main_menu_bar

    def __generate_tool_bar(self):
        self.toolbar = QToolBar()  # self.addToolBar('Exit')
        self.toolbar.addAction(GAction(self))
        self.toolbar.addAction(SAction(self))
        self.toolbar.addAction(ExitAction(self))
        return self.toolbar

    def click_data(self, currentItem):
        self.path_name = currentItem
        self.__bokeh_controller.add_tab(currentItem)


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()


if __name__ == '__main__':
    sys.exit(main())
