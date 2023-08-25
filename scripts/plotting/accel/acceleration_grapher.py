""" A function used to graph acceleration from a set of cleaned sheep accelerometer data, 
using numpy and matplotlib in python.
Assumptions: accelerometer outputs data at 25Hz, a line of zeros is outputed if the accelerometer runs at less than 25Hz, 
data is formatted as a list of lists containing [Timestamp, Index, X-acceleration, Y-acceleration, Z-acceleration]
"""

import matplotlib.pyplot as plt
import numpy as np
import math

# from scipy import constants
# print(constants.g)
GRAVITY   = 9.80665
# List indexes/indices for cleaned sheep accelerometer data
TIMESTAMP = 0
INDEX     = 1
X_ACCEL   = 2
Y_ACCEL   = 3
Z_ACCEL   = 4

def acceleration_grapher(data, calibrate_x = [-1.0,1.0], calibrate_y = [-1.0,1.0], calibrate_z = [-1.0,1.0], grav = True):
    """Returns an acceleration line graph pyplot object, given a file of sheep accelerometer data
    
    @param: data, a list of cleaned sheep accelerometer data which are lists 
    containing [Timestamp, Index, X-acceleration, Y-acceleration, Z-acceleration]
    @param: calibrate_x, a list of size 2 with a calibration lower bound and upper bound 
    @param: calibrate_y, a list of size 2 with a calibration lower bound and upper bound 
    @param: calibrate_z, a list of size 2 with a calibration lower bound and upper bound 
    @return: a pyplot object containing the acceleration line graph
    """
    x_acceleration   = np.array([0])
    y_acceleration   = np.array([0])
    z_acceleration   = np.array([0])
    net_acceleration = np.array([0])
    time_x_axis      = np.array([0])
    for line in data:
        # Checks for a line of zeros
        if not (line[X_ACCEL] == 0 and line[Y_ACCEL] == 0 and line[Z_ACCEL] == 0):
            time_x_axis    = np.append(time_x_axis, line[TIMESTAMP])
            x_acceleration = np.append(x_acceleration, float(line[X_ACCEL]))
            y_acceleration = np.append(y_acceleration, float(line[Y_ACCEL]))
            z_acceleration = np.append(z_acceleration, float(line[Z_ACCEL]))
    # Calibrates x,y,z accelerometer units into gravity units
    x_acceleration = (2 * x_acceleration - calibrate_x[0] - calibrate_x[1]) / (calibrate_x[1] - calibrate_x[0])
    y_acceleration = (2 * y_acceleration - calibrate_y[0] - calibrate_y[1]) / (calibrate_y[1] - calibrate_y[0])
    z_acceleration = (2 * z_acceleration - calibrate_z[0] - calibrate_z[1]) / -(calibrate_z[1] - calibrate_z[0])
    net_acceleration = np.sqrt(x_acceleration ** 2 + y_acceleration ** 2 + z_acceleration ** 2)
    plt.plot(time_x_axis, net_acceleration)
    plt.title(f"Acceleration for {data}")
    plt.xlabel("Timestamp")
    plt.ylabel("Acceleration (g)")
    # Y-axis label for uncalibrated data
    if calibrate_x == [-1.0,1.0] or calibrate_y == [-1.0,1.0] or calibrate_z == [-1.0,1.0]:
        plt.ylabel("Acceleration (units/s^2)")
    # Y-axis label for units in m/s^2
    if not grav:
        net_acceleration = GRAVITY * net_acceleration
        plt.ylabel("Acceleration (m/s^2)")
    plt.show()
    return plt
