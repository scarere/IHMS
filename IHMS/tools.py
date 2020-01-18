import numpy as np
import statistics as stat
import biosppy as bp
from PyQt5 import QtGui

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
    # Start PyQt
    app = QtGui.QApplication([])

    # Define a top-level widget to hold everything
    mainWidget = QtGui.QWidget()

    # Set Main Widget Background Color
    p = mainWidget.palette()
    p.setColor(mainWidget.backgroundRole(), QtGui.QColor(40, 40, 40))
    mainWidget.setPalette(p)

    # Set Figure Size
    fig.resize(size[0], size[1])

    # Set window title
    if (title != None):
        fig.setWindowTitle(title)

    # Set Grid Layout
    layout = QtGui.QGridLayout()
    fig.setLayout(layout)