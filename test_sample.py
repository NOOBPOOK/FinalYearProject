import serial
import matplotlib.pyplot as plt

#Creating an instance object 
serialInst = serial.Serial(timeout=0.020)

#Setting up the connection
serialInst.port = "COM3"
serialInst.baudrate = 9600
serialInst.open()

import time
import numpy as np

# Get the current time in seconds

#Sampling rate (that is 200 samples per second)
fs = 200 
frequencies = None
fft_result = None
limit_val = [[]]

#Counter
g = 0

#Intializing Timer from start
begin_time = time.time()
end_time = None

#Function to get power for specific waves
def get_power(low_limit, high_limit):
    """
    Indicating power for Waves based on Parameters
    Occurence during sleep
    """
    mask = (frequencies >= low_limit) & (frequencies <=high_limit)
    filtered_delta_frequenices = fft_result[mask]

    magnitude = np.abs(filtered_delta_frequenices)
    mean = np.mean(magnitude)

    return round(mean,2)

# Continuous loop to process the EEG Data
while True:
    try:
        g += 1
        
        start_time = time.time()
        eeg_data = []
        i = 0
        while i < fs:
            if serialInst.in_waiting:
                i += 1
                integer_value = serialInst.readline().decode("utf-8").rstrip("\r\n")
                if integer_value == '1025':
                    print("\n\nThe below samples were collected in 1 second")
                    break
                try:
                    eeg_data.append(int(integer_value))
                except:
                    pass

        fft_result = np.fft.fft(eeg_data)
        frequencies = np.fft.fftfreq(len(eeg_data), 1/fs)

        """
        #Calculate power for Delta Waves
        power = get_power(1,3)
        print(f"Delta waves (1-3Hz) : {power}")

        #Calculate power for Theta waves
        power = get_power(4,7)
        print(f"Theta waves (4-7Hz) : {power}")
        """

        #Calculate power for Low Alpha Waves
        power = get_power(8,9)
        print(f"Low Alpha waves (8-9Hz) : {power}")

        #Calculate power for High Alpha waves
        power = get_power(10,12)
        print(f"High Alpha waves (10-12Hz) : {power}")
        
        #Calculate power for Low Beta waves
        power = get_power(13,17)
        print(f"Low Beta waves (13-17Hz) : {power}")

        #Calculate power for High Beta Waves
        power = get_power(18,30)
        print(f"High Beta waves (18-30Hz) : {power}")

        #Calculate power for Low Gamma Waves
        power = get_power(31,40)
        print(f"Low Gamma waves (31-40Hz) : {power}")

        #Calculate power for High Gamma Waves
        power = get_power(41,50)
        print(f"High Gamma waves (41-50Hz) : {power}")

        end_time = time.time()
        print(f"Time taken in seconds to complete this iteration {end_time - start_time}")

    except:
        break


print(f"\n\n*********************************\nTotal time taken in seconds {end_time - begin_time}")
print(f"Total iterations : {g}")


