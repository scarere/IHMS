import gdx as gd #the gdx function calls are from a gdx.py file inside the gdx folder
import matplotlib.pyplot as plt
import time
import numpy as np

# Open Sensor
gdx = gd.gdx()
gdx.open_usb()

# Initialize Variables
fs = 200 # sampling frequency in hz
buffer = [] # Buffer to hold sensor data
winLength = 10 # Length of window in seconds

# Select sensor and sampling rate using console input
gdx.select_sensors()
gdx.start_fast(period=1000/fs)

while(true):
    while(len(buffer) < fs*window):
        data = gdx.read_chunk()
        buffer.append(data)
    
    window = buffer[0:winLength*fs]
    