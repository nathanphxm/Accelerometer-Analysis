import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

with open('sample_data/file007_clean.txt', 'r') as file:
    lines = file.readlines()

times, xs, ys, zs, iter = [], [], [], [], []
magnitude = []
for_mean = []
pitch = []
roll = []

for line in lines:
    timestamp, iteration, x, y, z = map(int, line.split(","))
    # Convert timestamp and iteration into continuous time
    time = timestamp + (iteration - 1) / 25.0  # Subtracting 1 to start the iteration from 0
    times.append(time)
    xs.append(x)
    ys.append(y)
    zs.append(z)
    magnitude.append((x**2+y**2+z**2)**0.5)
    iter.append(iteration)

# Create vectors from the accelerometer readings
accel_x_vector = np.array(xs)
accel_y_vector = np.array(ys)
accel_z_vector = np.array(zs)

# Calculate pitch and roll angles
pitch = np.arctan2(accel_x_vector, np.sqrt(accel_y_vector**2 + accel_z_vector**2))
roll = np.arctan2(-accel_y_vector, accel_z_vector)

# Convert radians to degrees
pitch_deg = np.degrees(pitch)
roll_deg = np.degrees(roll)

print("Pitch angle (degrees):", pitch_deg[:10])
print("Roll angle (degrees):", roll_deg[:10])
# Convert timestamps to datetime objects
datetimes = [datetime.fromtimestamp(ts) for ts in times]


