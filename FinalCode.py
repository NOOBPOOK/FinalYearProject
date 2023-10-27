"""
Final code for EEG Project
Implements Focus, Stop, Left, Right Features
Collects data from Adruino and sends output on another adruino via Bluetooth
Implements no Machine Learning Model
"""

"""
Program takes real time inputs from the user and gives out predictions without need of ML model
Electrode placements: Black(-in) and Red(+)on forehead, Yellow(Ref) on ear lobe
"""

import serial
import matplotlib.pyplot as plt
import time
import numpy as np

#Creating an instance object 
serialInst = serial.Serial("COM5", 500000)

#Creating a remote for controlling the car
serialRemote = serial.Serial("COM6", 115200)

#Sampling rate (that is 100 samples per second)
fs = 100 
frequencies = None
fft_result = None
prev_val_counter = 5            #Defines the no. of past inputs to give for prediction
buffer_period = 200             #Time for buffer to start the process
eeg_data = []                   #Stores the Real Time EEG Data (100 samples)
direction_data = []             #Array to store Direction Data
direction_value = 0             #Actually stores the Direction Data
focus_state = 0                 #0 stands for no focus & 1 stands for full focus
prev_alpha = []                 #Stores the Previous Alpha values
prev_gamma = []                 #Stores the Previous Gamma Values
last_break = 0                  #Defined how previous the car applied breaks
last_focus = 0                  #Defines how previous the car went forward in focus
left = 0                        #Buffer/Threshold for turning the car left
right = 0                       #Buffer/Threshold for turning the car right
no_straight = 0                 #Buffer/Threshold for steering the car straight
direction_state = 0             #Defines the current direction of the car

"""
Direction State
0 -> Straight
1 -> Left
2 -> Right
"""

print("Program start")

start = time.time()

#First fill the EEG data with 200 samples
while True:
    if len(eeg_data) == 100:
        break
    if serialInst.in_waiting:
        try:
            #Collecting EEG data
            bytes = serialInst.read(2)
            received_value = int(bytes[0] + (bytes[1] << 8))
            eeg_data.append(received_value)

            #Collecting EyeDirection data
            dir_bytes = serialInst.read(2)
            received_value = int(dir_bytes[0] + (dir_bytes[1] << 8)) 
            direction_data.append(received_value)
        except Exception as e:
            print(e)

        endtime = time.time()

print(f"The length of EEG data {len(eeg_data)}")
print(f"The time to fill 100 samples {endtime-start}")

fft_result = np.fft.fft(eeg_data)
frequencies = np.fft.fftfreq(len(eeg_data), 1/fs)
magnitude = np.abs(fft_result)

counter = 0                 #Counter Declaration

