import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


from graph import *


class Buttons(QWidget):
    def __init__(self, parent=None, window = None):
        super().__init__(parent)
        self.window = window
        self.layout = QGridLayout(self)
        
        
        self.startCalculationButton = QPushButton()
        self.startCalculationButton.setText("Calculate")
        self.startCalculationButton.clicked.connect(self.startCalculationButtonClicked)        
        self.startCalculationButton.setToolTip('Calculate profiles based on input.')  
        self.layout.addWidget(self.startCalculationButton,5,7)
        
        
        self.heightSpinBoxLabel = QLabel()
        self.heightSpinBoxLabel.setText('Height (mm)')
        self.heightSpinBoxLabel.setAlignment(Qt.AlignRight)
        self.heightSpinBoxLabel.setToolTip('Set the height of the channel in milimetres.')  
        self.layout.addWidget(self.heightSpinBoxLabel,0,0)  
        self.heightSpinBox = QDoubleSpinBox()
        self.heightSpinBox.setToolTip('Set the height of the channel in milimetres.')  
        self.heightSpinBox.setValue(self.window.settings.channelHeight)
        self.heightSpinBox.setDecimals(3)
        self.heightSpinBox.setSingleStep(0.1)
        self.heightSpinBox.valueChanged.connect(self.heightSpinBoxChanged)  
        self.layout.addWidget(self.heightSpinBox,0,1)       

        self.widthSpinBoxLabel = QLabel()
        self.widthSpinBoxLabel.setText('Width (mm)')
        self.widthSpinBoxLabel.setAlignment(Qt.AlignRight)
        self.widthSpinBoxLabel.setToolTip('Set the width of the channel in milimetres.')  
        self.layout.addWidget(self.widthSpinBoxLabel,1,0)  
        self.widthSpinBox = QDoubleSpinBox()
        self.widthSpinBox.setToolTip('Set the width of the channel in milimetres.')  
        self.widthSpinBox.setValue(self.window.settings.channelWidth)
        self.widthSpinBox.setDecimals(3)
        self.widthSpinBox.setSingleStep(0.1)
        self.widthSpinBox.valueChanged.connect(self.widthSpinBoxChanged)  
        self.layout.addWidget(self.widthSpinBox,1,1)  

        
        self.flowRateSpinBoxLabel = QLabel()
        self.flowRateSpinBoxLabel.setText('Flow rate (µl/min)')
        self.flowRateSpinBoxLabel.setAlignment(Qt.AlignRight)
        self.flowRateSpinBoxLabel.setToolTip('Set the flow rate of the pump in ul/min.')  
        self.layout.addWidget(self.flowRateSpinBoxLabel,2,0)  
        self.flowRateSpinBox = QDoubleSpinBox()
        self.flowRateSpinBox.setToolTip('Set the flow rate of the pump in ul/min.')  
        self.flowRateSpinBox.setValue(self.window.settings.flowRate)
        self.flowRateSpinBox.setDecimals(2)
        self.flowRateSpinBox.setSingleStep(1)
        self.flowRateSpinBox.valueChanged.connect(self.flowRateSpinBoxChanged)  
        self.flowRateSpinBox.setRange(0.0, 20000.)
        self.layout.addWidget(self.flowRateSpinBox,2,1)    
        
        self.viscositySpinBoxLabel = QLabel()
        self.viscositySpinBoxLabel.setText('Viscosity (mPa s)')
        self.viscositySpinBoxLabel.setAlignment(Qt.AlignRight)
        self.viscositySpinBoxLabel.setToolTip('Set viscosity. If the value differs from 1.002, you may be correct or wrong, depending on what you want. ')  
        self.layout.addWidget(self.viscositySpinBoxLabel,3,0)  
        self.viscositySpinBox = QDoubleSpinBox()
        self.viscositySpinBox.setDecimals(4)
        self.viscositySpinBox.setSingleStep(0.001)        
        self.viscositySpinBox.setToolTip('Set viscosity. If the value differs from 1.002, you may be correct or wrong, depending on what you want. ') 
        self.viscositySpinBox.setValue(self.window.settings.viscosity*1e3)
        self.viscositySpinBox.valueChanged.connect(self.viscositySpinBoxChanged)  
        self.layout.addWidget(self.viscositySpinBox,3,1)         
        
        
        self.numberOfZStepsSpinBoxLabel = QLabel()
        self.numberOfZStepsSpinBoxLabel.setText('Height grid steps')
        self.numberOfZStepsSpinBoxLabel.setAlignment(Qt.AlignRight)
        self.numberOfZStepsSpinBoxLabel.setToolTip('Set number of points over which the height is divided. Higher is better and slower.')
        self.layout.addWidget(self.numberOfZStepsSpinBoxLabel,0,2)  
        self.numberOfZStepsSpinBox = QSpinBox()
        self.numberOfZStepsSpinBox.setMaximum(2**16)
        self.numberOfZStepsSpinBox.setToolTip('Set number of points over which the height is divided. Higher is better and slower.')
        self.numberOfZStepsSpinBox.setValue(self.window.settings.Nz)
        self.numberOfZStepsSpinBox.valueChanged.connect(self.numberOfZStepsSpinBoxChanged)  
        self.layout.addWidget(self.numberOfZStepsSpinBox,0,3)            
        
        self.numberOfYStepsSpinBoxLabel = QLabel()
        self.numberOfYStepsSpinBoxLabel.setText('Width grid steps')
        self.numberOfYStepsSpinBoxLabel.setAlignment(Qt.AlignRight)
        self.numberOfYStepsSpinBoxLabel.setToolTip('Set number of points over which the width is divided. Higher is better and slower.')
        self.layout.addWidget(self.numberOfYStepsSpinBoxLabel,1,2)  
        self.numberOfYStepsSpinBox = QSpinBox()
        self.numberOfYStepsSpinBox.setMaximum(2**16)
        self.numberOfYStepsSpinBox.setToolTip('Set number of points over which the width is divided. Higher is better and slower.')
        self.numberOfYStepsSpinBox.setValue(self.window.settings.Ny)
        self.numberOfYStepsSpinBox.valueChanged.connect(self.numberOfYStepsSpinBoxChanged)  
        self.layout.addWidget(self.numberOfYStepsSpinBox,1,3)
        
        
        
        self.y0SpinBoxLabel = QLabel()
        self.y0SpinBoxLabel.setText('y0 (mm)')
        self.y0SpinBoxLabel.setAlignment(Qt.AlignRight)
        self.y0SpinBoxLabel.setToolTip('Set position of vertical profile')  
        self.layout.addWidget(self.y0SpinBoxLabel,2,2)  
        self.y0SpinBox = QDoubleSpinBox()
        self.y0SpinBox.setDecimals(4)
        self.y0SpinBox.setSingleStep(0.001)        
        self.y0SpinBox.setToolTip('Set position of vertical profile') 
        self.y0SpinBox.setValue(self.window.settings.y0)
        self.y0SpinBox.valueChanged.connect(self.y0SpinBoxChanged)  
        self.layout.addWidget(self.y0SpinBox,2,3)          
        
        
        self.z0SpinBoxLabel = QLabel()
        self.z0SpinBoxLabel.setText('z0 (mm)')
        self.z0SpinBoxLabel.setAlignment(Qt.AlignRight)
        self.z0SpinBoxLabel.setToolTip('Set position of horizontal profile')  
        self.layout.addWidget(self.z0SpinBoxLabel,3,2)  
        self.z0SpinBox = QDoubleSpinBox()
        self.z0SpinBox.setDecimals(4)
        self.z0SpinBox.setSingleStep(0.001)        
        self.z0SpinBox.setToolTip('Set position of horizontal profile ') 
        self.z0SpinBox.setValue(self.window.settings.y0)
        self.z0SpinBox.valueChanged.connect(self.z0SpinBoxChanged)  
        self.layout.addWidget(self.z0SpinBox,3,3)           
        
        
        
        self.minimumIterationsSpinBoxLabel = QLabel()
        self.minimumIterationsSpinBoxLabel.setText('Min iteration steps')
        self.minimumIterationsSpinBoxLabel.setAlignment(Qt.AlignRight)
        self.minimumIterationsSpinBoxLabel.setToolTip('Set the minimum number of terms of the sum in the Hagen-Poiseuille equation. Higher is better and slower.')
        self.layout.addWidget(self.minimumIterationsSpinBoxLabel,0,4)  
        self.minimumIterationsSpinBox = QSpinBox()
        self.minimumIterationsSpinBox.setMaximum(4096)
        self.minimumIterationsSpinBox.setToolTip('Set the minimum number of terms of the sum in the Hagen-Poiseuille equation. Higher is better and slower.')
        self.minimumIterationsSpinBox.setValue(self.window.settings.minimumSummationCutoff)
        self.minimumIterationsSpinBox.valueChanged.connect(self.minimumIterationsSpinBoxChanged)  
        self.layout.addWidget(self.minimumIterationsSpinBox,0,5)
        
        self.maximumIterationsSpinBoxLabel = QLabel()
        self.maximumIterationsSpinBoxLabel.setText('Max iteration steps')
        self.maximumIterationsSpinBoxLabel.setAlignment(Qt.AlignRight)
        self.maximumIterationsSpinBoxLabel.setToolTip('Set the maximum number of terms of the sum in the Hagen-Poiseuille equation. Higher is better and slower. When this is lower than the minimum iteration steps, this does not do anything. The actual number may be lower based on tolerance setting.')
        self.layout.addWidget(self.maximumIterationsSpinBoxLabel,1,4)  
        self.maximumIterationsSpinBox = QSpinBox()
        self.maximumIterationsSpinBox.setMaximum(4096)
        self.maximumIterationsSpinBox.setToolTip('Set the maximum number of terms of the sum in the Hagen-Poiseuille equation. Higher is better and slower.  When this is lower than the minimum iteration steps, this does not do anything. The actual number may be lower based on tolerance setting.')
        self.maximumIterationsSpinBox.setValue(self.window.settings.maximumSummationCutoff)
        self.maximumIterationsSpinBox.valueChanged.connect(self.maximumIterationsSpinBoxChanged)  
        self.layout.addWidget(self.maximumIterationsSpinBox,1,5)   
        
        self.errorToleranceSpinBoxLabel = QLabel()
        self.errorToleranceSpinBoxLabel.setText('Error tolerance (-log10)')
        self.errorToleranceSpinBoxLabel.setAlignment(Qt.AlignRight)
        self.errorToleranceSpinBoxLabel.setToolTip('Set the negative logarithm of the error tolerance. The sum in the Hagen-Poiseuille is cut off when two consequetive terms differ less than this value. Higher is better and slower.')
        self.layout.addWidget(self.errorToleranceSpinBoxLabel,2,4)  
        self.errorToleranceSpinBox = QDoubleSpinBox()
        self.errorToleranceSpinBox.setToolTip('Set the negative logarithm of the error tolerance. The sum in the Hagen-Poiseuille is cut off when two consequetive terms differ less than this value. Higher is better and slower.')
        self.errorToleranceSpinBox.setValue(-np.log10(self.window.settings.errorTolerance))
        self.errorToleranceSpinBox.setDecimals(2)
        self.errorToleranceSpinBox.setSingleStep(1)
        self.errorToleranceSpinBox.valueChanged.connect(self.errorToleranceSpinBoxChanged)  
        self.layout.addWidget(self.errorToleranceSpinBox,2,5)
        

    def startCalculationButtonClicked(self, event):
        print('Calculate Poiseuille flow.')
        
        if(np.abs(self.window.settings.z0 ) > 0.5*self.window.settings.channelHeight):
            z0 = np.sign(self.window.settings.z0) * 0.5*self.window.settings.channelHeight
            self.window.settings.z0 = z0
            self.z0SpinBox.setValue(z0)
            
        if(np.abs(self.window.settings.y0 ) > 0.5*self.window.settings.channelWidth):
            y0 = np.sign(self.window.settings.y0) * 0.5*self.window.settings.channelWidth
            self.window.settings.y0 = y0
            self.y0SpinBox.setValue(y0)            

        
        self.window.poiseuilleCalculator.loadFromSettings()
        self.window.poiseuilleCalculator.calculateYProfile()
        self.window.poiseuilleCalculator.calculateZProfile()
        self.window.poiseuilleCalculator.calculateCrossSectionFromLUT()
        
        
        
        
        self.window.updateGraphs()

    def heightSpinBoxChanged(self, event):
        self.window.settings.channelHeight = self.heightSpinBox.value()
        print('Height spinbox altered.')
        
    def widthSpinBoxChanged(self, event):
        self.window.settings.channelWidth = self.widthSpinBox.value()
        print('Width spinbox altered.')        
        
    def flowRateSpinBoxChanged(self, event):
        self.window.settings.flowRate = self.flowRateSpinBox.value()
        print('Flow rate spinbox altered.')                
        
    def viscositySpinBoxChanged(self, event):
        self.window.settings.flowRate = self.viscositySpinBox.value()*1e-3
        print('Viscosity spinbox altered.')             
        
    def numberOfZStepsSpinBoxChanged(self, event):
        self.window.settings.Nz = self.numberOfZStepsSpinBox.value()
        print('Nz spinbox altered.')           
        
    def numberOfYStepsSpinBoxChanged(self, event):
        self.window.settings.Ny = self.numberOfYStepsSpinBox.value()
        print('Ny spinbox altered.')            

    def y0SpinBoxChanged(self, event):
        y0 = self.y0SpinBox.value()
        self.window.settings.y0 = y0
        self.window.updateGraphs()
        print('y0 spinbox altered.')  
        
    def z0SpinBoxChanged(self, event):
        z0 = self.z0SpinBox.value()
        self.window.settings.z0 = z0
        self.window.updateGraphs()
        print('z0 spinbox altered.')          
        
    def minimumIterationsSpinBoxChanged(self, event):
        self.window.settings.minimumSummationCutoff = self.minimumIterationsSpinBox.value()
        print('nmin spinbox altered.')   

    def maximumIterationsSpinBoxChanged(self, event):
        self.window.settings.maximumSummationCutoff = self.maximumIterationsSpinBox.value()
        print('nmax spinbox altered.')  

    def errorToleranceSpinBoxChanged(self, event):
        self.window.settings.errorTolerance = 10**(-self.errorToleranceSpinBox.value())
        print('tolerance spinbox changed to ', self.window.settings.errorTolerance)  
                
        
        
        
        
        