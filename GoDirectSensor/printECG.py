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
recording1 = []
recording2 = []
chunked = []
for i in range(0,100):
    chunk = gdx.read_chunk() #returns a list of measurements from the sensors selected.
    data = np.squeeze(chunk)
    recording1.append(data)
    #recording2.append(data[1])
    if chunk == None: 
        break 
    print(time.time() - ts)
    print(np.shape(chunk))
    chunked = chunk


recording1 = np.asarray(recording1)
recording1 = recording1.flatten()
# recording2 = np.asarray(recording2)
# recording2 = recording2.flatten()
print(np.shape(recording1))
plt.plot(recording1)
plt.show()

# Close sensor
gdx.stop()
gdx.close()