import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

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

#select_datetimes, select_x, select_y, select_z, select_mag, select_iter = pick_hour(11,12)

#forplot_datetime, diff_x, diff_y, diff_z = accel_diff(select_datetimes,select_x,select_y,select_z)
forplot_datetime, diff_x, diff_y, diff_z, diff_mag = accel_diff(datetimes,xs,ys,zs,magnitude)

# Create a figure and three subplots
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(6, 6), sharex=True)

# Plot changes in x-axis reading over time
ax1.plot(forplot_datetime, diff_x)
ax1.set_title('Changes in x-axis reading over time')
ax1.set_ylabel('\u0394 X')
# Format the x-axis tick labels to display only hours and minutes
ax1.xaxis.set_major_locator(mdates.MinuteLocator(interval=60))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xlim(datetime(datetimes[0].year, datetimes[0].month, datetimes[0].day, 0, 0),
             datetime(datetimes[0].year, datetimes[0].month, datetimes[0].day, 23, 59))

# Plot changes in y-axis reading over time
ax2.plot(forplot_datetime, diff_y)
ax2.set_title('Changes in y-axis reading over time')
ax2.set_ylabel('\u0394 Y')
ax2.xaxis.set_major_locator(mdates.MinuteLocator(interval=60))
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

plt.xlim(datetime(datetimes[0].year, datetimes[0].month, datetimes[0].day, 0, 0),
             datetime(datetimes[0].year, datetimes[0].month, datetimes[0].day, 23, 59))

# Plot changes in z-axis reading over time
ax3.plot(forplot_datetime, diff_z)
ax3.set_title('Changes in z-axis reading over time')
ax3.set_ylabel('\u0394 Z')
ax3.xaxis.set_major_locator(mdates.MinuteLocator(interval=60))
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

plt.xlim(datetime(datetimes[0].year, datetimes[0].month, datetimes[0].day, 0, 0),
             datetime(datetimes[0].year, datetimes[0].month, datetimes[0].day, 23, 59))


#plot changes in magnitude over time
ax4.plot(forplot_datetime, diff_mag)
ax4.set_title('Changes in magnitude over time')
ax4.set_ylabel('\u0394 Magnitude')
ax4.xaxis.set_major_locator(mdates.MinuteLocator(interval=60))
ax4.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xlim(datetime(datetimes[0].year, datetimes[0].month, datetimes[0].day, 0, 0),
             datetime(datetimes[0].year, datetimes[0].month, datetimes[0].day, 23, 59))

plt.xticks(rotation = 90)

plt.tight_layout()
plt.show()

