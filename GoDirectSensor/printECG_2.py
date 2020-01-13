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

gdx.select_sensors(sensors=1)
gdx.start_fast() 

ts = time.time()
recording = []
for i in range(0,50):
    chunk = gdx.read_all() #returns a list of measurements from the sensors selected.
    if chunk == None: 
        break 
    print(time.time() - ts)
    print(np.shape(chunk))

chunk = np.asarray(chunk)
chunk = chunk.flatten()
print(np.shape(chunk))
plt.plot(chunk)
plt.show()

# Close sensor
gdx.stop()
gdx.close()