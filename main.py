import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from window import *
from graph import *


if __name__== '__main__':

    print('App starting')
    
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Plastique'))
    
    print(QStyleFactory.keys())
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
    

    