while True:
    try:
        #Popping 10 samples from the list and adding new samples into it
        #print(f"*****{serialInst.in_waiting}*******")
        if serialInst.in_waiting > 40:
            print(counter)
            starttime = time.time()
            counter += 1
            eeg_data = eeg_data[10:]            #Pop 10 samples from EEg data   
            direction_data = []                 #Emptying data from Direction Data

            for y in range(10):
                #Capturing Live EEG Data
                bytes = serialInst.read(2)
                received_value = int(bytes[0] + (bytes[1] << 8))
                eeg_data.append(received_value)

                #Capturing Live Direction Data
                dir_bytes = serialInst.read(2)
                direction_value = int(dir_bytes[0] + (dir_bytes[1] << 8))
                direction_data.append(direction_value)
            
            #print(eeg_data)
            #print(direction_data)

            #Performing FFT and limiting to 8-13 Hz
            fft_result = np.fft.fft(eeg_data)
            frequencies = np.fft.fftfreq(len(eeg_data), 1/fs)
            magnitude = np.abs(fft_result)
            phase = np.angle(fft_result)
            #print(phase)
            #print(frequencies)
            #print(magnitude)

            endtime = time.time()

            """
            print(f"\n\n\nLength of EEG Data {len(eeg_data)}")
            print(f"Power of Low Alpha Waves {lowAlpha}")
            print(f"Time duration {endtime-starttime}")
            print(f"Iteration {counter}")

            print(f"Power of Low Alpha Waves {lowAlpha}")
            print(f"Phase of Low Alpha waves {lowAlphaPhase}")

            print(f"Power of High Alpha Waves {highAlpha}")
            print(f"Phase of High Alpha waves {highAlphaPhase}")

            print(f"Power of Low Beta Waves {lowBeta}")
            print(f"Phase of Low Beta waves {lowBetaPhase}")

            print(f"Power of High Beta Waves {highBeta}")
            print(f"Phase of High Beta waves {highBetaPhase}")

            print(f"Power of Low Gamma Waves {lowGamma}")
            print(f"Phase of Low Gamma waves {lowGammaPhase}")

            print(f"Power of High Gamma Waves {highGamma}")
            print(f"Phase of High Gamma waves {highGammaPhase}")

            print(f"Time duration {endtime-starttime}")
            print(f"Iteration {counter}")
            """

            #Start predicting the status of eyes
            if counter > buffer_period:
                #Low alpha hertz frequencies
                mask = (frequencies >= 8) & (frequencies <= 9)
                filtered_low_alpha_results = fft_result[mask]
                phase = np.angle(filtered_low_alpha_results)
                #Averaging both the values of low alpha waves
                magnitude1 = np.abs(filtered_low_alpha_results)
                lowAlpha = np.mean(magnitude1)
                lowAlphaPhase = np.mean(phase)
                prev_alpha.append(lowAlpha)

                #High Gamma hertz frequencies
                mask = (frequencies >= 31) & (frequencies <= 49)
                filtered_high_gamma_results = fft_result[mask]
                phase = np.angle(filtered_high_gamma_results)
                #Averaging both the values of low alpha waves
                magnitude6 = np.abs(filtered_high_gamma_results)
                highGamma = np.mean(magnitude6)
                highGammaPhase = np.mean(phase)
                prev_gamma.append(highGamma)
                
                print(f"Alpha Values : {prev_alpha}")
                print(f"Gamma Values : {prev_gamma}")
                print(f"Direction Value : {direction_data}")

                #Collection all the parameter inputs for the model and loading it into a array
                if focus_state == 0:
                    if all(x > 950 for x in prev_gamma) == True:
                        if last_break > 20:
                            focus_state = 1
                            last_focus = 0
                            print("Data sent Start Focusing")
                            serialRemote.write('F\n'.encode())
                else:
                    if all(x > 750 for x in prev_alpha) == True:
                        if focus_state == 1 and last_focus > 20:
                            focus_state = 0
                            last_break = 0
                            print("Data Stopped")
                            serialRemote.write('S\n'.encode())
                
                last_break += 1
                last_focus += 1

                print(f"Last Break {last_break}")
                print(f"Last Focus {last_focus}")
                print(f"FOCUS_STATE {focus_state}")

                #Always maintain the window of previous inputs to be considered for output
                if len(prev_alpha) == 7:
                    prev_alpha.pop(0)
                if len(prev_gamma) == 5:
                    prev_gamma.pop(0)

                #Choosing Direction to steer [Consider only 5 values for faster execution]
                for dir_val in direction_data:
                    if dir_val > 400 and dir_val < 750:
                        if direction_state != 0:
                            no_straight += 1
                            if no_straight > 10:    
                                print("SSSSSSSSSSSSSSSSSSSSSSSS")
                                left = 0
                                right = 0
                                no_straight = 0
                                direction_state = 0

                    elif dir_val < 400:
                        if direction_state == 0:
                            left += 1
                            if left > 10:
                                print("LLLLLLLLLLLLLLLLLLLLLLLLL")
                                serialRemote.write('L\n'.encode())
                                left = 0
                                right = 0
                                no_straight = 0
                                direction_state = 1

                    elif dir_val > 750:
                        if direction_state == 0:
                            right += 1
                            if right > 10:
                                print("RRRRRRRRRRRRRRRRRRRRRRRRRRR")
                                serialRemote.write('R\n'.encode())
                                left = 0
                                right = 0
                                no_straight = 0
                                direction_state = 2
                
                print(f"Direction State ", direction_state)

    except Exception as e:
        print(e)
        break

print("The Program has been terminated!")