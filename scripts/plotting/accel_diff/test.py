import numpy as np
import pandas as pd
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

# Calculate the percentiles for high, medium, and low activity levels
high_percentile = np.percentile(diff_x, 100)  # You can adjust the percentile as needed
medium_percentile = np.percentile(diff_x, 50)  # You can adjust the percentile as needed

print(max(diff_x))
# high_activity_x = [val if abs(val) > high_percentile else None for val in diff_x]
# medium_activity_x = [val if abs(val) <= high_percentile and abs(val) > medium_percentile else None for val in diff_x]
# low_activity_x = [val if abs(val) <= medium_percentile else None for val in diff_x]

print(high_percentile)

# diff_x = pd.DataFrame(diff_x)
# diff_y = pd.DataFrame(diff_y)
# diff_z = pd.DataFrame(diff_z)
# diff_mag = pd.DataFrame(diff_mag)

# diff_x.to_csv("diff_x.csv")
# diff_y.to_csv("diff_y.csv")
# diff_z.to_csv("diff_z.csv")
# diff_mag.to_csv("diff_mag.csv")
