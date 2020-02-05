import sys
from os import listdir, remove
from os.path import isfile, join
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import numpy as np

class Visualizer():
    def __init__(self, size=(1500,800), title='Data Visualizer'):
        '''Used to easily analyze data windows tagged as abnormal by IHMS

        Args:
            size (int, int): The size of the overall window in the format (length, width)
            titl (str): The title of the overall window
        '''
       
        # Change App color palette and style
        if sys.platform.startswith('darwin'):
            QApplication.setStyle('macintosh')
        else:
            QApplication.setStyle('Fusion')

        p = QPalette()
        p.setColor(QPalette.Window, QColor(30,30,30))
        p.setColor(QPalette.WindowText, Qt.white)
        QApplication.setPalette(p)

        # Define a top-level widget to hold everything
        self.mainWidget = QWidget()

        # Set Figure Size
        self.mainWidget.resize(size[0], size[1])

        # Set window title
        if (title != None):
            self.mainWidget.setWindowTitle(title)

        ########################
        # Create Widgets
        ########################

        # Create dropdown menu
        self.dropdown = QComboBox()
        self.dropdown.setStyleSheet('QAbstractItemView{background:white}') # Change background color of dropdown
        self.scan()

        # Buttons
        self.scanButton = QPushButton('SCAN')
        self.scanButton.clicked.connect(self.scan)

        self.delButton = QPushButton('DELETE')
        self.delButton.clicked.connect(self.delete)

        self.plot1Button = QPushButton('Plot Data On Graph 1')
        self.plot1Button.clicked.connect(self.plotGraph1)

        self.plot2Button = QPushButton('Plot Data On Graph 2')
        self.plot2Button.clicked.connect(self.plotGraph2)

        self.clearButton = QPushButton('CLEAR')
        self.clearButton.clicked.connect(self.clearGraphs)

         # Create Logo PixMap
        self.logo = QLabel()
        logomap = QPixmap('IHMSLogo.png')
        logomap = logomap.scaled(250,250, Qt.KeepAspectRatio)
        self.logo.setPixmap(logomap)
        self.logo.setAlignment(Qt.AlignCenter)

        # Create status label
        self.title = QLabel()
        self.title.setText('Data\nVisualizer')
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont('Times', 50))

        self.spacer = QLabel()
        self.spacer.setText('')

        #####################
        # Create Plot Widgets
        #####################
        timewin = 10
        XWIN = timewin * 100
        XTICKS = timewin+1

         # Set Up variables
        (x_vec, step) = np.linspace(0,timewin,XWIN+1, retstep=True) # vector used to plot y values
        xlabels = np.zeros(timewin+1).tolist() # Vector to hold labels of ticks on x-axis
        xticks = list(range(0, timewin+1)) # Initialize locations of x-labels
        y_vec = np.zeros((len(x_vec))) # Initialize y_values as zero

        # Create axis item and set tick locations and labels
        self.axis1 = pg.AxisItem(orientation='bottom')
        self.axis1.setTicks([[(xticks[i],str(xlabels[i])) for i in range(len(xticks))]]) # Initialize all labels as zero

        self.axis2 = pg.AxisItem(orientation='bottom')
        self.axis2.setTicks([[(xticks[i],str(xlabels[i])) for i in range(len(xticks))]]) # Initialize all labels as zero

        
        # Create Plot Widgets
        self.plot1 = pg.PlotWidget(axisItems={'bottom': self.axis1}, labels={'left': 'Volts (mV)'}, title='Graph 1') # Create Plot Widget
        self.plot1.plotItem.showGrid(x=True) # Enable vertical gridlines

        self.plot2 = pg.PlotWidget(axisItems={'bottom': self.axis2}, labels={'left': 'Volts (mV)'}, title='Graph 2') # Create Plot Widget
        self.plot2.plotItem.showGrid(x=True) # Enable vertical gridlines

        # Plot data and save curve. Append curve to list
        self.curve1 = self.plot1.plot(x_vec, y_vec, pen=pg.mkPen('c', width=1)) # Set thickness and color of lines
        self.curve2 = self.plot2.plot(x_vec, y_vec, pen=pg.mkPen('m', width=1)) # Set thickness and color of lines
        
        #----------------------
        # Add Widgets to Layout
        #----------------------
        # Create Layouts
        right = QVBoxLayout()
        left = QVBoxLayout()
        wrap = QHBoxLayout()

        # Add widgets
        right.addWidget(self.plot1)
        right.addWidget(self.plot2)
        left.addWidget(self.logo)
        left.addWidget(self.title)
        left.addWidget(self.spacer, Qt.AlignBottom)
        left.addWidget(self.dropdown, Qt.AlignTop)
        left.addWidget(self.scanButton)
        left.addWidget(self.plot1Button)
        left.addWidget(self.plot2Button)
        left.addWidget(self.delButton)
        left.addWidget(self.clearButton)

        wrap.addLayout(left)
        wrap.addLayout(right)
        self.mainWidget.setLayout(wrap)

        self.mainWidget.show()

    def scan(self):
        '''Scans the savedData folder and updates the dropdown menu of available data windows
        '''
        self.dropdown.clear() # Clear combobox so we don't get duplicates
        files = [f for f in listdir('savedData') if isfile(join('savedData', f))] # Get list of files in savedData folder
        for file in files:
            if 'metadata' not in file: # Discard metadata files as options
                self.dropdown.addItem(file[:-4]) # Add data as an option in dropdown menu
    
    def delete(self):
        '''Deletes the selected data window
        '''
        datastring = str(self.dropdown.currentText())
        remove('savedData/' + datastring + '.csv')
        remove('savedData/' + datastring + '-metadata.csv')
        self.scan()

    def plotGraph1(self):
        '''Plots a data window on graph 1
        '''

        #Clear plot 1 to get rid of abnormal annotations (vertical lines)
        self.plot1.clear()

        #Load data and metadata of data file/window currently selected by dropdown menu
        datastring = str(self.dropdown.currentText())
        metadata = np.genfromtxt('savedData/'+ datastring + '-metadata.csv', delimiter=',')
        data = np.genfromtxt('savedData/' + datastring + '.csv', delimiter=',')

        # Seperate metadata into relevant variables. 
        fs = metadata[0] # First element is always sampling frequency
        winLength = int(metadata[1]) # Second element is always the length of the data window in seconds
        rpeaks = metadata[2:] # rest of data is locations of detected abnormalities

        # Set helper variables
        xwin = int(fs*winLength)
        (x_vec, step) = np.linspace(0,winLength,xwin, retstep=True) # vector used to plot y values
        xticks = list(range(0, winLength+1))

        # Reset x axis label locations and plot data
        self.axis1 = pg.AxisItem(orientation='bottom')
        self.axis1.setTicks([[(xticks[i],str(xticks[i])) for i in range(len(xticks))]]) # Set labels
        self.curve1 = self.plot1.plot(x_vec, data, pen=pg.mkPen('c', width=1)) # Set thickness and color of lines

        # Annotate abnormal peaks with vertical lines
        for peak in rpeaks:
            line = pg.InfiniteLine(pos=peak/fs, label='Abnormal', labelOpts={'movable':True, 'position':0.9}, pen=pg.mkPen('y', width=0.75))
            self.plot1.addItem(line)

        # Process Changes
        QApplication.processEvents()
    
    def plotGraph2(self):
        '''Plots a data window on graph 1
        '''
        
        #Clear plot 2 to get rid of abnormal annotations (vertical lines)
        self.plot2.clear()

        #Load data and metadata of data file/window currently selected by dropdown menu
        datastring = str(self.dropdown.currentText())
        metadata = np.genfromtxt('savedData/'+ datastring + '-metadata.csv', delimiter=',')
        data = np.genfromtxt('savedData/' + datastring + '.csv', delimiter=',')

        # Seperate metadata into relevant variables. 
        fs = metadata[0] # First element is always sampling frequency
        winLength = int(metadata[1]) # Second element is always the length of the data window in seconds
        rpeaks = metadata[2:] # rest of data is locations of detected abnormalities

        # Set helper variables
        xwin = int(fs*winLength)
        (x_vec, step) = np.linspace(0,winLength,xwin, retstep=True) # vector used to plot y values
        xticks = list(range(0, winLength+1))

        # Set x axis label locations and plot data
        self.axis2 = pg.AxisItem(orientation='bottom')
        self.axis2.setTicks([[(xticks[i],str(xticks[i])) for i in range(len(xticks))]]) # Set labels
        self.curve2 = self.plot2.plot(x_vec, data, pen=pg.mkPen('m', width=1)) # Set thickness and color of lines

        # Annotate abnormal peaks with vertical lines
        for peak in rpeaks:
            line = pg.InfiniteLine(pos=peak/fs, label='Abnormal', labelOpts={'movable':True, 'position':0.9}, pen=pg.mkPen('y', width=0.75))
            self.plot2.addItem(line)

        # Process Changes
        QApplication.processEvents()
    
    def clearGraphs(self):
        '''Clears both graphs

        Since clearing plots erases all items, axis and curve items must be re-initialized
        '''
        
        # Clear Graph
        self.plot1.clear()
        self.plot2.clear()

        # Set helper variables
        timewin = 10
        XWIN = timewin * 100
        XTICKS = timewin+1

        # Set Up variables
        (x_vec, step) = np.linspace(0,timewin,XWIN+1, retstep=True) # vector used to plot y values
        xlabels = np.zeros(timewin+1).tolist() # Vector to hold labels of ticks on x-axis
        xticks = list(range(0, timewin+1)) # Initialize locations of x-labels
        y_vec = np.zeros((len(x_vec))) # Initialize y_values as zero

        # Reset Axes
        self.axis1 = pg.AxisItem(orientation='bottom')
        self.axis1.setTicks([[(xticks[i],str(xlabels[i])) for i in range(len(xticks))]])
        self.axis2 = pg.AxisItem(orientation='bottom')
        self.axis2.setTicks([[(xticks[i],str(xlabels[i])) for i in range(len(xticks))]])

        # Reset Data
        self.curve1 = self.plot1.plot(x_vec, y_vec, pen=pg.mkPen('c', width=1)) # Set thickness and color of lines
        self.curve2 = self.plot2.plot(x_vec, y_vec, pen=pg.mkPen('m', width=1)) # Set thickness and color of lines

# Open Data Visualizer
if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Visualizer()
    app.exec_()