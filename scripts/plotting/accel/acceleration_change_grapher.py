""" A function used to graph change in acceleration from a file of sheep accelerometer data, using numpy and matplotlib in 
python.
Assumptions: accelerometer records data at 25Hz, files are formatted as a line of timestamps and 25 lines of accelerometer 
data after each timestamp, timestamp is formatted as (*seconds, milliseconds).
"""

import matplotlib.pyplot as plt
import numpy as np
import math

FREQUENCY = 25
# Indexes/Indices for cleaned sheep accelerometer data
TIMESTAMP = 0
INDEX     = 1
X_ACCEL   = 2
Y_ACCEL   = 3
Z_ACCEL   = 4

def float_list(data):
    '''Converts elements of a list to type float'''
    for i in len(data):
        data[i] = float(data[i])

def euclidean_distance(coordinates_1, coordinates_2):
    '''Returns the distance between two lists of coordinates, or -1 if the coordinates are not the same dimensions'''
    # Checks if coordinates have the same dimensions, returns -1 otherwise
    if len(coordinates_1) != len(coordinates_2):
        return -1
    # Checks for coordinates in one, two or three dimensions
    if 0 < len(coordinates_1) <= 3:
        distance = 0
        for i in range(len(coordinates_1)):
            distance += (coordinates_1[i] - coordinates_2[i]) ** 2
        return math.sqrt(distance)
    return -1

def acceleration_change_grapher(data):
    """Returns an acceleration change line graph pyplot object, given a file of sheep accelerometer data
    
    @param: data, a list of lists containing data formatted as [Timestamp, Index, X-acceleration, Y-acceleration, Z-acceleration]
    @return a pyplot object containing an acceleration change graph for the given data
    """
    acceleration_y_axis = np.array([])
    time_x_axis = np.array([])
    previous_acceleration = [line[0][X_ACCEL], line[0][Y_ACCEL], line[0][Z_ACCEL]]
    float_list(previous_acceleration)
    for line in data:
        time_x_axis = np.append(time_x_axis, line[TIMESTAMP])
        if not (line[X_ACCEL] == 0 and line[Y_ACCEL] == 0 and line[Z_ACCEL] == 0):
            acceleration = [line[X_ACCEL], line[Y_ACCEL], line[Z_ACCEL]]
            float_list(acceleration)
            acceleration_y_axis = np.append(acceleration_y_axis, euclidean_distance(previous_acceleration, acceleration))
            acceleration = previous_acceleration
    plt.plot(time_x_axis, acceleration_y_axis)
    plt.title(f"Change in acceleration for {data}")
    plt.xlabel("Timestamp")
    plt.ylabel("Acceleration (units/s^2)")
    plt.show()
    return plt
