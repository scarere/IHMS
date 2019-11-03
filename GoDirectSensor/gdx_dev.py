from godirect import GoDirect

import logging
import time                 #Ex all new ones

logging.basicConfig()
#logging.getLogger('godirect').setLevel(logging.DEBUG)
#logging.getLogger('pygatt').setLevel(logging.DEBUG)
logging.getLogger('bleak').propagate = False

class gdx:

    selected_device = None
    selected_device2 = None
    selected_sensors = []
    selected_sensors2 = []
    buffer = []
    buffer2 = []

    
    def __init__(self):

        self.godirect = GoDirect(use_ble=False, use_usb=False) # testing a way to control USB and BLE
        self.ble_open = False #used to keep track of when godirect.__init__(use_ble) is called. 
        #Do not want to call it twice
    


    def open_usb(self):
        """ Discovers the Go Direct device with a USB connection and opens that device
        for data collection. If there are multiple devices discovered, a list of devices
        is printed to the terminal with a prompt for the user to choose one. 
		""" 
        self.godirect.__init__(use_ble=False, use_usb=True)

        found_devices = self.godirect.list_devices()
        number_found_devices = len(found_devices)
        print("Number of usb devices found = " +str(number_found_devices))
           
        if number_found_devices == 1: # if there is one device, select that one.
            gdx.selected_device = found_devices[0]
            print("USB device = ", found_devices[0])

        elif number_found_devices == 2: # if there are two devices, select both.
            if number_found_devices > 2:
                print ("only two USB devices will be connnected")
            gdx.selected_device = found_devices[0]
            gdx.selected_device2 = found_devices[1]

            print("USB devices = ", found_devices[0], ", ", found_devices[1])           
    
        elif number_found_devices == 0: # if there are no found devices
            print("No Go Direct Devices found on USB")
        
        # now we check to see if a device was selected (in one of the cases above)
        # If so, then open that device 

        if gdx.selected_device != None:
            open_device_success = gdx.selected_device.open()
            print("USB Device successfully opened = ", open_device_success)

        if gdx.selected_device2 != None:
            open_device2_success = gdx.selected_device2.open()           
            print("USB Device 2 successfully opened = ", open_device2_success)


    def open_ble(self,device_to_open=None, device2_to_open=None):
        """ Open a Go Direct device via bluetooth for data collection. 
        
        Args: 
            device_to_open: Set to None to receive a list of all discovered Go Direct 
        devices for the user to choose one. Set to a specific Go Direct device name, 
        for example "GDX-FOR 071000U9", to open that device. Set to "proximity_pairing"
        to open the device with the highest rssi (closest proximity).
		""" 
        if self.ble_open == False:
            print("Wait for device to connect via ble...")
            self.godirect.__init__(use_ble=True, use_usb=False)

        #print("Begin search for ble devices...")
        found_devices = self.godirect.list_devices() #find all available bluetooth devices 
        number_found_devices = len(found_devices)
        print("Number of ble devices found = " +str(number_found_devices))
        
        # were any ble devices found? If so, the code below will determine which one to open
        # and then open it        
        if number_found_devices >= 1: 
             
            # the case below occurs when the device_to_open parameter = "proximity_pairing"
            # In the for loop each device, in the list of found_devices, is pulled out
            # that device's rssi is compared to the previous highest rssi
            # the device with the highest rssi is stored as the device to open                
            if device_to_open == "proximity_pairing": 
                print ("Begin proximity pairing")
                i=1
                rmax=-99
                dmax=0
                for device in found_devices:
                    print(str(i)+": "+str(device))
                    v=device.rssi
                    if v>rmax:
                        dmax=i
                        rmax=v
                        print("rmax: ", rmax," dmax: ", dmax)
                    i+= 1
                x=dmax
                selected = int(x)
                if selected <= number_found_devices:
                    gdx.selected_device = found_devices[selected-1]
                    print("proximity device to open = ", found_devices[selected-1] )
                else:
                    print("Proximity selection was invalid")


            # the case below occurs when there is a device_to_open parameter, like "GDX-FOR 071000U9"
            # In the for loop each device, in the list of found_devices, is pulled out
            # that found device's name is compared to the device_to_open parameter name
            # if the names match, then we store this device as the device to open               
            elif device_to_open != None: 
                print("Searching for a device with name ", device_to_open)
                for device in found_devices: 
                    if device_to_open == str(device.name):
                        print("device_to_open_found = True")
                        gdx.selected_device = device 
                        break #a match was made, break out of the loop
                if device2_to_open != None:
                    for device in found_devices:
                        print("Searching for a device2 with name ", device2_to_open)
                        if device2_to_open == str(device.name):    
                            print("device2_to_open_found = True")
                            gdx.selected_device2 = device 
                            break #a match was made, break out of the loop               

            
            # the case below occurs when there is no device_to_open parameter. In this case,
            # provide a list of all discovered ble sensors and the user chooses one or two.          
            elif device_to_open == None: 
                print("Found " +str(number_found_devices) + " devices:")
                i=1
                for d in found_devices:
                    print(str(i)+": "+str(d))
                    i += 1
                print("Select up to two devices separated by spaces:", end=' ')
                user_selected_device = []
                for s in input().split(' '):
                    user_selected_device.append(int(s))
                    print("user selected device = ", user_selected_device)
             
                    selected = int(user_selected_device[0])
                if selected < number_found_devices:
                    gdx.selected_device = found_devices[selected-1]
                else:
                    print("Selection was invalid")
        

            
            
            # now we check to see if a device was selected (in one of the cases above)
            # If so, then open that device               
            if gdx.selected_device != None:
                open_device_success = gdx.selected_device.open()
                print("BLE device successfully opened = ", open_device_success)
            if gdx.selected_device2 != None:
                open_device2_success = gdx.selected_device2.open()
                print("BLE device2 successfully opened = ", open_device2_success)		

        else:
            print("No Go Direct Devices Found on Bluetooth")
     
           

    def select_sensors(self, sensors=None, dev2=False): #sensor is a list, such as [1,3,4]
        """ Select the sensors (by number) to enable for data collection. Note that the sensors are
        not enabled in this function, that happens in the start() function.
        
        Args: 
            sensors []: if sensors is left blank, a list of all available sensors is provided
            by a prompt in the terminal for the user to select from. Otherwise, enter a list of sensor numbers
            such as [1,2,3]
		""" 

        if dev2 == False: #this first code sets up dev1. If dev2 = True, then do not call this code.
            if gdx.selected_device == None:
                return 
            device = gdx.selected_device

        elif dev2 == True: #is this function being called to configure dev2? then use this code
            if gdx.selected_device2 == None:
                return 
            device = gdx.selected_device2

        selected_sensors = []# need to clear out the sensors list each time we call 

        if sensors == None: #if the sensors parameter is left blank provide an input prompt for the user to select sensors
            sensors = device.list_sensors()
            for i in sensors:
                c = sensors[i]
                print(str(c))
            print("Select sensors separated by spaces:", end=' ')
            for s in input().split(' '):
                selected_sensors.append(int(s))

        else:
            for sensor in sensors:  #if the user did input a list of sensors as a paramter, then store that list
                selected_sensors.append(sensor)  

        if dev2 == False: #this first code sets up dev1. If dev2 = True, then do not call this code.
            gdx.selected_sensors = selected_sensors
        elif dev2 == True:
            gdx.selected_sensors2 = selected_sensors


    
    def start(self, period=None):
        """ Enables the sensors that were selected in the select_sensors() function 
        and then starts data collection.
        
        Args: 
            period (int): If period is left blank, a prompt in the terminal allows the user to enter
            the period. Otherwise, enter a period in milliseconds, e.g. 1000
		"""        
        
        if gdx.selected_device == None:
            return 

        if period == None: #if the period parameter is left blank, user prompted to enter the period
            print("Select period (ms):", end=' ')
            period = int(input())

        gdx.selected_device.enable_sensors(sensors=gdx.selected_sensors)
        print("enabled sensors = ", gdx.selected_sensors)
        
        if gdx.selected_device2 != None:
            gdx.selected_device2.enable_sensors(sensors=gdx.selected_sensors2)
            print("enabled sensors2 = ", gdx.selected_sensors2)

        
        gdx.selected_device.start(period=period)
        
        if gdx.selected_device2 != None:
            gdx.selected_device2.start(period=period)

    def read(self, dev2=False):             

        """ Same functionality as read() above, however value sensor.values is copied into
        values[] by value instead of by reference, allowing sensor.clear() to be called.
        Only the most recent measurements are returned from readValues() and then cleared
        from both sensor.values and values[]
		Returns:
		    value[]: a list that includes a data point from each of the enabled sensors
		"""
        
        retvalues = []  
        values = []       
        
        # This code either retrieves the buffer data, or reads new data, from dev1 (this is not dev2)
        if dev2 == False: 
            if gdx.selected_device == None:
                return 
            device = gdx.selected_device
            # Use a try/except because you will get an error if you call len() on an empty list
            try:
                # Is there data in the buffer? If so, we use that data as the data to return.
                # We won't call code to read more data until the buffer is cleared.
                if len(gdx.buffer[0]) != 0:
                    store_buffer = gdx.buffer
                    gdx.buffer = []
                    
                    # This code indexes out each sensor channel's list of data (from the buffer).
                    # The most recent data point is pulled from each channel's list, to be returned.
                    # The remaining data in each list (if any) is stored back into the buffer.
                    for j in store_buffer:
                        values[:] = j
                        pop_values = values.pop(0)
                        retvalues.append(pop_values)
                        gdx.buffer.append(values)
                        values = []
                    return retvalues 
            except:
                pass    
                
            # If there was data in the buffer, this code is never called.
            # But if no data in the buffer, then we use this code to get new data.
            # If sample rate is fast, each channel may return multiple data points.
            # This is why the buffer is a list of lists.
            if device.read():
                gdx.buffer = []
                sensors = device.get_enabled_sensors()
                if sensors != None:
                    for sensor in sensors: 
                        # The sensor.values call may read one sensor value, or multiple sensor values (if fast sampling)
                        values[:] = sensor.values
                        # Pull the first value off the values list
                        pop_values = values.pop(0)
                        # Build a list of each channel's first value (this builds the return list)
                        retvalues.append(pop_values)
                        # Build a list of lists for each channel's data that is not returned
                        gdx.buffer.append(values)
                        sensor.clear()
                        values = []
                    return retvalues
            else:
                return None

          
        # This code either retrieves the buffer data, or reads new data, from dev2 (this is not dev1)
        elif dev2 == True: 
            if gdx.selected_device2 == None:
                return 
            device = gdx.selected_device2         
            # Use a try/except because you will get an error if you call len() on an empty list
            try:
                # Is there data in the buffer? If so, we use that data as the data to return.
                # We won't call code to read more data until the buffer is cleared.
                if len(gdx.buffer2[0]) != 0:
                    store_buffer = gdx.buffer2
                    gdx.buffer2 = []
                    
                    # This code indexes out each sensor channel's list of data (from the buffer).
                    # The most recent data point is pulled from each channel's list, to be returned.
                    # The remaining data in each list (if any) is stored back into the buffer.
                    for j in store_buffer:
                        values[:] = j
                        pop_values = values.pop(0)
                        retvalues.append(pop_values)
                        gdx.buffer2.append(values)
                        values = []
                    return retvalues 
            except:
                pass    
                
            # If there was data in the buffer, this code is never called.
            # But if no data in the buffer, then we use this code to get new data.
            # If sample rate is fast, each channel may return multiple data points.
            # This is why the buffer is a list of lists.
            if device.read():
                gdx.buffer2 = []
                sensors = device.get_enabled_sensors()
                if sensors != None:
                    for sensor in sensors: 
                        # The sensor.values call may read one sensor value, or multiple sensor values (if fast sampling)
                        values[:] = sensor.values
                        # Pull the first value off the values list
                        pop_values = values.pop(0)
                        # Build a list of each channel's first value (this builds the return list)
                        retvalues.append(pop_values)
                        # Build a list of lists for each channel's data that is not returned
                        gdx.buffer2.append(values)
                        sensor.clear()
                        values = []
                    return retvalues
            else:
                return None
    
    def stop(self):
        """ Stop data collection on the enabled sensors.
		"""       
        if gdx.selected_device == None:
            return 
        gdx.selected_device.stop()

        if gdx.selected_device2 == None:
            return 
        gdx.selected_device2.stop()



    def close(self):
        """ Disconnect the USB or BLE device if a device is open.
        """
        if gdx.selected_device != None:
            gdx.selected_device.close()
        
        if gdx.selected_device2 != None:
            gdx.selected_device2.close()

        self.ble_open = False
        self.godirect.quit()  



    def device_info(self, dev2=False):
        """ Returns information about the device. The device must be opened first, 
        using the open() function, before this function can be called.

		Returns:
		    device_info[]: a list that includes name, description, battery %, charger state, rssi
		"""        
        
        if dev2 == False: #this first code sets up dev1. If dev2 = True, then do not call this code.
            if gdx.selected_device == None:
                return 
            device = gdx.selected_device
        elif dev2 == True: #is this function being called to configure dev2? then use this code
            if gdx.selected_device2 == None:
                return 
            device = gdx.selected_device2            
                
        device_info = []  # 0 = name, 1 = description, 2 = battery %, 3 = charger state, 4 = rssi

        device_info.append(device._name)
        device_info.append(device._description)
        device_info.append(device._battery_level_percent) 
        charger_state = ["Idle", "Charging", "Complete", "Error"]  
        device_info.append(charger_state[device._charger_state])
                    # int:  0 = Idle, 1 = Charging, 2 = Complete, 3 = Error
        device_info.append(device._rssi)
        return device_info  


    def enabled_sensor_info(self, dev2=False):
        """ Returns the description and units (good for column headers) 
        of the sensors that have been enabled for data collection.

		Returns:
		    sensor_info[]: a list of each enabled sensors' description with 
            units, e.g. ['Force (N)', 'X-axis acceleration (m/s²)', 'X-axis gyro (rad/s)']
		"""                
        if dev2 == False: #this first code sets up dev1. If dev2 = True, then do not call this code.
            if gdx.selected_device == None:
                return 
            device = gdx.selected_device
        elif dev2 == True: #is this function being called to configure dev2? then use this code
            if gdx.selected_device2 == None:
                return 
            device = gdx.selected_device2 
        
        sensors = device.get_enabled_sensors()
        sensor_info = []
        for sensor in sensors:
            info = sensor.sensor_description + " (" + sensor.sensor_units + ")"
            sensor_info.append(info)
        return sensor_info


    def sensor_info(self):
        """ Information about all of the sensors that are on an open device. Note that this is different
        than the enabled_sensor_info() function, which provides a description of only those sensors
        that were enabled for data collection.

		Returns:
		    available_sensors[]: a list within a list of each sensor's number, description, 
            and units.
		"""         
        if gdx.selected_device == None:
            return 
        sensors = gdx.selected_device.list_sensors()
        available_sensors = []  # 0 = sensor number, 1 = description, 2 = units, 3 = incompatible sensors
        
        all_sensor_numbers = [] # mnake this list first so that we can use it later when looking at exclusion mask
        for i in sensors:
            c = sensors[i]
            sensor_number = c.sensor_number
            all_sensor_numbers.append(sensor_number)
        
        for i in sensors:
            incompatible_sensors = []
            c = sensors[i]
            sensor_number = c.sensor_number
            sensor_description = c.sensor_description
            sensor_units = c.sensor_units
            exclusion_mask = c._mutual_exclusion_mask
            bin_string = format(exclusion_mask, '32b')   
            answer =  [x == '1' for x in bin_string[::-1]] # answer is a True False array [TRUE, TRUE, FALSE]
            # the bin-string and formating converts the mutual exclusion mask to an array of Trues and Falses 
            # representing the mask. the bin_string contents are reversed (with [::-1]) because string 
            # formatting formats the number the way we read it - most significant bit first,
            i = 0
            for channel in answer: #change the True/False list to a list of sensor numbers. e.g, [TRUE, TRUE, FALSE] = [1,2]
                if channel == True and i in all_sensor_numbers: #and i is a sensor number that is also an actual sensor
                    incompatible_sensors.append(i)
                i+=1  
            available_sensors.append([sensor_number, sensor_description, sensor_units, incompatible_sensors])
            
        return available_sensors # [[Sensor1 number, Sensor1 description, Sensor1 units, Incopatible1 Sensors], [Sensor2 number, Sensor 2 description, Sensor 2 units, Incopatible1 Sensors]]


 
    def discover_ble_devices(self):
        """ Enables bluetooth, and returns the name and rssi of all discovered GoDirect devices. 
        This function should be called prior to opening a device. The name returned 
        by this function can be used in ble_open() to open a specific device. 

		Returns:
		    discovered_ble_devices[]: a list within a list of name and rssi for each device
            [[name1,rssi1],[name2,rssi2],[name3,rssi3]]
		""" 
        self.godirect.__init__(use_ble=True, use_usb=False)
        self.ble_open = True

        print("Begin search for ble devices...")
        found_devices = self.godirect.list_devices() #find all available bluetooth devices 
        number_found_devices = len(found_devices)
        #print("Number of ble devices found = " +str(number_found_devices))
        discovered_ble_devices = []
                
        if number_found_devices >= 1:
            for device in found_devices:
                #print(device)
                device_name = device.name
                device_rssi = device.rssi
                #print("device name = ", device_name)
                #print("device rssi = ", device_rssi) #you can get rssi before opening the device
                discovered_ble_devices.append([device_name, device_rssi])
            
        return discovered_ble_devices


    def monitor_rssi(self, init=False):
        """ Enables bluetooth, and returns the name and rssi of all discovered GoDirect devices. 
        This function should be called prior to opening a device. The name returned 
        by this function can be used in ble_open() to open a specific device. 

		Returns:
		    discovered_ble_devices[]: a list within a list of name and rssi for each device
            [[name1,rssi1],[name2,rssi2],[name3,rssi3]]
		""" 
        if init == True:

            self.godirect.__init__(use_ble=True, use_usb=False)
            self.ble_open = True

            print("Begin search for ble devices...")
        
        found_devices = self.godirect.list_devices() #find all available bluetooth devices 
        number_found_devices = len(found_devices)
        #print("Number of ble devices found = " +str(number_found_devices))
        discovered_ble_devices = []
                
        if number_found_devices >= 1:
            for device in found_devices:
                #print(device)
                device_name = device.name
                device_rssi = device.rssi
                #print("device name = ", device_name)
                #print("device rssi = ", device_rssi) #you can get rssi before opening the device
                discovered_ble_devices.append([device_name, device_rssi])
            
        return discovered_ble_devices
 




  
        

   