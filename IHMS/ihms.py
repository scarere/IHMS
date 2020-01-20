# Change error settings
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}
#import tensorflow as tf
# Processing Imports
import numpy as np
import statistics as stat
import biosppy as bp
import time
from tensorflow.keras.models import load_model
# Sensor IO Imports
from multiprocessing import Process, Queue
import multiprocessing as mp
import gdx as gd
# Gui Imports
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg
# Other imports
import sys
from datetime import datetime

#-----------------
# Helper Functions
#-----------------

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
        bpm: The beats per minute of the window of data based on the median beat period
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

    bpm = 60*fs / period
    
    return beatList, bpm

class dataCollector():
    def __init__(self,):
        mp.set_start_method('spawn')

    def start(self):
        self.sensors = [1, 5]
        self.period = int((1/100)*1000) # period in ms

        # Create Queue's To Pass Data from collect_data process to main process
        dataq = Queue()
        timeq = Queue()

        # Create and Start Data Collection Process
        self.dataproc = Process(target=self.collect_data, args=(dataq, timeq, self.sensors, self.period))
        self.dataproc.start()

        return [dataq, timeq]
    
    def stop(self):
        # Terminate data collection process
        self.dataproc.terminate()

        # Close sensor
        gdx = gd.gdx()
        gdx.stop()
        gdx.close()
    
    def collect_data(self, dataq, timeq, sensor, period):
        ''' Collects data within it's own process

        Call this function within its own process to collect chunks of data in the background.
        The function pushes chunks to a Queue that is accessible from the main process

        Args:
            dataq: The multiprocessing Queue() object to push the chunks of data to
            timeq: The multiprocessing Queue() object to push the corresponding timestamps to
            sensor (int): The number identifier for the sensor to collect data from
            period (int): The sampling period (in milliseconds) to start the sensor with
        '''

        # Open sensor
        gdx = gd.gdx()
        gdx.open_usb()

        # Select and Start Sensors
        gdx.select_sensors(sensors=sensor)
        gdx.start_fast(period=period)

        # Get Start Time
        ts = time.time()
        while(True):
            try:
                chunk = gdx.read_chunk() #returns a list of measurements from the sensors selected.

                # Turn data into numpy array
                data = np.asarray(chunk)
                #data = data.flatten()
                # Push data and a timestamp to respective queue's
                dataq.put(data)
                timeq.put(time.time() - ts)
            except (KeyboardInterrupt, SystemExit):
                print("Exit")
                raise

#------------------------
# Dashboard Class for GUI
#------------------------

class Dashboard():
    def __init__(self, fs=200, tickfactor=1, timewin=10, size=(1500,800), title='IHMS'):
        self.fs = fs
        self.timewin = timewin
        self.tickfactor = tickfactor
        self.XWIN = self.timewin * self.fs
        self.XTICKS = (int)((self.timewin+1) / self.tickfactor)
        self.firstUpdate = True
        self.running = False
        self.collector = dataCollector()

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
        self.curve1 = self.plot1.plot(self.x_vec, self.y_vec1, pen=pg.mkPen('c', width=0.5)) # Set thickness and color of lines
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

        # Create status label
        self.status = QLabel()
        self.status.setText('Idle')
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setFont(QFont('Times', 30))
        
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
        left.addWidget(self.status, Qt.AlignTop)
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
    
    def updateStatus(self, newStatus):
        self.status.setText(str(newStatus))
        QApplication.processEvents()

    def updatePlot1(self, chunk):
        #print(np.shape(chunk))
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
        QApplication.processEvents()

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
        QApplication.processEvents()

    def start(self):
        # Initialize Variables
        self.sensors = [1]
        self.period = int((1/self.fs)*1000) # period in ms
        print(self.period)
        print(self.fs)
        #winLength = select_winLength()
        self.winLength = 10
        self.buffer = [] # Buffer to hold sensor data

        # Load model
        modelname = 'mit/mit-200hz'
        self.model = load_model('trained-models/' + modelname + '.h5')

        dataq, timeq = self.collector.start()

        self.running = True
        self.updateStatus('Recording')
        while(self.running == True):
            # Get Chunk of data from Data Queue
            chunk = dataq.get()
            #tc = timeq.get()

                
            if not np.size(chunk) == 0:
                self.updatePlot1(chunk[0]) # Plot filtered data
                #self.updatePlot2(chunk[1]) # Also plot raw data

                # Add Chunk of data to buffer
                if len(self.buffer) == 0: # Check if buffer is empty
                    self.buffer = chunk[0]
                else:
                    self.buffer = np.append(self.buffer, chunk[0], axis=0)
                
                # Check buffer length so that we don't overwrite previous message immediately
                if len(self.buffer) > self.fs*self.winLength*0.25:
                    self.updateStatus('Running...')
                
                if len(self.buffer) > self.fs*self.winLength:
                    self.updateStatus('Processing...')
                    # Get date and time string in case data needs to be saved
                    now = datetime.now()
                    dt_string = now.strftime("%d-%m-%Y--%H:%M:%S")
                    # Seperate a window from buffer
                    win = self.buffer[0:self.fs*self.winLength]
                    self.buffer = self.buffer[self.fs*self.winLength:]
                    
                    # Extract heartbeats
                    beats, bpm = extract_heartbeats(win=win, fs=self.fs, beatWin=2)
                    #print(np.shape(beats))
                    beats = np.expand_dims(beats, 2)
                    self.updateBPM(bpm)
                    #print(np.shape(beats))

                    # Get Predictions
                    predictions = self.model.predict(beats, batch_size=len(beats))

                    if 'mit' in modelname:
                        classes = ['N', 'S', 'V', 'F', 'Q']
                        for pred in predictions:
                            if not np.argmax(pred) == 0:
                                self.updateStatus(classes[np.argmax(pred)] + ' Class Detected')
                                break
                        else:
                            self.updateStatus('No Abnormalities Detected')
                    else:
                        for pred in predictions:
                            if pred[0] < 0.5: # Check If beat was predicted as abnormal
                                win = np.asarray(win)
                                self.updateStatus('Arrhythmia Detected!')
                                np.savetxt('savedData/' + dt_string + '.csv', win, fmt='%f', delimiter=',')
                                break # Break from check since we are already saving whole window
                        else:
                            self.updateStatus('No Abnormalities Detected')


        self.updateStatus('Idle')

    def stop(self):
        self.collector.stop()
        self.running = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Dashboard()
    app.exec_()