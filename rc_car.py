import serial

serialinst = serial.Serial("COM3", baudrate=9600)

serialinst.open()

while True:
    dir = []
    dir = list(map(int, input("Enter your direction here >> ").split()))

    #Controlling Signals
    #Forward
    if 0 in dir:
        serialinst.write("0".encode())

    #Back
    if 1 in dir:
        serialinst.write("1".encode())

    #Left
    if 2 in dir:
        serialinst.write("2".encode())

    #Right
    if 3 in dir:
        serialinst.write("3".encode())

    if 5 in dir:
        serialinst.write("4".encode())