"""
Program takes real time inputs from the user and gives out predictions without need of ML model
Electrode placements: Black(-in) and Red(+)on forehead, Yellow(Ref) on ear lobe
"""

import serial
import matplotlib.pyplot as plt
import time
import numpy as np 
import csv
import joblib

#Creating an instance object 
serialInst = serial.Serial("COM5", 500000)

#Creating a remote for controlling the car
serialRemote = serial.Serial("COM4", 115200)

#Sampling rate (that is 200 samples per second)
fs = 100 
frequencies = None
fft_result = None
prev_val_counter = 5 #Defines the no. of past inputs to give for prediction
buffer_period = 100 #Time for buffer to start the process
eeg_data = []
focus_state = 0 #0 stands for no focus & 1 stands for full focus
prev_alpha = []
prev_gamma = []
last_break = 0
last_focus = 0

print("Program start")

start = time.time()

#First fill the EEG data with 200 samples
while True:
    if len(eeg_data) == 100:
        break
    if serialInst.in_waiting:
        try:
            bytes = serialInst.read(2)
            received_value = int(bytes[0] + (bytes[1] << 8))
            eeg_data.append(received_value)
        except Exception as e:
            print(e)

        endtime = time.time()

print(f"The length of EEG data {len(eeg_data)}")
print(f"The time to fill 100 samples {endtime-start}")

fft_result = np.fft.fft(eeg_data)
frequencies = np.fft.fftfreq(len(eeg_data), 1/fs)
magnitude = np.abs(fft_result)

#Counter Declaration
counter = 0

while True:
    try:
        #Popping 10 samples from the list and adding new samples into it
        #print(f"*****{serialInst.in_waiting}*******")
        if serialInst.in_waiting > 20:
            print(counter)
            starttime = time.time()
            counter += 1
            eeg_data = eeg_data[10:]
            for y in range(10):
                bytes = serialInst.read(2)
                received_value = int(bytes[0] + (bytes[1] << 8))
                eeg_data.append(received_value)
            
            #print(eeg_data)


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
                
                print(prev_alpha)
                print(prev_gamma)

                #Collection all the parameter inputs for the model and loading it into a array
                if focus_state == 0:
                    if all(x > 950 for x in prev_gamma) == True:
                        if last_break > 20:
                            focus_state = 1
                            last_focus = 0
                            print("Data sent Start Focusing")
                            serialRemote.write('F'.encode())
                else:
                    if all(x > 750 for x in prev_alpha) == True:
                        if focus_state == 1 and last_focus > 20:
                            focus_state = 0
                            last_break = 0
                            print("Data Stopped")
                            serialRemote.write('S'.encode())
                
                last_break += 1
                last_focus += 1
                print(f"Last Break {last_break}")
                print(f"Last Focus {last_focus}")
                print(f"FOCUS_STATE {focus_state}")

                if len(prev_alpha) == 10:
                    prev_alpha.pop(0)
                if len(prev_gamma) == 5:
                    prev_gamma.pop(0)

    except Exception as e:
        print(e)
        break

print("The Program has been terminated!")






        



