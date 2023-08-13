""" A function used to graph acceleration from a cleaned sheep data text file, using numpy and matplotlib in python.
"""

import matplotlib.pyplot as plt
import numpy as np

def acceleration_grapher(filename):
    'Returns an acceleration line graph object, given a cleaned file of sheep accelerometer data'
    acceleration_y_axis = np.array([])
    with open(filename) as file:
        lines = file.readlines()
        previous_acceleration = lines[0]
        for line in lines:
            if line[:3] != [0,0,0]:
                acceleration_y_axis = np.append(acceleration_y_axis, euclidean_distance(previous_acceleration, line))
                previous_acceleration = line
    time_x_axis = np.arange(np.size(acceleration_y_axis))
    plt.plot(time_x_axis, acceleration_y_axis)
    plt.title(f"Acceleration for {filename}")
    plt.xlabel("Time")
    plt.ylabel("Acceleration")
    plt.show(c = 'hotpink')
    return plt

def euclidean_distance(coordinates_1, coordinates_2)
    '''Returns the distance between two lists of coordinates, or -1 if the coordinates are not the same dimensions'''
    # Checks if coordinates have the same dimensions, returns -1 otherwise
    if len(coordinates_1) != len(coordinates_2):
        return -1
    # Checks for coordinates in one, two or three dimensions
    if 0 < len(coordinates_1) <= 3:
        distance = 0
        for point_1, point_2 in coordinates_1, coordinates_2:
            distance += (point_1 - point_2) ** 2
        return math.sqrt(distance)
    return -1
