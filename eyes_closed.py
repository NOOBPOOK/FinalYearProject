"""
Program detects if eyes are closed or not by studying the alpha waves 8-13 Hz
Electrode placements: Black(-in) on forehead, Yellow(Ref) on ear lobe, Red(in+) on back
"""

import serial
import matplotlib.pyplot as plt
import time
import numpy as np

#Creating an instance object 
serialInst = serial.Serial()

#Setting up the connection
serialInst.port = "COM3"
serialInst.baudrate = 500000
serialInst.open()

#Sampling rate (that is 200 samples per second)
fs = 100 
frequencies = None
fft_result = None

"""
Threshold value. More the value more pressure to get eyes closed so that the movement can be detected.
More value more pressure and vice versa
"""

threshold_freq = 550


light = []

eeg_data = []
print("Program start")
print(f"OOOOOO stands for Eyes Opened")
print(f"XXXXXX stands for Eyes Closed")
start = time.time()
serialInst.write("0".encode())
ledState = "OOOOOO"

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
    #Popping 10 samples from the list and adding new samples into it
    #print(f"*****{serialInst.in_waiting}*******")
    if serialInst.in_waiting > 20:
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
        #print(frequencies)
        #print(magnitude)

        #Low alpha hertz frequencies
        mask = (frequencies >= 8) & (frequencies <= 12)
        filtered_low_alpha_results = fft_result[mask]

        #Averaging both the values of low alpha waves
        magnitude = np.abs(filtered_low_alpha_results)
        mean1 = np.mean(magnitude)

        endtime = time.time()

        """
        print(f"\n\n\nLength of EEG Data {len(eeg_data)}")
        print(f"Power of Low Alpha Waves {mean1}")
        print(f"Time duration {endtime-starttime}")
        print(f"Iteration {counter}")
        """

        light.append(mean1)

        print(f"Mean Values{light}")

        if len(light) > 5:
            light.pop(0)
        
        if all(x > threshold_freq  for x in light):
            if ledState != "XXXXXX":
                #serialInst.write("1".encode())
                ledState = "XXXXXX"

        else:
            if ledState == "XXXXXX":
                #serialInst.write("0".encode())
                ledState = "OOOOOO"

        print(f"{ledState}\n")

    else:
        pass






        


