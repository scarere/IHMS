# Processing Imports
import numpy as np
import statistics as stat
import biosppy as bp
# Gui Imports
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QWidgets import *
import pyqtgraph as pg
# Other imports
import sys

def extract_heartbeats(win, fs, beatWin=2):
    """ Extracts heartbeats from an ECG recording.

    Given an ECG recording, extracts individual heartbeats and returns them seperately in a list. 
    Beats are normalized, and padded to a fixed length

    Args:
        win (array): A list of voltage values that represent the ECG recording
        fs (int, float): The sampling frequency of the ECG recording
        beatWin (int, float): The length of the window in seconds that the beat should be seperated into. If beats are 
            too short they will be padded, if they are too long they will be truncated

    Returns:
        beatList: A list of arrays that represent the individual beats within the recording.
    """

    # Extract R-peaks
    rpeaks, = bp.ecg.hamilton_segmenter(signal=win, sampling_rate=fs)
    rpeaks, = bp.ecg.correct_rpeaks(signal=win, rpeaks=rpeaks, sampling_rate=fs)

    # Normalize data
    norm = (win - min(win))/(max(win)-min(win))

    # Calculate median distance between rpeaks (in samples) and use this as period
    diffs = []
    for index, r in enumerate(rpeaks):
        if index > 0:
            diffs.append(r-rpeaks[index-1]) # Calculate difference between r-peaks in samples
    period = stat.median(diffs) # Calculate median period
    del diffs

    # Calculate beat length in samples
    beatLength = beatWin*fs

    # Extract individual heartbeats
    beatList = []
    for r in rpeaks:
        if r > beatLength/2 and len(win)-r > beatLength/2:
            beat = norm[r-int(period/2):r+int(period/2)] # Exctract data surrounding r-peak
            # Check length of beat and either truncate or pad it
            if (len(beat)>beatLength):
                beat = beat[0:beatLength]
            else:
                beat = np.pad(beat, (0,beatLength - len(beat)), 'constant') # Pad beat with zeros if it is short
            beatList.append(beat)
    
    return beatList

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

    # Set Grid Layout
    layout = QGridLayout()
    mainWidget.setLayout(layout)

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

    startButton = QPushButton("START")
    stopButton = QPushButton("STOP")
    logo = QLabel()
    logomap = QPixmap('IHMSLogo.png')
    logomap = logomap.scaled(250,250, Qt.KeepAspectRatio)
    logo.setPixmap(logomap)
    logo.setAlignment(Qt.AlignCenter)
    
    #----------------------
    # Add Widgets to Layout
    #----------------------
    layout.addWidget(plot1, 0, 1)
    layout.addWidget(plot2, 2, 1)
    layout.addWidget(logo, 0, 0)
    layout.addWidget(startButton, 2, 0)
    layout.addWidget(stopButton, 3, 0)

    mainWidget.show()
    app.exec()

    return mainWidget, [axis1, axis2], [curve1, curve2]