from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import sys
import numpy as np

class Dashboard():
    def __init__(self, fs, tickfactor=1, timewin=10, size=(1500,800), title='IHMS'):
        self.fs = fs
        self.timewin = timewin
        self.tickfactor = tickfactor
        self.XWIN = self.timewin * self.fs
        self.XTICKS = (int)((self.timewin+1) / self.tickfactor)
        self.firstUpdate = True
        self.run = False

        # Start PyQt
        #self.app = QApplication([])

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
        
        # ------------------
        # Create Plot Widgets
        # ------------------

        # Set Up variables
        (self.x_vec, step) = np.linspace(0,self.timewin,self.XWIN+1, retstep=True) # vector used to plot y values
        self.xlabels1 = np.zeros(self.XTICKS).tolist() # Vector to hold labels of ticks on x-axis
        self.xticks1 = [ x * self.tickfactor for x in list(range(0, self.XTICKS))] # Initialize locations of x-labels
        self.xlabels2 = np.zeros(self.XTICKS).tolist() # Vector to hold labels of ticks on x-axis
        self.xticks2 = [ x * self.tickfactor for x in list(range(0, self.XTICKS))] # Initialize locations of x-labels
        self.y_vec1 = np.zeros((len(self.x_vec))) # Initialize y_values as zero
        self.y_vec2 = np.zeros((len(self.x_vec))) # Initialize y_values as zero

        # Create axis item and set tick locations and labels
        self.axis1 = pg.AxisItem(orientation='bottom')
        self.axis1.setTicks([[(self.xticks1[i],str(self.xlabels1[i])) for i in range(len(self.xticks1))]]) # Initialize all labels as zero

        self.axis2 = pg.AxisItem(orientation='bottom')
        self.axis2.setTicks([[(self.xticks2[i],str(self.xlabels2[i])) for i in range(len(self.xticks2))]]) # Initialize all labels as zero

        # Create plot widget and append to list
        self.plot1 = pg.PlotWidget(axisItems={'bottom': self.axis1}, labels={'left': 'Volts (mV)'}, title='Filtered ECG') # Create Plot Widget
        self.plot1.plotItem.setMouseEnabled(x=False, y=False) # Disable panning for widget
        self.plot1.plotItem.showGrid(x=True) # Enable vertical gridlines

        self.plot2 = pg.PlotWidget(axisItems={'bottom': self.axis2}, labels={'left': 'Volts (mV)'}, title='Raw Voltage') # Create Plot Widget
        self.plot2.plotItem.setMouseEnabled(x=False, y=False) # Disable panning for widget
        self.plot2.plotItem.showGrid(x=True) # Enable vertical gridlines

        # Plot data and save curve. Append curve to list
        self.curve1 = self.plot1.plot(self.x_vec, self.y_vec1, pen=pg.mkPen('r', width=0.5)) # Set thickness and color of lines
        self.curve2 = self.plot2.plot(self.x_vec, self.y_vec2, pen=pg.mkPen('y', width=0.5)) # Set thickness and color of lines

        # --------------------
        # Create Other Widgets
        # --------------------

        # Create stop and start buttons
        self.startButton = QPushButton("START")
        self.startButton.clicked.connect(self.start)
        self.stopButton = QPushButton("STOP")
        self.stopButton.clicked.connect(self.stop)

        # Create BPM holder layout
        self.bpm = QVBoxLayout()
        self.bpm.setSpacing(0)
        self.bpm.setContentsMargins(0,0,0,0)

        # BPM Number
        self.bpmNum = QLabel()
        self.bpmNum.setText("60")
        self.bpmNum.setAlignment(Qt.AlignCenter)
        self.bpmNum.setFont(QFont('Times', 100, QFont.Bold))

        #BPM label
        self.bpmlabel = QLabel()
        self.bpmlabel.setText("BPM")
        self.bpmlabel.setAlignment(Qt.AlignCenter)
        self.bpmlabel.setFont(QFont('Times', 40, QFont.Bold))
        self.bpmlabel.setStyleSheet("color: darkRed")

        # Add Num and label to holder layout
        self.bpm.addWidget(self.bpmNum)
        self.bpm.addWidget(self.bpmlabel)

        # Create Logo PixMap
        self.logo = QLabel()
        logomap = QPixmap('IHMSLogo.png')
        logomap = logomap.scaled(250,250, Qt.KeepAspectRatio)
        self.logo.setPixmap(logomap)
        self.logo.setAlignment(Qt.AlignCenter)
        
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
        left.addWidget(self.logo, Qt.AlignBottom)
        left.addLayout(self.bpm)
        left.addWidget(self.bpmlabel, Qt.AlignTop)
        left.addWidget(self.startButton)
        left.addWidget(self.stopButton)

        wrap.addLayout(left)
        wrap.addLayout(right)
        self.mainWidget.setLayout(wrap)

        self.mainWidget.show()
    
    def updateBPM(self, bpm):
        bpm = int(bpm)
        self.bpmNum.setText(str(bpm))
        QApplication.processEvents()

    def updatePlot1(self, chunk):
        chunkperiod = len(chunk)*(1/self.fs)
        self.xticks1 = [x - chunkperiod for x in self.xticks1] # Update location of x-labels
        if(self.xticks1[0] < 0): # Check if a label has crossed to the negative side of the y-axis
            # Delete label on left of x-axis and add a new one on the right side
            self.xticks1.pop(0)
            self.xticks1.append(self.xticks1[-1] + self.tickfactor)
            # Adjust time labels accordingly
            if (self.firstUpdate == False): # Check to see if it's the first update, if so skip so that time starts at zero
                self.xlabels1.append(self.xlabels1[-1] + self.tickfactor)
                self.xlabels1.pop(0)
            else:
                self.firstUpdate = False

        # Update Plot Data
        self.y_vec1 = np.append(self.y_vec1, chunk, axis=0)[len(chunk):] # Append chunk to the end of y_data (currently only doing 1 channel)
        self.curve1.setData(self.x_vec, self.y_vec1) # Update data
        # Update x-axis labels
        self.axis1 = self.plot1.getAxis(name='bottom')
        self.axis1.setTicks([[(self.xticks1[i],str(self.xlabels1[i])) for i in range(len(self.xticks1))]])

        # Update changes
        self.app.processEvents()

    def updatePlot2(self, chunk):
        chunkperiod = len(chunk)*(1/self.fs)
        self.xticks2 = [x - chunkperiod for x in self.xticks2] # Update location of x-labels
        if(self.xticks2[0] < 0): # Check if a label has crossed to the negative side of the y-axis
            # Delete label on left of x-axis and add a new one on the right side
            self.xticks2.pop(0)
            self.xticks2.append(self.xticks2[-1] + self.tickfactor)
            # Adjust time labels accordingly
            if (self.firstUpdate == False): # Check to see if it's the first update, if so skip so that time starts at zero
                self.xlabels2.append(self.xlabels2[-1] + self.tickfactor)
                self.xlabels2.pop(0)
            else:
                self.firstUpdate = False

        # Update Plot Data
        self.y_vec2 = np.append(self.y_vec2, chunk, axis=0)[len(chunk):] # Append chunk to the end of y_data (currently only doing 1 channel)
        self.curve2.setData(self.x_vec, self.y_vec2) # Update data
        # Update x-axis labels
        self.axis2 = self.plot2.getAxis(name='bottom')
        self.axis2.setTicks([[(self.xticks2[i],str(self.xlabels2[i])) for i in range(len(self.xticks2))]])

        # Update changes
        self.app.processEvents()
    
    def start(self):
        if not self.run:
            self.run = self.startLoop()

    
    def startLoop(self):
        count = 0
        self.run = True
        while(self.run == True):
           self.bpmNum.setText(str(count))
           count = count + 1
           QApplication.processEvents()
        
        self.bpmNum.setText('00')

    def stop(self):
        self.run = False
        QApplication.processEvents()


