import serial
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Open a serial connection to Arduino
ser = serial.Serial('COM3', 9600)  # Change 'COM3' to the correct port

# Initialize data buffer
buffer_size = 512
data_buffer = []
sampleRate = 1000

# Define the frequency range of interest
min_freq = 4  # Minimum frequency in Hz
max_freq = 40  # Maximum frequency in Hz

# Infinite loop for real-time data processing
while True:
    try:
        # Read data from Arduino
        raw_data = ser.readline().decode().strip()
        voltage = float(raw_data)
        
        # Add data to the buffer
        data_buffer.append(voltage)
        
        # Ensure the buffer does not exceed its size
        if len(data_buffer) > buffer_size:
            data_buffer.pop(0)
        
        # Perform FFT analysis
        if len(data_buffer) == buffer_size:
            data_array = np.array(data_buffer)
            fft_result = np.fft.fft(data_array)
            freqs = np.fft.fftfreq(len(data_array))
            
            # Calculate amplitude (magnitude of FFT)
            amplitude = np.abs(fft_result)
            
            # Find the peaks in the amplitude spectrum within the specified range
            peaks, _ = find_peaks(amplitude, height=0.1, threshold=(min_freq / sampleRate, max_freq / sampleRate))
            
            # Print frequencies and corresponding amplitudes of peaks
            for peak_idx in peaks:
                freq = freqs[peak_idx] * sampleRate
                amp = amplitude[peak_idx]
                print(f"Frequency: {freq} Hz, Amplitude: {amp}")
            
    except KeyboardInterrupt:
        ser.close()
        break

