import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from icons import *
from graph import *
from layout import *
from settings import *
from poiseuille import *


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__(parent=None)
        self.icons = Icons()
        self.setWindowIcon(self.icons.windowIcon)        
        self.setWindowTitle("Hagen-Poiseuille Viewer for Rectangular Flows")
        app = QApplication(sys.argv)
        self.settings = Settings(sys.path[0] + '\\settings\\lastSettings.yaml')
        self.setGeometry(*self.settings.windowSize)
        
        
        
        
        self.poiseuilleCalculator = PoiseuilleCalculator(self)
        
        
        self.figures = Layout(window = self)
        self.setCentralWidget(self.figures)
        
        #self.figures.heightProfileGraph.updateGraph(self.poiseuilleCalculator.z, self.poiseuilleCalculator.zProfile)
        #self.figures.widthProfileGraph.updateGraph(self.poiseuilleCalculator.y, self.poiseuilleCalculator.yProfile)
        self.updateGraphs()
        self._createMenu()



    def _createMenu(self):

        menu = self.menuBar().addMenu("&Menu")

        menu.addAction("&Exit", self.close)

    def closeEvent(self,event):
        """Destructor of window. Saves settings to yaml file."""
        self.settings.windowSize = list(self.geometry().getRect())
        print(list(self.geometry().getRect()))
        self.settings.saveLastUsedSettings()

    def updateGraphs(self):
        self.figures.heightProfileGraph.updateGraph(self.poiseuilleCalculator.z,self.poiseuilleCalculator.zProfile)
        self.figures.widthProfileGraph.updateGraph(self.poiseuilleCalculator.y,self.poiseuilleCalculator.yProfile)
        self.figures.crossSection.updateGraph(self.poiseuilleCalculator.calculateYZCrossSection,self.settings.channelHeight,
        self.settings.channelWidth, self.settings.z0, self.settings.y0)

