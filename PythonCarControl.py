import serial

serialRemote = serial.Serial(port="COM7", baudrate=115200)

while True:
    try:
        n = input("Please enter your direction")
        if n == 'W':
            print("Going Forward")
            serialRemote.write('F\n'.encode())
        elif n == 'S':
            print("Going Backward")
            serialRemote.write('B\n'.encode())
        elif n == 'C':
            print("Stop All")
            serialRemote.write('S\n'.encode())
    except:
        break

print("Program has been terminated")