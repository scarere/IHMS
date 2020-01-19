from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import sys
import numpy as np

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
    bpm.addWidget(bpmNum)
    bpm.addWidget(bpmlabel)

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