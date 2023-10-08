"""
Program detects if eyes are closed or not by studying the alpha waves 8-13 Hz
Electrode placements: Black(-in) and Red(+)on forehead, Yellow(Ref) on ear lobe
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

#Sampling rate (that is 200 samples per second)
fs = 100 
frequencies = None
fft_result = None

"""
Threshold value. More the value more pressure to get eyes closed so that the movement can be detected.
More value more pressure and vice versa
"""
threshold_freq = 700

#Creating the CSV file which will conatin values
file_path = "C:/Users/hp/Documents/GitHub/FinalYearProject/eeg_data/BlackFrontRedBack/EventEEG/focuscar5.csv"
eeg_file = open(file_path, mode = 'w')
writer = csv.writer(eeg_file, lineterminator="\n")
writer.writerow(['Timestamp','Iterations','LowAlpha','LowAlphaPhase','HighAlpha','HighAlphaPhase','LowBeta','LowBetaPhase','HighBeta','HighBetaPhase','LowGamma','LowGammePhase','HighGamma','HighGammaPhase','EyeStatus'])

"""
Table Order
Timestamp, Iterations, LowAlpha, LowAlphaPhase, HighAlpha, HighAlphaPhase, LowBeta, LowBetaPhase, HighBeta, HighBetaPhase, LowGamma, LowGammaPhase, HighGamma, HighGammaPhase, EyeStatus
"""

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
    try:
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
            phase = np.angle(fft_result)
            #print(phase)
            #print(frequencies)
            #print(magnitude)



            #Low alpha hertz frequencies
            mask = (frequencies >= 8) & (frequencies <= 9)
            filtered_low_alpha_results = fft_result[mask]
            phase = np.angle(filtered_low_alpha_results)
            #Averaging both the values of low alpha waves
            magnitude1 = np.abs(filtered_low_alpha_results)
            lowAlpha = np.mean(magnitude1)
            lowAlphaPhase = np.mean(phase)

            #High alpha hertz frequencies
            mask = (frequencies >= 10) & (frequencies <= 12)
            filtered_high_alpha_results = fft_result[mask]
            phase = np.angle(filtered_high_alpha_results)
            #Averaging both the values of high alpha waves
            magnitude2 = np.abs(filtered_high_alpha_results)
            highAlpha = np.mean(magnitude2)
            highAlphaPhase = np.mean(phase)

            #Low Beta hertz frequencies
            mask = (frequencies >= 13) & (frequencies <= 17)
            filtered_low_beta_results = fft_result[mask]
            phase = np.angle(filtered_low_beta_results)
            #Averaging both the values of low beta waves
            magnitude3 = np.abs(filtered_low_beta_results)
            lowBeta = np.mean(magnitude3)
            lowBetaPhase = np.mean(phase)

            #High Beta hertz frequencies
            mask = (frequencies >= 18) & (frequencies <= 30)
            filtered_high_beta_results = fft_result[mask]
            phase = np.angle(filtered_high_beta_results)
            #Averaging both the values of low beta waves
            magnitude4 = np.abs(filtered_high_beta_results)
            highBeta = np.mean(magnitude4)
            highBetaPhase = np.mean(phase)

            #Low Gamma hertz frequencies
            mask = (frequencies >= 30) & (frequencies <= 40)
            filtered_low_gamma_results = fft_result[mask]
            phase = np.angle(filtered_low_gamma_results)
            #Averaging both the values of low alpha waves
            magnitude5 = np.abs(filtered_low_gamma_results)
            lowGamma = np.mean(magnitude5)
            lowGammaPhase = np.mean(phase)

            #High Gamma hertz frequencies
            mask = (frequencies >= 31) & (frequencies <= 49)
            filtered_high_gamma_results = fft_result[mask]
            phase = np.angle(filtered_high_gamma_results)
            #Averaging both the values of low alpha waves
            magnitude6 = np.abs(filtered_high_gamma_results)
            highGamma = np.mean(magnitude6)
            highGammaPhase = np.mean(phase)

            endtime = time.time()

            """
            print(f"\n\n\nLength of EEG Data {len(eeg_data)}")
            print(f"Power of Low Alpha Waves {lowAlpha}")
            print(f"Time duration {endtime-starttime}")
            print(f"Iteration {counter}")
            """

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
            Table Order
            Timestamp, Iterations, LowAlpha, LowAlphaPhase, HighAlpha, HighAlphaPhase, LowBeta, 
            LowBetaPhase, HighBeta, HighBetaPhase, LowGamma, LowGammaPhase, HighGamma, HighGammaPhase, EyeStatus
            """

            #Inserting Values into CSV Sheet
            if counter > 500:
                writer.writerow([(endtime-start),counter,
                                 lowAlpha,lowAlphaPhase,highAlpha,highAlphaPhase,
                                 lowBeta,lowBetaPhase,highBeta,highBetaPhase,
                                 lowGamma,lowGammaPhase,highGamma,highGammaPhase,
                                 ledState])

            light.append(lowAlpha)

            #print(f"Mean Values{light}")

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

            print(f"Eyes Status :   {ledState}\n")

        else:
            pass
    except:
        break

print("The Program has been terminated!")
eeg_file.close()






        


