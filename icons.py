import sys
from PyQt5.QtGui import QIcon

class Icons():

    def __init__(self, iconFolder = None):
        if(iconFolder is None):
            iconFolder = sys.path[0] + '\\icons\\'
        self.windowIcon = QIcon(iconFolder + 'windowIcon.png')        
        return