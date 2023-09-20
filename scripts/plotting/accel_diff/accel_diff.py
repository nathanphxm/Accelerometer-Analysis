import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

with open('./paddock_data/pink69_gps0003_file011_clean.txt', 'r') as file:
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
datetimes = [datetime.utcfromtimestamp(ts) for ts in times]

def pick_hour(start,end):
    indices = np.where([dt.hour in range(start,end+1) for dt in datetimes])[0]
    filtered_datetimes = [datetimes[i] for i in indices]
    filtered_x = [xs[i] for i in indices]
    filtered_y = [ys[i] for i in indices]
    filtered_z = [zs[i] for i in indices]
    filtered_mag = [magnitude[i] for i in indices]
    filtered_iter = [iter[i] for i in indices]
    
    return filtered_datetimes,filtered_x,filtered_y,filtered_z,filtered_mag,filtered_iter

def accel_diff(datetime,x,y,z):
    change_x = []
    change_y = []
    change_z = []
    for i in range(1,len(datetime)):
        change_x.append(x[i] - x[i-1])
        change_y.append(y[i] - y[i-1])
        change_z.append(z[i] - z[i-1])
    datetime = datetime[1:]

    return datetime,change_x,change_y,change_z

select_datetimes, select_x, select_y, select_z, select_mag, select_iter = pick_hour(11,12)

#forplot_datetime, diff_x, diff_y, diff_z = accel_diff(select_datetimes,select_x,select_y,select_z)
forplot_datetime, diff_x, diff_y, diff_z = accel_diff(datetimes,xs,ys,zs)

plt.figure(figsize=(6, 6))

plt.subplot(3, 1, 1)
plt.plot(forplot_datetime, diff_x)
plt.title('Changes in x-axis reading over time')
plt.xlabel('Time')
plt.ylabel('\u0394 X')


plt.subplot(3, 1, 2)
plt.plot(forplot_datetime, diff_y)
plt.title('Changes in y-axis reading over time')
plt.xlabel('Time')
plt.ylabel('\u0394 Y')


plt.subplot(3, 1, 3)
plt.plot(forplot_datetime, diff_z)
plt.title('Changes in z-axis reading over time')
plt.xlabel('Time')
plt.ylabel('\u0394 Z')

# Format the x-axis tick labels to display only hours and minutes
for ax in plt.gcf().axes:
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

plt.tight_layout()
plt.show()

