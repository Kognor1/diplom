#!/usr/local/bin/python36
import sys

from PyQt5 import QtWebEngineWidgets, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from bokeh_fc import TestBokeh

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.form_widget = FormWidget(self)

        self.setGeometry(0,0,900,900)
        _widget = QWidget()
        _layout = QVBoxLayout(_widget)
        _layout.addWidget(self.form_widget)
        self.setCentralWidget(_widget)


class FormWidget(QWidget):
    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
       # self.__controls()
        self.__layout()

    def __controls(self):

        a=TestBokeh.TestBokeh()
        html= a.main()
        html.find("<head>")
        with open("test2.html","w")as f:
            f.write(html)
        #self.browser.setHtml(html)x`
        self.browser.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.JavascriptEnabled, True)
        self.browser.load(QUrl('file:///test2.html'))

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.webView = QtWebEngineWidgets.QWebEngineView()
        self.mainLayout.addWidget(self.webView, 100)
        self.webView.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.JavascriptEnabled, True)
        self.webView.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.LocalContentCanAccessRemoteUrls,
                                             True)
        self.webView.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.ErrorPageEnabled, True)
        self.webView.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, True)

        dev_view = QtWebEngineWidgets.QWebEngineView()
        self.mainLayout.addWidget(dev_view, 100)
        self.browser.page().setDevToolsPage(self.dev.page())
        # self.page().setDevToolsPage(self.browser.page())
    def __controls_test(self):
        self.browser.page().runJavaScript("""$("div:contains('Wiggle')").click()""")

    def __layout(self):
        self.vbox = QVBoxLayout()
        self.hBox = QVBoxLayout()
        self.getboundsbutton = QPushButton("Start Bokeh")
        self.test = QPushButton("Start JS Code")
        self.browser = QWebEngineView()
        self.dev = QWebEngineView()
       # self.hBox.addWidget(QWidget(),stretch=20)
        self.hBox.addWidget(self.browser,stretch=50)
       # self.hBox.addWidget(self.dev,stretch=20)
        self.hBox.addWidget(self.getboundsbutton,stretch=10)
        self.hBox.addWidget(self.test, stretch=20)
        self.vbox.addLayout(self.hBox)
        self.setLayout(self.vbox)

        self.getboundsbutton.clicked.connect(self.__controls)
        self.test.clicked.connect(self.__controls_test)


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()


if __name__ == '__main__':
    sys.exit(main())