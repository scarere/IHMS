import numpy as np
import statistics as stat
import matplotlib.pyplot as plt
import wfdb # Official Physionet API for loading databases into python
import biosppy as bp
from scipy import signal as sigproc
import time
from sk_dsp_comm import fir_design_helper as fir_d

# Get time reference
ts = time.time()

print(' 0.00s - Loading Data From CSV ...')

# Import list of recordings from ptb database
records = wfdb.get_record_list('mitdb')

fs = 360
ds = 200
winLength = 10*fs
beatLength = 2*fs
beatLengthResampled = 2*ds
signals = []
annotations = []
for record in records:
    signal, field = wfdb.rdsamp('data/mit-original-1.0.0/' + record)
    ann = wfdb.rdann('data/mit-original-1.0.0/' + record, extension='atr', summarize_labels=True)
    signals.append(signal[:,0]) # Append only the first channel (lead) recording/signal
    annotations.append(ann) # Append annotations

# Heartbeat Extraction
tc = time.time() - ts
print('%.2fs - Extracting Heartbeats ...' % tc)

beats = []
for sigIndex, signal in enumerate(signals): # iterate through all of the signals
    #print(ann.contained_labels)
    # Update on current signal
    tc = time.time() - ts
    print('%.2fs - Processing Signal ' % tc, sigIndex, ' of 48', end='\r')

    ann = annotations[sigIndex] # Get Annotation Object associated with signal

    # Normalize data
    norm = (signal - min(signal))/(max(signal)-min(signal))

     # Find R peaks
    rpeaks, = bp.ecg.hamilton_segmenter(signal=signal, sampling_rate=fs)
    rpeaks, = bp.ecg.correct_rpeaks(signal=signal, rpeaks=rpeaks, sampling_rate=fs)

    # Calculate median distance between rpeaks within window (in samples) and use this as period
    diffs = []
    for index, r in enumerate(rpeaks):
        if index > 0:
            diffs.append(r-rpeaks[index-1])
    period = stat.median(diffs)

    for index, peak in enumerate(ann.sample):

        if peak > beatLength/2 and len(signal)-peak > beatLength/2:

            beat = norm[peak-int(period/2):peak+int(period/2)] # Exctract data surrounding r-peak
            beat = sigproc.resample(beat, int(beatLengthResampled*ds/fs)) 

            # Check length of beat and either truncate or pad it
            if (len(beat)>beatLengthResampled):
                beat = beat[0:beatLengthResampled]
            else:
                beat = np.pad(beat, (0,beatLengthResampled - len(beat)), 'constant') # Pad beat with zeros if it is short
            
            # Classify beat
            if (ann.symbol[index] == 'N' or ann.symbol[index] == 'L' or ann.symbol[index] == 'R' 
                or ann.symbol[index] == 'e' or ann.symbol[index] == 'j'):
                beat = np.append(beat, [0], axis=0)
                beats.append(beat)
                #print('Just N')
                
            elif (ann.symbol[index] == 'a' or ann.symbol[index] == 'A' or ann.symbol[index] == 'J' or ann.symbol[index] == 'S'):
                beat = np.append(beat, [1], axis=0)
                beats.append(beat)
                #print('just an S')

            elif (ann.symbol[index] == 'V' or ann.symbol[index] == 'E'):
                beat = np.append(beat, [2], axis=0)
                beats.append(beat)
                #print('found V')

            elif (ann.symbol[index] == 'F'):
                beat = np.append(beat, [3], axis=0)
                beats.append(beat)
                #print('found F')

            elif (ann.symbol[index] == '/' or ann.symbol[index] == 'f' or ann.symbol[index] == 'Q'):
                beat = np.append(beat, [4], axis=0)
                #print('BIG Q')
                beats.append(beat)

tc = time.time() - ts
print('%.2fs - Exporting Data to CSV ...' % tc )                
beats = np.asarray(beats)
np.savetxt('data/mit-200hz-v1.csv', beats, fmt='%f', delimiter=',')
tc = time.time() - ts
print('%.2fs - End\n' % tc )

classnum, class_counts = np.unique(beats[:, -1], return_counts=True)
classes = ['Normal', 'Premature', 'Ventricular', 'Fusion of V and N', 'Unclassifiable']
IDs = ['N', 'S', 'V', 'F', 'Q']

print(np.shape(beats))
for index, num in enumerate(classnum):
    print(IDs[int(num)], ' - ', classes[int(num)], ': ', class_counts[index])

