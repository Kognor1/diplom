import os

from Views import BokehWidget
from bokeh_fc.TestBokeh import TestBokeh


class BokehController():

    def __init__(self,mainWindow):
        self.open_tabs={}
        self.__bokeh_widget= BokehWidget(mainWindow)
        pass
    def get_bokeh_widget(self):
        return self.__bokeh_widget
    def add_tab(self,filename):
        _, name = os.path.split(filename)
        if( name in self.open_tabs.keys()):
            self.__bokeh_widget.select_tab(self.open_tabs[name])
            return False
        else:
            a = TestBokeh(filename)
            script, div = a.main()
            self.open_tabs[name]=self.__bokeh_widget.get_tab(name,script,div,a.bin_head["Traces"],a.bin_head["Interval"],filename)
            self.__bokeh_widget.select_tab(self.open_tabs[name])
            return True

    def delete_tab(self,filename):
        pass