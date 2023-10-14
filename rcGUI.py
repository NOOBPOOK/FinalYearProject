import tkinter as tk
import serial

dir = 0

serialinst = serial.Serial("COM4", baudrate=500000)

actions = set()  # Set to store the currently pressed arrow keys


def print_statement():
    global dir
    if 'Up' in actions and 'Left' in actions:
        serialinst.write('f'.encode())
        dir = 1
        serialinst.write('l'.encode())
        print("Forward + Left")

    elif 'Up' in actions and 'Right' in actions:
        serialinst.write('f'.encode())
        dir = 2
        serialinst.write('r'.encode())
        print("Forward + Right")

    elif 'Down' in actions and 'Right' in actions:
        serialinst.write('b'.encode())
        dir = 2
        serialinst.write('r'.encode())
        print("Backward + Right")

    elif 'Down' in actions and 'Left' in actions:
        serialinst.write('b'.encode())
        dir  = 1
        serialinst.write('l'.encode())
        print("Backward + Left")

    elif 'Down' in actions:
        serialinst.write('b'.encode())
        if dir != 0:
            serialinst.write('n'.encode())
            dir = 0
        print("Backward")

    elif 'Left' in actions:
        serialinst.write('l'.encode())
        print("Left")

    elif 'Right' in actions:
        serialinst.write('r'.encode())
        print("Right")

    elif 'Up' in actions:
        serialinst.write('f'.encode())
        if dir != 0:
            serialinst.write('n'.encode())
            dir = 0
        print("Forward")

def key_press(event):
    actions.add(event.keysym)
    print_statement()

def key_release(event):
    actions.discard(event.keysym)
    print_statement()

# Create the main application window
root = tk.Tk()
root.title("Button Actions")

# Bind arrow key presses and releases
root.bind("<Key>", key_press)
root.bind("<KeyRelease>", key_release)

# Run the GUI event loop
root.mainloop()
