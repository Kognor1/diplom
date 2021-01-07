import os
from string import Template

from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QLabel


class BokehWidget(QTabWidget):
    class BokehTab(QWidget):
        def __init__(self, nameTab, script, div, time, trace, path):
            super().__init__()
            self.vbox = QVBoxLayout()
            self.hBox = QVBoxLayout()
            self.__info_data_label = QLabel(
                "File: {0};   Time: {1};   Trace: {2};  Path:  {3}".format(nameTab, time, trace, path))
            self.browser = QWebEngineView()
            self.dev = QWebEngineView()
            self.script = script
            self.div = div
            self.name = nameTab
            self.hBox.addWidget(self.browser, stretch=75)
            self.hBox.addWidget(self.dev, stretch=20)
            self.hBox.addWidget(self.__info_data_label, stretch=5)
            # self.hBox.addWidget(self.test, stretch=20)
            self.vbox.addLayout(self.hBox)

            self.controls()
            self.setLayout(self.vbox)

        def controls(self):
            with open(os.path.join("temp", "template.html"), "r")as f:
                template = f.read()
            t = Template(template)
            content = t.substitute(bokeh_script=str(self.script), bokeh_div=str(self.div))
            with open("{}.html".format(os.path.join("temp", self.name)), "w") as f:
                f.write(content)
            self.browser.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.JavascriptEnabled, True)
            self.browser.load(QUrl('file:///{}.html'.format("temp/" + self.name)))  # TODO проверить на linux
            self.browser.page().setDevToolsPage(self.dev.page())

        def __controls_test(self):
            self.browser.page().runJavaScript("""$("div:contains('Wiggle')").click()""")

    def __init__(self, parent):
        super(BokehWidget, self).__init__(parent)

    # def controls(self,browser,dev):
    #     with open("template.html","r")as f:
    #          template = f.read()
    #     t = Template(template)
    #     content = t.substitute(bokeh_script=str(self.script), bokeh_div=str(self.div))
    #     with open("workZone_{}.html".format(self.name),"w") as f:
    #         f.write(content)
    #     self.browser.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.JavascriptEnabled, True)
    #     self.browser.load(QUrl('file:///workZone_{}.html'.format(self.name)))
    #     self.browser.page().setDevToolsPage(self.dev.page())

    # def __controls_test(self):
    #     self.browser.page().runJavaScript("""$("div:contains('Wiggle')").click()""")

    def get_tab(self, nameTab, script, div, time, trace, path):
        tab = BokehWidget.BokehTab(nameTab, script, div, time, trace, path)
        self.addTab(tab, nameTab)
        return tab

    def select_tab(self, tab):
        self.setCurrentWidget(tab)
