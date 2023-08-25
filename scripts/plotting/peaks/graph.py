import numpy as np
from scipy.signal import butter, filtfilt, find_peaks
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Read data from the specified text file
with open('./resources/file007_clean.txt', 'r') as file:
    lines = file.readlines()

times, xs, ys, zs = [], [], [], []

for line in lines:
    timestamp, iteration, x, y, z = map(int, line.split(","))
    # Convert timestamp and iteration into continuous time
    time = timestamp + (iteration - 1) / 25.0  # Subtracting 1 to start the iteration from 0
    times.append(time)
    xs.append(x)
    ys.append(y)
    zs.append(z)

# Convert timestamps to datetime objects
datetimes = [datetime.utcfromtimestamp(ts) for ts in times]

# Find the index where the time reaches 00:00
start_index = next((i for i, dt in enumerate(datetimes) if dt.hour == 0 and dt.minute == 0), None)

# If found, slice the data from that index onwards
if start_index is not None:
    times = times[start_index:]
    datetimes = datetimes[start_index:]
    xs = xs[start_index:]
    ys = ys[start_index:]
    zs = zs[start_index:]
else:
    print("No timestamp corresponding to 00:00 found!")
    exit()

# Convert lists to numpy arrays for easier calculations
xs, ys, zs = np.array(xs), np.array(ys), np.array(zs)

# Design a Butterworth low-pass filter
b, a = butter(N=3, Wn=0.1, btype='low')

# Apply the filter to the data
filtered_xs = filtfilt(b, a, xs)
filtered_ys = filtfilt(b, a, ys)
filtered_zs = filtfilt(b, a, zs)

# Segment data into 5-minute chunks and compute peaks
segment_duration = 5 * 60  # 5 minutes in seconds
end_time = times[-1]  # Last timestamp in the data
segment_starts = np.arange(times[0], end_time, segment_duration)

x_peaks, y_peaks, z_peaks = [], [], []

for start in segment_starts:
    mask = (times >= start) & (times < start + segment_duration)
    segment_x = filtered_xs[mask]
    segment_y = filtered_ys[mask]
    segment_z = filtered_zs[mask]
    
    peaks_x = find_peaks(segment_x)[0]
    peaks_y = find_peaks(segment_y)[0]
    peaks_z = find_peaks(segment_z)[0]
    
    x_peaks.append(len(peaks_x) / 5)  # Average peaks per minute
    y_peaks.append(len(peaks_y) / 5)
    z_peaks.append(len(peaks_z) / 5)

# Convert segment_starts to datetime for plotting
segment_datetimes = [datetime.utcfromtimestamp(ts) for ts in segment_starts]

# Convert segment_datetimes to numerical timestamps for calculations
segment_timestamps = [dt.timestamp() for dt in segment_datetimes]

# Generate interpolated data for smoother curves
x_interp = np.linspace(segment_timestamps[0], segment_timestamps[-1], len(segment_timestamps) * 10)
f_x = interp1d(segment_timestamps, x_peaks, kind='cubic')
f_y = interp1d(segment_timestamps, y_peaks, kind='cubic')
f_z = interp1d(segment_timestamps, z_peaks, kind='cubic')

# Convert interpolated timestamps back to datetime for plotting
x_interp_dates = [datetime.utcfromtimestamp(ts) for ts in x_interp]

# Generate hourly x-ticks and labels
hourly_ticks = [datetimes[0] + timedelta(hours=i) for i in range(24)]
hourly_labels = [dt.strftime('%H:%M') for dt in hourly_ticks]

# Plotting the number of peaks for each 5-minute segment in the same window
plt.figure(figsize=(15, 15))

# X Peaks
plt.subplot(3, 1, 1)
plt.plot(x_interp_dates, f_x(x_interp), label='X Peaks')
plt.title('Average Number of X Peaks per Minute in 5-minute segments')
plt.xlabel('Time')
plt.ylabel('Average Peaks per Minute')
plt.xticks(hourly_ticks, hourly_labels, rotation=45)
plt.grid(True)
plt.legend()

# Y Peaks
plt.subplot(3, 1, 2)
plt.plot(x_interp_dates, f_y(x_interp), label='Y Peaks')
plt.title('Average Number of Y Peaks per Minute in 5-minute segments')
plt.xlabel('Time')
plt.ylabel('Average Peaks per Minute')
plt.xticks(hourly_ticks, hourly_labels, rotation=45)
plt.grid(True)
plt.legend()

# Z Peaks
plt.subplot(3, 1, 3)
plt.plot(x_interp_dates, f_z(x_interp), label='Z Peaks')
plt.title('Average Number of Z Peaks per Minute in 5-minute segments')
plt.xlabel('Time')
plt.ylabel('Average Peaks per Minute')
plt.xticks(hourly_ticks, hourly_labels, rotation=45)
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()