'''
A script to plot delta acceleration of each axis, as well as highlighting the activity level in 3 categories: low, medium, high
By inputting upper and lower threshold, the intensity of activity highlights can be adjusted.
Adding on to that, there's a function to pick hours of the day to specify the scope of analysis.
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from scipy.signal import find_peaks
import pandas as pd

with open('./paddock_data/green131_gps0459_file011_clean.txt', 'r') as file:
    lines = file.readlines()

times, xs, ys, zs, iter = [], [], [], [], []
magnitude = []
for_mean = []

# file reading
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


# Convert timestamps to datetime objects
datetimes = [datetime.fromtimestamp(ts) for ts in times]

# function to filter our specific hours of the day for analysis
def filter_hour(start_hour, end_hour):
    hour_indices = np.where((datetimes[0].hour <= start_hour) & (datetimes[0].hour >= end_hour))[0]
    xs = xs[hour_indices]
    ys = ys[hour_indices]
    xs = xs[hour_indices]
    magnitude = magnitude[hour_indices]
    iter = iter[hour_indices]
    return xs, ys, zs, magnitude, iter

# Define a function to classify activity, as well as putting the low and medium threshold
def classify_activity(values ,low_threshold, medium_threshold):
    categories = np.where(np.abs(values) < low_threshold, 1,
                           np.where(np.abs(values) < medium_threshold, 2, 3))
    return categories


#xs, ys, zs, magnitude, iter = filter_hour(11,12)

# difference of acceleration and magnitude
diff_x = np.diff(xs)
diff_y = np.diff(ys)
diff_z = np.diff(zs)
diff_mag = np.diff(magnitude)
forplot_datetime = datetimes[1:]


# Classify activity for diff_x, diff_y, diff_z, and diff_mag
# category_x = classify_activity(diff_x)
# category_y = classify_activity(diff_y)
# category_z = classify_activity(diff_z)
# category_mag = classify_activity(diff_mag)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6, 6))
timestamps = [mdates.date2num(dt) for dt in forplot_datetime]

ax1.plot(timestamps, diff_x, color="b")

# Classify activity for diff_x
category_x = classify_activity(diff_x, 100, 300)

# Create a mask for low, medium, and high activity
low_mask = category_x == 1
medium_mask = category_x == 2
high_mask = category_x == 3

# Fill between the data points based on activity
y1 = min(diff_x)
y2 = max(diff_x)

# highlighting the activity by coloring the graph
ax1.fill_between(timestamps,y1,y2, where=high_mask, color="red", alpha=0.3)
ax1.fill_between(timestamps,y1,y2, where=medium_mask, color="yellow", alpha=0.3)
ax1.fill_between(timestamps,y1,y2, where=low_mask, color="green", alpha=0.3)

ax1.set_title('Changes in x-axis reading over time')
ax1.set_ylabel('\u0394 X')
ax1.xaxis.set_major_locator(mdates.MinuteLocator(interval=60))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax1.tick_params(axis='x', rotation=45)  # Rotate x-axis labels by 90 degrees

# Plot changes in y-axis reading over time
ax2.plot(forplot_datetime, diff_y, color="b")

# Classify activity for diff_x
category_y = classify_activity(diff_y, 100, 300)

# Create a mask for low, medium, and high activity
low_mask = category_y == 1
medium_mask = category_y == 2
high_mask = category_y == 3

# Fill between the data points based on activity
y1 = min(diff_y)
y2 = max(diff_y)

# highlighting the activity by coloring the graph
ax2.fill_between(timestamps,y1,y2, where=high_mask, color="red", alpha=0.3)
ax2.fill_between(timestamps,y1,y2, where=medium_mask, color="yellow", alpha=0.3)
ax2.fill_between(timestamps,y1,y2, where=low_mask, color="green", alpha=0.3)

ax2.set_title('Changes in y-axis reading over time')
ax2.set_ylabel('\u0394 Y')
ax2.xaxis.set_major_locator(mdates.MinuteLocator(interval=60))
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax2.tick_params(axis='x', rotation=45)  # Rotate x-axis labels by 90 degrees

# Plot changes in z-axis reading over time
ax3.plot(forplot_datetime, diff_z, color="b")

# Classify activity for diff_x
category_z = classify_activity(diff_z, 100, 300)

# Create a mask for low, medium, and high activity
low_mask = category_z == 1
medium_mask = category_z == 2
high_mask = category_z == 3

# Fill between the data points based on activity
y1 = min(diff_y)
y2 = max(diff_y)

# highlighting the activity by coloring the graph
ax3.fill_between(timestamps,y1,y2, where=high_mask, color="red", alpha=0.3)
ax3.fill_between(timestamps,y1,y2, where=medium_mask, color="yellow", alpha=0.3)
ax3.fill_between(timestamps,y1,y2, where=low_mask, color="green", alpha=0.3)

ax3.set_title('Changes in z-axis reading over time')
ax3.set_ylabel('\u0394 Z')
ax3.xaxis.set_major_locator(mdates.MinuteLocator(interval=60))
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax3.tick_params(axis='x', rotation=45)  # Rotate x-axis labels by 90 degrees

# # Plot changes in magnitude over time
# ax4.plot(forplot_datetime, diff_mag)
# ax4.set_title('Changes in magnitude over time')
# ax4.set_ylabel('\u0394 Magnitude')
# ax4.xaxis.set_major_locator(mdates.MinuteLocator(interval=60))
# ax4.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
# ax4.tick_params(axis='x', rotation=45)  # Rotate x-axis labels by 90 degrees

# Set the x-axis limits for all subplots (you can customize these limits)
xmin = datetime(datetimes[0].year, datetimes[0].month, datetimes[0].day, 0, 0)
xmax = datetime(datetimes[0].year, datetimes[0].month, datetimes[0].day, 23, 59)
ax1.set_xlim(xmin, xmax)
ax2.set_xlim(xmin, xmax)
ax3.set_xlim(xmin, xmax)
# ax4.set_xlim(xmin, xmax)

plt.tight_layout()
plt.show()