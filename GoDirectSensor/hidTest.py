import hid
import pyhidapi
import numpy as np
from hid import hidapi

VID = 0x08f7
PID = 0x0010
buff = np.zeros(10)


for d in hid.enumerate(VID, PID):
    print(d['path'])
    print(VID)
    print(PID)
    print(d['product_string'])
    device = hid.Device(vid=VID, pid=PID)
    dev = hid.hidapi.open(vid=VID, pid=PID)
    num = hid.hidapi.hid_write(dev, buff, len(buff))
    #device.write(buff)
