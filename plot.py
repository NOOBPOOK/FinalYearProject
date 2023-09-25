import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Number of data points to display
display_points = 100

# Create a circular buffer to store the data
x_data = np.arange(display_points)
y_data = np.zeros(display_points)

# Create a figure and axis for the plot
fig, ax = plt.subplots()
line, = ax.plot(x_data, y_data)

# Function to update the plot
def update(frame):
    global y_data
    # Shift the existing data to the left and append new data at the end
    y_data[:-1] = y_data[1:]
    y_data[-1] = np.random.rand()  # Replace this with your data source
    
    # Update the plot data
    line.set_ydata(y_data)
    
    return line,

# Create a FuncAnimation instance to update the plot
ani = FuncAnimation(fig, update, blit=True, interval=100)

# Display the plot
plt.show()
