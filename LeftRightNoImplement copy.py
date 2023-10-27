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
serialInst.port = "COM5"
serialInst.baudrate = 500000
serialInst.open()

print("Program start")

start = time.time()
serialInst.write("0".encode())
state = 0
left_tp = 0
right_tp = 0
left_state = 0
right_state = 0
left_timeperiod = 0
right_timeperiod = 0
time_ignore = 0
left_flag = False
right_flag = False

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


                #Condition for Going Straight
                if received_value > 480 and received_value < 700:
                    if state == 0:
                        print("SSSSSSSSSSSSSSSSSSS")
                    if left_state == 1:
                        if left_timeperiod > 100 and left_flag == False:
                            left_flag = True
                            print("LLLLLLLLLLLLLLLLLLL")
                        else:
                            left_timeperiod += 1
                    if right_state == 1:
                        if right_timeperiod > 100  and right_flag == False:
                            right_flag = True
                            print("RRRRRRRRRRRRRRRRRRR")
                        else:
                            right_timeperiod += 1

                #Condition for Goig Right
                elif received_value < 480:
                    if left_state == 1:
                        state = 0
                        time_ignore = 0
                        left_tp = 0
                        right_tp = 0
                        left_state = 0
                        left_timeperiod = 0
                        left_flag = False
                    else:
                        if right_tp > 8 and time_ignore > 35:
                            right_state = 1
                            state = 2
                        else:
                            right_tp += 1
                
                #Condition for Going Left
                elif received_value > 700:
                    if right_state == 1:
                        state = 0
                        time_ignore = 0
                        left_tp = 0
                        right_tp = 0
                        right_state = 0
                        right_timeperiod = 0
                        right_flag = False
                    else:
                        if left_tp > 8 and time_ignore > 35:
                            left_state = 1
                            state = 1
                        else:
                            left_tp += 1

                time_ignore += 1
                
    except:
        break


            
