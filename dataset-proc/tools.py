import numpy as np
import statistics as stat
import biosppy as bp

def extract_hb(win, fs, beatWin=2):
    """ Extracts heartbeats from an ECG recording.

    Given an ECG recording, extracts individual heartbeats and returns them seperately in a list. 
    Beats are normalized, and padded to a fixed length

    Args:
        win (array): A list of voltage values that represent the ECG recording
        fs (int, float): The sampling frequency used to obtain the ECG recording
        beatWin (int, float): The number of seconds that each beat recording should be. If beats are 
            too short they will be padded, if they are too long they will be truncated

    Returns:
        beats: A list of arrays that represent the individual beats within the recording.
    """
    # Calculate beat length in samples
    beatLength = beatWin*fs

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

    # Extract individual heartbeats
    beats = []
    for r in rpeaks:
        if r > beatLength/2 and len(win)-r > beatLength/2:
            beat = norm[r-int(period/2):r+int(period/2)] # Exctract data surrounding r-peak
            # Check length of beat and either truncate or pad it
            if (len(beat)>beatLength):
                beat = beat[0:beatLength]
            else:
                beat = np.pad(beat, (0,beatLength - len(beat)), 'constant') # Pad beat with zeros if it is short
            beats.append(beat)
    
    return beats