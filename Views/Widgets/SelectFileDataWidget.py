import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QHeaderView, \
    QTableWidgetItem, QComboBox, QCheckBox, QToolButton, QSizePolicy

from Views.Actions import OpenFilesAction
from . import WidgetWrapper


class SelectFileDataWidget(QWidget):
    def __init__(self, outer_fk):
        super().__init__()
        self.outer_fk = outer_fk
        self.tabWidget = QTabWidget()
        self.vbox = QVBoxLayout()
        self.__files_tab = QWidget()
        self.__files_tab.setLayout(self.__create_files_tab_layout())
        self.tabWidget.addTab(self.__files_tab, 'Files List')
        self.__opened_files = {}
        self.vbox.addWidget(self.tabWidget)
        self.setLayout(self.vbox)

    def __create_files_tab_layout(self):
        self.hor_layout = QVBoxLayout()
        self.label = QLabel("SEISMOGRAM FILES")
        self.__open_folder_btn = QToolButton(self)
        __open_folder_btn_size_policy= QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.__open_folder_btn.setSizePolicy(__open_folder_btn_size_policy)
        self.__open_folder_btn.setDefaultAction(OpenFilesAction(self, self._load_data))
        self.hor_layout.addWidget(self.label)
        self.hor_layout.addWidget(self.__open_folder_btn)

        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["File", "Type", "Fix"])
        self.table.cellClicked.connect(self.__cell_click)
        self.table_header = self.table.horizontalHeader()
        self.table_header.setSectionResizeMode(0, QHeaderView.Stretch)
        self.table_header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table_header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        self.hor_layout.addWidget(self.table)
        return self.hor_layout

    def _load_data(self, path):
        for i in path[0]:
            _, name = os.path.split(i)

            if (not name in self.__opened_files.keys()):
                self.__opened_files[name] = i
                self.add_row(name)

    def get_open_file_dialog_load_data_func(self):
        return self._load_data

    def add_row(self, filename):
        row = self.table.rowCount()
        self.table.setRowCount(row + 1)
        cell = QTableWidgetItem(str(filename))
        qc = QComboBox()
        qchb = QHBoxLayout()
        qchb.addWidget(QCheckBox())
        qchb.setAlignment(Qt.AlignCenter)
        chkBoxItem = QTableWidgetItem()
        chkBoxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        chkBoxItem.setCheckState(Qt.Unchecked)

        qc.addItem("Null")
        qc.addItem("None")
        self.table.setItem(row, 0, cell)
        self.table.setCellWidget(row, 1, qc)
        self.table.setCellWidget(row, 2, WidgetWrapper.WidgetWrapper(qchb))
        # self.table.setItem(row, 2, chkBoxItem)

    def __cell_click(self, *args, **kwargs):
        if args[1] == 0:
            self.outer_fk(self.__opened_files[self.table.item(args[0], args[1]).text()])