def launchGUI(title='IHMS', size=(1500,800)):
    # Set Variables
    fs = 200
    tickfactor = 1
    timewin = 10
    XWIN = timewin * fs
    XTICKS = (int)((timewin+1) / tickfactor)

    # Start PyQt
    app = QApplication([])

    # Change App color palette and style
    if sys.platform.startswith('darwin'):
        app.setStyle('macintosh')
    else:
        app.setStyle('Fusion')

    p = QPalette()
    p.setColor(QPalette.Window, QColor(30,30,30))
    p.setColor(QPalette.WindowText, Qt.white)

    app.setPalette(p)

    # Define a top-level widget to hold everything
    mainWidget = QWidget()

    # Set Figure Size
    mainWidget.resize(size[0], size[1])

    # Set window title
    if (title != None):
        mainWidget.setWindowTitle(title)

    # ------------------
    # Create Plot Widgets
    # ------------------

    # Set Up variables
    (x_vec, step) = np.linspace(0,timewin,XWIN+1, retstep=True) # vector used to plot y values
    xlabels = np.zeros(XTICKS).tolist() # Vector to hold labels of ticks on x-axis
    xticks = [ x * tickfactor for x in list(range(0, XTICKS))] # Initialize locations of x-labels
    y_vec = np.zeros((len(x_vec))) # Initialize y_values as zero

    # Create axis item and set tick locations and labels
    axis1 = pg.AxisItem(orientation='bottom')
    axis1.setTicks([[(xticks[i],str(xlabels[i])) for i in range(len(xticks))]]) # Initialize all labels as zero

    axis2 = pg.AxisItem(orientation='bottom')
    axis2.setTicks([[(xticks[i],str(xlabels[i])) for i in range(len(xticks))]]) # Initialize all labels as zero

    # Create plot widget and append to list
    plot1 = pg.PlotWidget(axisItems={'bottom': axis1}, labels={'left': 'Volts (mV)'}, title='Filtered ECG') # Create Plot Widget
    plot1.plotItem.setMouseEnabled(x=False, y=False) # Disable panning for widget
    plot1.plotItem.showGrid(x=True) # Enable vertical gridlines

    plot2 = pg.PlotWidget(axisItems={'bottom': axis2}, labels={'left': 'Volts (mV)'}, title='Raw Voltage') # Create Plot Widget
    plot2.plotItem.setMouseEnabled(x=False, y=False) # Disable panning for widget
    plot2.plotItem.showGrid(x=True) # Enable vertical gridlines

    # Plot data and save curve. Append curve to list
    curve1 = plot1.plot(x_vec, y_vec, pen=pg.mkPen('r', width=0.5)) # Set thickness and color of lines
    curve2 = plot2.plot(x_vec, y_vec, pen=pg.mkPen('y', width=0.5)) # Set thickness and color of lines

    # --------------------
    # Create Other Widgets
    # --------------------

    # Create stop and start buttons
    startButton = QPushButton("START")
    stopButton = QPushButton("STOP")

    # Create BPM holder layout
    bpm = QVBoxLayout()
    bpm.setSpacing(0)
    bpm.setContentsMargins(0,0,0,0)

    # BPM Number
    bpmNum = QLabel()
    bpmNum.setText("60")
    bpmNum.setAlignment(Qt.AlignCenter)
    bpmNum.setFont(QFont('Times', 100, QFont.Bold))

    #BPM label
    bpmlabel = QLabel()
    bpmlabel.setText("BPM")
    bpmlabel.setAlignment(Qt.AlignCenter)
    bpmlabel.setFont(QFont('Times', 40, QFont.Bold))
    bpmlabel.setStyleSheet("color: darkRed")

    # Add Num and label to holder layout
    bpm.addWidget(bpmNum, Qt.AlignTop)
    bpm.addWidget(bpmlabel, Qt.AlignTop)

    # Create Logo PixMap
    logo = QLabel()
    logomap = QPixmap('IHMSLogo.png')
    logomap = logomap.scaled(250,250, Qt.KeepAspectRatio)
    logo.setPixmap(logomap)
    logo.setAlignment(Qt.AlignCenter)
    
    #----------------------
    # Add Widgets to Layout
    #----------------------
    # Create Layouts
    right = QVBoxLayout()
    left = QVBoxLayout()
    wrap = QHBoxLayout()

    # Add widgets
    right.addWidget(plot1)
    right.addWidget(plot2)
    left.addWidget(logo, Qt.AlignBottom)
    left.addLayout(bpm)
    left.addWidget(bpmlabel, Qt.AlignTop)
    left.addWidget(startButton)
    left.addWidget(stopButton)

    wrap.addLayout(left)
    wrap.addLayout(right)
    mainWidget.setLayout(wrap)

    mainWidget.show()
    app.exec()

    return mainWidget, [axis1, axis2], [curve1, curve2]