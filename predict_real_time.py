from multiprocessing import Process, Queue
from datasetProc.tools import extract_heartbeats
import GoDirectSensor.gdx as gd
import numpy as np
import time
from keras.models import load_model


# Change error settings
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # or any {'0', '1', '2'}
import tensorflow as tf

def collect_data(dataq, timeq, sensor, period):
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
    gdx.select_sensors(sensors=[sensor])
    gdx.start_fast(period=period)

    # Get Start Time
    ts = time.time()
    while(True):
        try:
            chunk = gdx.read_chunk() #returns a list of measurements from the sensors selected.

            # Reshape data
            data = np.asarray(chunk)
            data = data.flatten()

            # Push data and a timestamp to respective queue's
            dataq.put(data)
            timeq.put(time.time() - ts)
        except (KeyboardInterrupt, SystemExit):
            print("Exit")
            raise

def select_sensor():
    # List of available channels in order
    sensors = ['ECG (mV)', 'Heart Rate (bpm)', 'EMG (mV)', 'EMG Rectified (mV)', 'Voltage (mV)']

    # Ask user which channel to get data from
    for index, sensor in enumerate(sensors):
        print((index+1), ' - ', sensor)
    print('Please select sensor by number: ', end=' ')
    sensor = int(input())
    print()

    # Return integer that represents sensor
    return sensor

def select_period():
    # Ask user what period to use
    print('Please select period (ms): ', end=' ')
    period = int(input())
    print()

    # return period
    return period

def select_winLength():
    # Ask user what winLength to use. winLength is the length in seconds, of data to record before making predictions
    print('Print Select the buffer window length (s): ', end=' ')
    winLength = int(input())
    print()

    # Return winLength
    return winLength

def select_model():
    models = ['mit-v1', 'ptb-v1-A', 'ptb-v1-B', 'ptb-v3-A', 'ptb-v3-B', 'ptb-v5-A']

    for index, model in enumerate(models):
        print(index+1, ' - ', model)
    print('Please select which model to use by number: ', end=' ')
    model = int(input())
    return models[model-1]

def main():
    # Initialize Variables
    sensor = select_sensor()
    period = select_period()
    fs = int(1/period*1000) # sampling frequency in hz
    #winLength = select_winLength()
    winLength = 10
    buffer = [] # Buffer to hold sensor data
    modelname = select_model()
    print(modelname)

    # Load model
    model = load_model('MachineLearning/models/model-' + modelname + '.h5')
    #model = load_model('MachineLearning/models/model-mit-v1.h5')

    # Create Queue's To Pass Data from collect_data process to main process
    dataq = Queue()
    timeq = Queue()

    # Create and Start Data Collection Process
    dataproc = Process(target=collect_data, args=(dataq, timeq, sensor, period))
    dataproc.start()

    print("Data Collection Process Started ...\n")
    while(True):
        # Get Chunk of data from Data Queue
        chunk = dataq.get()
        tc = timeq.get()
        #print(tc)

        # Add Chunk of data to buffer
        if len(buffer) == 0: # Check if buffer is empty
            buffer = chunk
            #print(np.shape(buffer))
        else:
            buffer = np.append(buffer, chunk, axis=0)
            #print(np.shape(buffer))


        if len(buffer) > fs*winLength:
            #print("Processing Window...")
            # Seperate a window from buffer
            win = buffer[0:fs*winLength]
            buffer = buffer[fs*winLength:]

            # Extract heartbeats from window
            beats = extract_heartbeats(win=win, fs=fs, beatWin=2)
            print(np.shape(beats))
            beats = np.expand_dims(beats, 2)
            print(np.shape(beats))

            # Get Predictions
            predictions = model.predict(beats, batch_size=len(beats))
            if 'mit' in modelname:
                classes = ['N', 'S', 'V', 'F', 'Q']
                for pred in predictions:
                    print(classes[np.argmax(pred)])
            else:  
                for pred in predictions:
                    if pred[0] > 0.5:
                        print('Normal')
                    else:
                        print('Abnormal')
            # print('Predictions: ', end='')
            # [print(pred, ', ', end='') for pred in predictions]

            # Check if we should end process
            # if input() == 'q' or input() == 'Q':
            #     # Exit loop
            #     break
    
    # Terminate data collection process
    dataproc.terminate()

if __name__ == '__main__':
    main()
    