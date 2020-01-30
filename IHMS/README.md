# Welcome to IHMS

## Steps for Use

**Step 1:** Ensure you have the necessary requirements in your environment. These can be installed using the following command
```bash
pip install -r requirements.txt
```

**Step 2:** Navigate to the IHMS folder in the IHMS repository within terminal or command line (this folder)

**Step 3:** Create a new folder to store abnormal data. Default is 'savedData'. Name of folder can be changed in IHMS.py

**Step 4:** Plug the Vernier GoDirect sensor into your machine via USB or USB adapter

**Step 5:** Run the following command
```bash
python ihms.py
```

**Step 6:** Press the start button to begin recording and real-time prediction

**Step 7:** Pressing stop will reset the system. Make sure to press stop before closing the window or the sensor will not disconnect properly

## Steps to use visualizer to view savedData

**Step 8:**Run the following command (Can be run in a seperate terminal to have both applications open at once)
```bash
python visualizer.py
```

**Step 9:**Use the drop down menu to select the data which you would like to view. Data is named after the time it was detected/captured

**Step 10:**Click either 'Plot On Graph 1' or 'Plot On Graph 2' to plot the selected data on the desired graph

**Step 11:**You can either select a different data file to display and overwrite what is currently on a graph, or you can use the clear button to clear the data currently displayed

## Possible Errors

### An error occurs during IHMS operation or program did not exit properly:
- The system has not properly closed the sensor and an error will occur the next time you run the IHMS system. Disconnect the sensor from your machine by unplugging the USB and pluggin it back in.



**Further Steps to Come**
