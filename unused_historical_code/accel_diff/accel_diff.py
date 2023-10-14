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

def pick_hour(start,end):
    indices = np.where([dt.hour in range(start,end+1) for dt in datetimes])[0]
    filtered_datetimes = [datetimes[i] for i in indices]
    filtered_x = [xs[i] for i in indices]
    filtered_y = [ys[i] for i in indices]
    filtered_z = [zs[i] for i in indices]
    filtered_mag = [magnitude[i] for i in indices]
    filtered_iter = [iter[i] for i in indices]
    
    return filtered_datetimes,filtered_x,filtered_y,filtered_z,filtered_mag,filtered_iter

def accel_diff(datetime,x,y,z,mag):
    change_x = []
    change_y = []
    change_z = []
    change_mag = []
    for i in range(1,len(datetime)):
        change_x.append(x[i] - x[i-1])
        change_y.append(y[i] - y[i-1])
        change_z.append(z[i] - z[i-1])
        change_mag.append(mag[i] - mag[i-1])
    datetime = datetime[1:]

    return datetime,change_x,change_y,change_z,change_mag

# Define your threshold values for low, medium, and high activity
low_threshold = 300  # Adjust this threshold as needed
medium_threshold = 1000  # Adjust this threshold as needed

def classify_activity(diff_values):
    categories = []
    for value in diff_values:
        if abs(value) < low_threshold:
            categories.append(1)  # Low activity
        elif abs(value) < medium_threshold:
            categories.append(2)  # Medium activity
        else:
            categories.append(3)  # High activity
    return categories


# Now you have category labels for each type of acceleration

select_datetimes, select_x, select_y, select_z, select_mag, select_iter = pick_hour(11,12)

forplot_datetime, diff_x, diff_y, diff_z,diff_mag = accel_diff(select_datetimes,select_x,select_y,select_z,select_mag)
#forplot_datetime, diff_x, diff_y, diff_z, diff_mag = accel_diff(datetimes,xs,ys,zs,magnitude)

# Classify activity for diff_x, diff_y, diff_z, and diff_mag
category_x = classify_activity(diff_x)
category_y = classify_activity(diff_y)
category_z = classify_activity(diff_z)
category_mag = classify_activity(diff_mag)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6, 6))

ax1.plot(forplot_datetime, diff_x)
ax1.set_title('Changes in x-axis reading over time')
ax1.set_ylabel('\u0394 X')
ax1.xaxis.set_major_locator(mdates.MinuteLocator(interval=60))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax1.tick_params(axis='x', rotation=45)  # Rotate x-axis labels by 90 degrees

# Plot changes in y-axis reading over time
ax2.plot(forplot_datetime, diff_y)
ax2.set_title('Changes in y-axis reading over time')
ax2.set_ylabel('\u0394 Y')
ax2.xaxis.set_major_locator(mdates.MinuteLocator(interval=60))
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax2.tick_params(axis='x', rotation=45)  # Rotate x-axis labels by 90 degrees

# Plot changes in z-axis reading over time
ax3.plot(forplot_datetime, diff_z)
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
xmin = datetime(datetimes[0].year, datetimes[0].month, datetimes[0].day, 11, 0)
xmax = datetime(datetimes[0].year, datetimes[0].month, datetimes[0].day, 12, 0)
ax1.set_xlim(xmin, xmax)
ax2.set_xlim(xmin, xmax)
ax3.set_xlim(xmin, xmax)
# ax4.set_xlim(xmin, xmax)

plt.tight_layout()
plt.show()