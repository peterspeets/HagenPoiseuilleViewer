import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


from graph import *
from buttons import *


class Layout(QWidget):
    def __init__(self, parent=None, window = None):
        super().__init__(parent)
        self.window = window
        self.layout = QGridLayout(self)
        self.buttons = Buttons(window = self.window)
        self.crossSection = CrossSection()
        self.heightProfileGraph = Graph()
        self.widthProfileGraph = Graph()
        self.heightProfileGraph.color = 'r'
        self.widthProfileGraph.color = 'b'
        
        self.layout.addWidget(self.crossSection,0,0)
        self.layout.addWidget(self.heightProfileGraph,0,1)
        self.layout.addWidget(self.widthProfileGraph,1,0)
        self.layout.addWidget(self.buttons,1,1)
        
        self.heightProfileGraph.ax.set_xlabel('Distance (mm)')
        self.heightProfileGraph.ax.set_ylabel('Flow speed (mm/s)')
        self.heightProfileGraph.ax.set_title('Flow profile along z axis')
        
        self.widthProfileGraph.ax.set_xlabel('Distance (mm)')
        self.widthProfileGraph.ax.set_ylabel('Flow speed (mm/s)')
        self.widthProfileGraph.ax.set_title('Flow profile along y axis')
        


