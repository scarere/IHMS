import gdx as gd #the gdx function calls are from a gdx.py file inside the gdx folder
import matplotlib.pyplot as plt
import time
import numpy as np

# Open sensor
gdx = gd.gdx()
gdx.open_usb()

# Print sensor info
device_info = gdx.device_info()
battery_level = device_info[2]
charger_state = device_info[3]  
print("battery level % = ", battery_level)
print("charger state = ", charger_state)

gdx.select_sensors()
gdx.start_fast() 

ts = time.time()
for i in range(0,10):
    measurements = gdx.read_chunk() #returns a list of measurements from the sensors selected.
    if measurements == None: 
        break 
    print(time.time() - ts)
    print(np.shape(measurements))

# Close sensor
gdx.stop()
gdx.close()