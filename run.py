import joblib
import serial.tools.list_ports

#Listing down all the available ports
ports = serial.tools.list_ports.comports()
for i in ports:
    print(str(i))

#Creating an instance object 
serialInst = serial.Serial()

#Setting up the connection
serialInst.port = "COM3"
serialInst.baudrate = 9600

#Loading the already stored model
loaded_m = joblib.load('trained_model.pkl')

serialInst.open()
prev = ""

"""Reading data from the Adruino"""
while True:
    if serialInst.in_waiting:
        packet = serialInst.readline().decode("utf")
        try:    
            packet = float(packet.rstrip("\\r\\n"))
            packet = loaded_m.predict([[packet]])
        except Exception as e:
            print(e)
            continue
        if float(packet) < 2.5:
            if prev != "h":
                serialInst.write(bytes("1", 'utf-8'))
                prev = "h"
        else:
            if prev != "l":
                serialInst.write(bytes("0", 'utf-8'))
                prev = "l"
        


        