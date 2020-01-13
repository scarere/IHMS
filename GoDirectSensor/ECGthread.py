from multiprocessing import Process, Queue
import gdx as gd
import numpy as np
import time
import matplotlib.pyplot as plt

def collect_data(dataq, timeq):
    # Open sensor
    gdx = gd.gdx()
    gdx.open_usb()
    gdx.select_sensors(sensors=[1])
    gdx.start_fast(period=8) 
    ts = time.time()
    while(True):
        try:
            chunk = gdx.read_chunk() #returns a list of measurements from the sensors selected.
            data = np.asarray(chunk)
            data = data.flatten()
            dataq.put(data)
            timeq.put(time.time() - ts)
        except (KeyboardInterrupt, SystemExit):
            print("Exit")
            raise


def main():
    q1 = Queue()
    q2 = Queue()

    p1 = Process(target=collect_data, args=(q1, q2,))
    p1.start()
    


    print("Process Started")

    recording = []
    for i in range(0,50):
        chunk = q1.get()
        data = np.squeeze(chunk)
        tc = q2.get()
        print((tc), ": ", np.shape(data))
        recording.append(data)

    p1.terminate()
    recording = np.asarray(recording)
    recording = recording.flatten()
    print(np.shape(recording))
    plt.plot(recording)
    plt.show()

if __name__ == "__main__":
    main()
    

    
