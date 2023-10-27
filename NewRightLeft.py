"""
Program detects if eyes are in left or right
Electrode placements: Black(-in) left side and Red(+)right side (from the patient's POV) on forehead, Yellow(Ref) on ear lobe
"""

import serial
import matplotlib.pyplot as plt
import time
import numpy as np
import csv

#Creating an instance object 
serialInst = serial.Serial()

#Setting up the connection
serialInst.port = "COM3"
serialInst.baudrate = 500000
serialInst.open()

serialRemote = serial.Serial("COM4",115200)

print("Program start")

start = time.time()
serialInst.write("0".encode())

#Counter Declaration
counter = 0
dir_data = []
time_ignore = 0

while True:
    try:
        counter += 1
        #print(f"Counter : {counter}")
        if counter > 200:
            #Popping 10 samples from the list and adding new samples into it
            #print(f"*****{serialInst.in_waiting}*******")
            if serialInst.in_waiting > 10:
                starttime = time.time()
                counter += 1
                bytes = serialInst.read(2)
                received_value = int(bytes[0] + (bytes[1] << 8))
                dir_data.append(received_value)

                #Condition for Going Right
                if all(x > 650 for x in dir_data) and time_ignore > 150:
                    print("LLLLLLLLLLLLLLLLL")
                    time_ignore = 0
                
                #Condition for Going Left
                elif all(x < 480 for x in dir_data) and time_ignore > 150:
                    print("RRRRRRRRRRRRRRRR")
                    time_ignore = 0
                
                time_ignore += 1
                
                #print(dir_data)
                print(f"TIME IGNORE {time_ignore}")

                if len(dir_data) == 3:
                    dir_data.pop(0)          
    
    except:
        break


            
