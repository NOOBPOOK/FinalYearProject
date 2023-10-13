import serial

serialinst = serial.Serial("COM4", baudrate=500000)

while True:
    dir = int(input("Enter your direction here >> "))

    #Controlling Signals

    #Forward
    if dir == 0:
        serialinst.write('f'.encode())

    #Back
    if dir == 1:
        serialinst.write('b'.encode())

    #Left
    if dir == 2:
        serialinst.write('l'.encode())

    #Right
    if dir == 3:
        serialinst.write('r'.encode())

    #Clear all steering options
    if dir == 4:
        serialinst.write('n'.encode())

    #Stop all operations on the car
    if dir == 5:
        serialinst.write('s'.encode())