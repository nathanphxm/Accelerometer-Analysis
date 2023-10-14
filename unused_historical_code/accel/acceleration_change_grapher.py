""" A function used to graph change in acceleration from a file of sheep accelerometer data, using numpy and matplotlib in 
python.
Assumptions: accelerometer records data at 25Hz, files are formatted as a line of timestamps and 25 lines of accelerometer 
data after each timestamp, timestamp is formatted as (*seconds, milliseconds).
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math

FREQUENCY = 25

def int_list(data):
    '''Converts elements of a list to type int'''
    for i in range(len(data)):
        data[i] = int(data[i])

def float_list(data):
    '''Converts elements of a list to type float'''
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

def acceleration_change_grapher(filename, header = False):
    '''Returns an acceleration change line graph pyplot object, given a file of sheep accelerometer data'''
    acceleration_y_axis = np.array([0])
    time_x_axis = np.array([0])
    with open(filename) as file:
        lines = file.readlines()
        if not header:
            previous_timestamp    = extract_timestamp(lines[0])
            previous_acceleration = lines[1].strip().split(',')
        else:
            previous_timestamp    = extract_timestamp(lines[1])
            previous_acceleration = lines[2].strip().split(',')
        initial_timestamp = previous_timestamp
        float_list(previous_acceleration)
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
                acceleration_y_axis = np.append(acceleration_y_axis, euclidean_distance(previous_acceleration, acceleration))
                previous_acceleration = acceleration
    extend_x_axis = np.linspace(timestamp_to_seconds(timestamp), timestamp_to_seconds(timestamp) + 1, FREQUENCY - zero_line_count)
    time_x_axis = np.append(time_x_axis, np.delete(extend_x_axis, 0))
    plt.plot(time_x_axis, acceleration_y_axis)
    plt.title(f"Change in acceleration for {filename}")
    plt.xlabel("Timestamp (s)")
    plt.ylabel("Acceleration (units/s^2)")
    plt.show()
    return plt

acceleration_change_grapher('resources/file007.txt')