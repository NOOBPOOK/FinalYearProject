"""
Program detects if eyes are closed or not by studying the alpha waves 8-13 Hz
Electrode placements: Black(-in) and Red(+)on forehead, Yellow(Ref) on ear lobe
"""

import serial
import matplotlib.pyplot as plt
import time
import numpy as np
import joblib


#Creating an instance object 
serialInst = serial.Serial()

#Setting up the connection
serialInst.port = "COM5"
serialInst.baudrate = 500000
serialInst.open()

#Sampling rate (that is 200 samples per second)
fs = 100 
frequencies = None
fft_result = None
eeg_data = []
prev = [] #Store previous Average values for ML
loaded_m = joblib.load('Prev3ModelAvg.pkl') #Load the model in Computer


print("Program start")
print(f"OOOOOO stands for Eyes Opened")
print(f"XXXXXX stands for Eyes Closed")


start = time.time()
eyesState = 0

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
    eyeParam = []
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

            #Low alpha hertz frequencies
            mask = (frequencies >= 8) & (frequencies <= 9)
            filtered_low_alpha_results = fft_result[mask]
            phase = np.angle(filtered_low_alpha_results)
            #Averaging both the values of low alpha waves
            magnitude1 = np.abs(filtered_low_alpha_results)
            lowAlpha = np.mean(magnitude1)
            lowAlphaPhase = np.mean(phase)
            eyeParam.append(lowAlpha)
            eyeParam.append(lowAlphaPhase)

            #High alpha hertz frequencies
            mask = (frequencies >= 10) & (frequencies <= 12)
            filtered_high_alpha_results = fft_result[mask]
            phase = np.angle(filtered_high_alpha_results)
            #Averaging both the values of high alpha waves
            magnitude2 = np.abs(filtered_high_alpha_results)
            highAlpha = np.mean(magnitude2)
            highAlphaPhase = np.mean(phase)
            eyeParam.append(highAlpha)
            eyeParam.append(highAlphaPhase)

            #Low Beta hertz frequencies
            mask = (frequencies >= 13) & (frequencies <= 17)
            filtered_low_beta_results = fft_result[mask]
            phase = np.angle(filtered_low_beta_results)
            #Averaging both the values of low beta waves
            magnitude3 = np.abs(filtered_low_beta_results)
            lowBeta = np.mean(magnitude3)
            lowBetaPhase = np.mean(phase)
            eyeParam.append(lowBeta)
            eyeParam.append(lowBetaPhase)

            #High Beta hertz frequencies
            mask = (frequencies >= 18) & (frequencies <= 30)
            filtered_high_beta_results = fft_result[mask]
            phase = np.angle(filtered_high_beta_results)
            #Averaging both the values of low beta waves
            magnitude4 = np.abs(filtered_high_beta_results)
            highBeta = np.mean(magnitude4)
            highBetaPhase = np.mean(phase)
            eyeParam.append(highBeta)
            eyeParam.append(highBetaPhase)

            #Low Gamma hertz frequencies
            mask = (frequencies >= 30) & (frequencies <= 40)
            filtered_low_gamma_results = fft_result[mask]
            phase = np.angle(filtered_low_gamma_results)
            #Averaging both the values of low alpha waves
            magnitude5 = np.abs(filtered_low_gamma_results)
            lowGamma = np.mean(magnitude5)
            lowGammaPhase = np.mean(phase)
            eyeParam.append(lowGamma)
            eyeParam.append(lowGammaPhase)

            #High Gamma hertz frequencies
            mask = (frequencies >= 31) & (frequencies <= 49)
            filtered_high_gamma_results = fft_result[mask]
            phase = np.angle(filtered_high_gamma_results)
            #Averaging both the values of low alpha waves
            magnitude6 = np.abs(filtered_high_gamma_results)
            highGamma = np.mean(magnitude6)
            highGammaPhase = np.mean(phase)
            eyeParam.append(highGamma)
            eyeParam.append(highGammaPhase)

            eyeParam.append((lowAlpha+highAlpha)/2)
            eyeParam.append((lowBeta+highBeta)/2)
            eyeParam.append((lowGamma+highGamma)/2)

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
            if counter > 497 and counter < 501:
                prev.append((lowAlpha+highAlpha)/2)
                prev.append((lowBeta+highBeta)/2)
                prev.append((lowGamma+highGamma)/2) 

            #Start predicting the status of eyes
            if counter > 500:

                #Collection all the parameter inputs for the model and loading it into a array
                eyeParam.extend(prev)
                print(eyeParam)

                eyePrediction = loaded_m.predict([eyeParam])
                #print("Input value: ", eyeParam)
                print("Predicted value: ", eyePrediction)
                

                """
                EyesState 0 -> Normal (Eyes Opened)
                EyesState 1 -> Closed (Eyes Closed) 
                """

                if int(eyePrediction) == 0:
                    print(f"\n\n********** OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO *************\n\n")
                
                else:
                    print(f"\n\n********** Closed *************\n\n")

                if len(prev) == 9:
                    prev.pop(0)
                    prev.pop(0)
                    prev.pop(0)
                    prev.append((lowAlpha+highAlpha)/2)
                    prev.append((lowBeta+highBeta)/2)
                    prev.append((lowGamma+highGamma)/2) 

    except Exception as e:
        print(e)
        break

print("The Program has been terminated!")






        


