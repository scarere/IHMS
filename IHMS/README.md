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

## Possible Errors

### An error occurs during IHMS operation or program did not exit properly:
- The system has not properly closed the sensor and an error will occur the next time you run the IHMS system. Disconnect the sensor from your machine by unplugging the USB and pluggin it back in.



**Further Steps to Come**
