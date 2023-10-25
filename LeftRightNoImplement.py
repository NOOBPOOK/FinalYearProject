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

print("Program start")

left = 0
right = 0
no_straight = 0
start = time.time()
serialInst.write("0".encode())
state = 0

#Counter Declaration
counter = 0

while True:
    try:
        counter += 1
        #print(f"Counter : {counter}")
        if counter > 200:
            #Popping 10 samples from the list and adding new samples into it
            #print(f"*****{serialInst.in_waiting}*******")
            if serialInst.in_waiting > 1:
                starttime = time.time()
                counter += 1
                bytes = serialInst.read(2)
                received_value = int(bytes[0] + (bytes[1] << 8))
                #print(received_value)
                
                if received_value > 400 and received_value < 750:
                    if state != 0:
                        if no_straight > 5:
                            state = 0
                            print("You are looking Straight")
                            left = 0
                            right = 0
                            no_straight = 0
                        else:
                            no_straight += 1
                    else:
                        print("You are looking Straight")
                elif received_value < 400:
                    if state != 2:
                        left += 1
                        if left > 10:
                            print("LLLLLLLLLLLLLLLLLLLLLLLLL")
                            left = 0
                            state = 1
                            right = 0
                elif received_value > 750:
                    if state != 1:
                        right += 1
                        if right > 10:
                            right = 0
                            print("RRRRRRRRRRRRRRRRRRRRRRRRRRR")
                            state = 2
                            left = 0
                
    except:
        break


            
