'''
This script runs the Fast Fourier Transform of the acceleration data on x, y, and z axis. 
The input is one day worth of data. 
Calculation is based on the this reference: https://www.alphabold.com/fourier-transform-in-python-vibration-analysis/
The calculation is then used to plot a FFT graph showing amplitude of FFT signal against frequency domain
'''


import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from scipy.fftpack import fft,fftfreq

with open('./sample_data/file007_clean.txt', 'r') as file:
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
print(datetimes[0])
# Calculate the time difference between consecutive datetimes
time_diff = (datetimes[-1] - datetimes[0]).total_seconds() / (len(datetimes) - 1)
print(time_diff)

# calculating average sampling rate throughout the day
for i in range(len(iter)-1):
    if(iter[i+1]<iter[i]):
        for_mean.append(iter[i])
avg_sample_rate = np.mean(for_mean)

#function to plot FFT graph from the given set of data
def fft_plot3(axis,direction):
    sample_rate = avg_sample_rate # average sampling rate
    total_second = (datetimes[-1] - datetimes[0]).total_seconds()
    N = sample_rate*total_second
    frequency = np.linspace(0.0, (sample_rate/2), int (N/2)) # forming the frequency domain

    freq_data = fft(axis) # performing FFT to the data
    y = 2/N * np.abs (freq_data [0: int(N/2)])
    #y = y - np.mean(y)

    plt.plot(frequency[frequency>0.4], y[frequency>0.4])
    plt.ylim(0,1)
    plt.title('Frequency domain Signal of ' +direction)
    plt.xlabel('Frequency in Hz')
    plt.ylabel("Amplitude")
    plt.show()

# fft_plot3(xs,"x")
# fft_plot3(ys,"y")
# fft_plot3(zs,"z")
# fft_plot3(magnitude,"total magnitude")
# source: https://www.alphabold.com/fourier-transform-in-python-vibration-analysis/