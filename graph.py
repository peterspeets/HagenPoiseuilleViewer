import sys

import numpy as np
from scipy.stats import norm
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Graph(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        #  create widgets
        self.view = FigureCanvas(Figure(figsize=(5, 3)))
        self.ax = self.view.figure.subplots()
        self.toolbar = NavigationToolbar2QT(self.view, self)
        
        self.ax.set_xlabel('Distance (mm)')
        self.ax.set_ylabel('Flow speed (mm/s)')
        self.ax.set_title('$title')
        self.color = 'r'
        self.ax.grid()


        #  Create layout
        input_layout = QHBoxLayout()
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.toolbar)
        vlayout.addWidget(self.view)
        vlayout.addLayout(input_layout)
        self.setLayout(vlayout)
        
        self.x = np.array([])
        self.y = np.array([])
        self.onChange()

    def updateGraph(self,x,y):
        self.x = x.copy()
        self.y = y.copy()
        self.onChange()
        
    
    def onChange(self):
        #self.ax.clear()
        while(len(self.ax.lines) > 0):
            self.ax.lines.pop(0)
            
        self.ax.plot(self.x, self.y, color = self.color)
        if(len(self.x ) > 0 and len(self.y) > 0):
            self.ax.set_xlim(1.05*np.amin(self.x),1.05* np.amax(self.x) + 1e-32)
            self.ax.set_ylim(np.amin(self.y), 1.1*np.amax(self.y)+ 1e-32)
        self.view.figure.tight_layout()
        self.view.draw()
        
        
        
        
        
        
        
class CrossSection(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        #  create widgets
        self.view = FigureCanvas(Figure(figsize=(5, 3)))
        self.ax = self.view.figure.subplots()
        self.toolbar = NavigationToolbar2QT(self.view, self)
        
        self.ax.set_xlabel('Width (mm)')
        self.ax.set_ylabel('Height (mm)')
        self.ax.set_title('Cross section')
        


        #  Create layout
        input_layout = QHBoxLayout()
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.toolbar)
        vlayout.addWidget(self.view)
        vlayout.addLayout(input_layout)
        self.setLayout(vlayout)
        
        self.profile = np.array([[]])
        self.height = 1.0
        self.width = 1.0
        self.z0 = 0.0
        self.y0 = 0.0
        
        self.onChange()

    def updateGraph(self,profile, h,w,z0,y0):
        self.profile = profile.copy()
        self.height = h
        self.width = w
        self.z0 = z0
        self.y0 = y0
        
        if(np.abs(self.z0 ) > 0.5*h):
            self.z0 = np.sign(z0) * 0.5*h       
        if(np.abs(self.y0 ) > 0.5*w):
            self.y0 = np.sign(y0) * 0.5*w       
        self.onChange()
        
    
    def onChange(self):
        self.ax.clear()
        self.ax.set_xlabel('Width (mm)')
        self.ax.set_ylabel('Height (mm)')
        self.ax.set_title('Cross section')
        self.ax.imshow(self.profile, extent = [-0.5*self.width, 0.5*self.width, -0.5*self.height, 0.5*self.height])
        self.ax.vlines(self.y0, -0.5*self.height, 0.5*self.height,color = 'r',linestyle = '--')
        self.ax.hlines(self.z0, -0.5*self.width, 0.5*self.width,color = 'b',linestyle = '--')
        self.view.figure.tight_layout()
        self.view.draw()        

        
    
        
        
        
        

