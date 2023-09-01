import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from scipy.fftpack import fft,fftfreq

with open('./sample_data/file007_clean.txt', 'r') as file:
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



hour_start = 11
hour_end = 13
indices = np.where([dt.hour in range(hour_start,hour_end+1) for dt in datetimes])[0]
filtered_datetimes = [datetimes[i] for i in indices]
filtered_x = [xs[i] for i in indices]
filtered_y = [ys[i] for i in indices]
filtered_z = [zs[i] for i in indices]
filtered_mag = [magnitude[i] for i in indices]
filtered_iter = [iter[i] for i in indices]

for i in range(len(filtered_iter)-1):
    if(filtered_iter[i+1]<filtered_iter[i]):
        for_mean.append(filtered_iter[i])


avg_sample_rate = np.mean(for_mean)

def fft_plot3(axis,datetimes,sample_rate,direction):
    total_second = (datetimes[-1] - datetimes[0]).total_seconds()
    N = sample_rate*total_second
    frequency = np.linspace(0.0, (sample_rate/2), int (N/2))

    freq_data = fft(axis)
    y = 2/N * np.abs (freq_data [0: int(N/2)])
    #y = y - np.mean(y)

    plt.plot(frequency[frequency>0.4], y[frequency>0.4])
    plt.ylim(0,4)
    plt.title('Frequency domain Signal of ' +direction)
    plt.xlabel('Frequency in Hz')
    plt.ylabel("Amplitude")
    plt.show()

fft_plot3(filtered_x,filtered_datetimes,avg_sample_rate,"x")
fft_plot3(filtered_y,filtered_datetimes,avg_sample_rate,"y")
fft_plot3(filtered_z,filtered_datetimes,avg_sample_rate,"z")
fft_plot3(filtered_mag,filtered_datetimes,avg_sample_rate,"total magnitude")
