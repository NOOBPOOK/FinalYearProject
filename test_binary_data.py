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

while True:
    if serialInst.in_waiting:
        bytes = serialInst.read(2)
        vol = int(bytes[0] + (bytes[1] << 8))
        print(vol)