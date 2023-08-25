""" A function used to graph acceleration from a file of sheep accelerometer data, using numpy and matplotlib in python.
Assumptions: accelerometer records data at 25Hz, files are formatted as a line of timestamps and 25 lines of accelerometer 
data after each timestamp.
"""

import matplotlib.pyplot as plt
import numpy as np
import math

FREQUENCY = 25
# from scipy import constants
# GRAVITY = constants.g
GRAVITY   = 9.80665

def int_list(data):
    '''Converts elements of a list to type int'''
    for i in range(len(data)):
        data[i] = int(data[i])

def float_list(data):
    'Converts elements of a list to type float'
    for i in range(len(data)):
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

def extract_timestamp(times):
    '''Returns a numpy array of seconds and milliseconds from a timestamp starting with *.'''
    times[0] = times[0].strip('*')
    return np.array([times[0], times[1]])

def timestamp_to_seconds(times):
    '''Returns time in milliseconds, given a numpy array of seconds and milliseconds'''
    return 1000 * times[0] + times[1]

def acceleration_grapher(filename, header = False, calibrate_x = [-1.0,1.0], calibrate_y = [-1.0,1.0], calibrate_z = [-1.0,1.0]):
    """Returns an acceleration line graph pyplot object, given a file of sheep accelerometer data
    
    @param: calibrate_x a list of size 2 with a calibration lower bound and upper bound 
    @param: calibrate_y a list of size 2 with a calibration lower bound and upper bound 
    @param: calibrate_z a list of size 2 with a calibration lower bound and upper bound 
    @return: a pyplot object containing the acceleration line graph
    """
    x_acceleration   = np.array([0])
    y_acceleration   = np.array([0])
    z_acceleration   = np.array([0])
    time_x_axis = np.array([0])
    with open(filename) as file:
        lines = file.readlines()
        if not header:
            previous_timestamp = extract_timestamp(lines[0])
        else:
            previous_timestamp = extract_timestamp(lines[1])
        initial_timestamp = previous_timestamp
        for line in lines:
            # Checks for timestamp which starts with *
            if line.startswith('*'):
                timestamp = extract_timestamp(line)
                if timestamp != initial_timestamp:
                    extend_x_axis = np.linspace(timestamp_to_seconds(previous_timestamp), (timestamp_to_seconds(timestamp), FREQUENCY - zero_line_count))
                    time_x_axis = np.append(time_x_axis, np.delete(extend_x_axis, 0))
                zero_line_count = 0
            # Lines that do not start with * is accelerometer data
            if not line.startswith('*'):
                if line[:3] == [0,0,0]:
                    zero_line_count += 1
                acceleration = line[:3].strip().split(',')
                float_list(acceleration) 
                x_acceleration   = np.append(acceleration[0])
                y_acceleration   = np.append(acceleration[1])
                z_acceleration   = np.append(acceleration[2])
    extend_x_axis = np.linspace(timestamp_to_seconds(timestamp), timestamp_to_seconds(timestamp) + 1, FREQUENCY - zero_line_count)
    time_x_axis = np.append(time_x_axis, np.delete(extend_x_axis, 0))
    # Calibrates x,y,z accelerometer units into gravity units
    x_acceleration = (2 * x_acceleration - calibrate_x[0] - calibrate_x[1]) / (calibrate_x[1] - calibrate_x[0])
    y_acceleration = (2 * y_acceleration - calibrate_y[0] - calibrate_y[1]) / (calibrate_y[1] - calibrate_y[0])
    z_acceleration = (2 * z_acceleration - calibrate_z[0] - calibrate_z[1]) / -(calibrate_z[1] - calibrate_z[0])
    net_acceleration = np.sqrt(x_acceleration ** 2 + y_acceleration ** 2 + z_acceleration ** 2)
    plt.plot(time_x_axis, net_acceleration)
    plt.title(f"Acceleration for {filename}")
    plt.xlabel("Timestamp (s)")
    plt.ylabel("Acceleration (g)")
    # Y-axis label for uncalibrated data
    if calibrate_x == [-1.0,1.0] or calibrate_y == [-1.0,1.0] or calibrate_z == [-1.0,1.0]:
        plt.ylabel("Acceleration (units/s^2)")
    plt.show()
    return plt

acceleration_grapher('resources/file007.txt')