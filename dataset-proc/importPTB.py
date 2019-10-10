import numpy as np
import statistics as stat
import matplotlib.pyplot as plt
import wfdb # Official Physionet API for loading databases into python
import biosppy as bp
from scipy import signal as sigproc

# Import list of recordings from ptb database
records = wfdb.get_record_list('ptbdb')

# Get list of control records
controlRecords = []
with open('data/ptb-original-1.0.0/CONTROLS', "r") as f:
    for line in f:
        controlRecords.append(line.rstrip()) #rstrip() removes trailing \n characters

# Remove control records from total records string to get abnormal records
abnormalRecords = [x for x in records if x not in controlRecords]

# Initialize lists to hold signals
ctrlSignals = []
abnSignals = []
# Import signals and fields into a tuple
for record in controlRecords:
    signal, field = wfdb.rdsamp('data/ptb-original-1.0.0/' + record)
    ctrlSignals.append(signal[:, 1]) #append Lead II signal to list
for record in abnormalRecords:
    signal, field = wfdb.rdsamp('data/ptb-original-1.0.0/' + record)
    abnSignals.append(signal[:, 2]) #append Lead II signal to list
    
# Convert list of signals to np array
ctrlSignals = np.asarray(ctrlSignals)
abnSignals = np.asarray(abnSignals)

# ctrl = ctrlSignals[0][0:10000]
# abn = abnSignals[0][0:4000]
# abnnorm = (abn-min(abn))/(max(abn)-min(abn))
# ctrlnorm = (ctrl-min(ctrl))/(max(ctrl)-min(ctrl))
# rpeaks, = bp.ecg.hamilton_segmenter(signal=abn, sampling_rate=1000)
# rpeaks, = bp.ecg.correct_rpeaks(signal=abn, rpeaks=rpeaks, sampling_rate=1000)
# plt.plot(abnnorm, label='Filtered')
# plt.vlines(rpeaks, -0.1, 1.1, color='m', label='R-peaks')
# plt.show()

# Define Variables for heartbeat extraction
fs = 1000 # Original Sampling Rate
winLength = 10000 # Total window length (in samples) before resampling
beatLength = 800 # Fixed length of single beat (in samples) after resampling
ds = 400 # Downsample signal to this sampling frequency

# Extract Control Heartbeats
ctrlBeats = []
for i in range(6, 9):
    for signal in ctrlSignals:
        # Grab 10s window of data
        win = signal[i*winLength:i*winLength + winLength] # Fs is 1000Hz, therefore a 10s window is 10000 samples
        win = sigproc.resample(win, int(winLength*ds/fs)) # Resample 10 seconds of data to 400Hz
        # Find R peaks
        rpeaks, = bp.ecg.hamilton_segmenter(signal=win, sampling_rate=ds)
        rpeaks, = bp.ecg.correct_rpeaks(signal=win, rpeaks=rpeaks, sampling_rate=ds)
        # Normalize data
        norm = (win - min(win))/(max(win)-min(win))
        # Calculate median distance between rpeaks (in samples) and use this as period
        diffs = []
        for index, r in enumerate(rpeaks):
            if index > 0:
                diffs.append(r-rpeaks[index-1])
        period = stat.median(diffs)
        # Extract individual heartbeats
        for r in rpeaks:
            if r > beatLength/2 and len(win)-r > beatLength/2:
                beat = norm[r-int(period/2):r+int(period/2)] # Exctract data surrounding r-peak
                beat = np.pad(beat, (0,beatLength - len(beat)), 'constant') # Pad beat with zeros if it is short
                ctrlBeats.append(beat)

# Extract abnormal patient heartbeats
abnBeats = []
for i in range(2, 3):
    for signal in abnSignals:
        # Grab 10s window of data
        win = signal[i*winLength:i*winLength + winLength] # Fs is 1000Hz, therefore a 10s window is 10000 samples
        win = sigproc.resample(win, int(winLength*ds/fs)) # Resample 10 seconds of data to 400Hz
        # Find R peaks
        rpeaks, = bp.ecg.hamilton_segmenter(signal=win, sampling_rate=ds)
        rpeaks, = bp.ecg.correct_rpeaks(signal=win, rpeaks=rpeaks, sampling_rate=ds)
        # Normalize data
        norm = (win - min(win))/(max(win)-min(win))
        # Calculate median distance between rpeaks (in samples) and use this as period
        diffs = []
        for index, r in enumerate(rpeaks):
            if index > 0:
                diffs.append(r-rpeaks[index-1])
        period = stat.median(diffs)
        # Extract individual heartbeats
        for r in rpeaks:
            if r > beatLength/2 and len(win)-r > beatLength/2:
                beat = norm[r-int(period/2):r+int(period/2)] # Exctract data surrounding r-peak
                beat = np.pad(beat, (0,beatLength - len(beat)), 'constant') # Pad beat with zeros if it is short
                abnBeats.append(beat)

# Append labels to dataset (0 for normal, 1 for abnormal)
ctrlY = np.zeros(shape=(len(ctrlBeats), 1))
abnY = np.ones(shape=(len(abnBeats), 1))
ctrlBeats = np.append(ctrlBeats, values=ctrlY, axis=1)
abnBeats = np.append(abnBeats, values=abnY, axis=1)

# Print info about data to be exported
print(len(ctrlBeats), " samples for control patient data\n")
print(len(abnBeats), " samples for abnormal patient data\n")

# Export data as csv
ctrlBeats = np.asarray(ctrlBeats)
abnBeats = np.asarray(abnBeats)
np.savetxt('data/ptb-400hz_normal-v2.csv', ctrlBeats, fmt='%f', delimiter=',')
np.savetxt('data/ptb-400hz_abnormal-v2.csv', abnBeats, fmt='%f', delimiter=',')


