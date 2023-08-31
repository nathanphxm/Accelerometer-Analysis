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
print(datetimes[0])
# Calculate the time difference between consecutive datetimes
time_diff = (datetimes[-1] - datetimes[0]).total_seconds() / (len(datetimes) - 1)
print(time_diff)

sample = len(datetimes)

def plot_fft(time,axis,sample_rate,direction):
    # This returns the fourier transform coeficients as complex numbers
    transformed_axis = np.fft.fft(axis)

    # Take the absolute value of the complex numbers for magnitude spectrum
    freqs_magnitude = np.abs(transformed_axis)

    # Create frequency x-axis that will span up to sample_rate
    freq_axis = np.linspace(0, sample//2, num = len(freqs_magnitude))

    # Plot frequency domain
    plt.plot(freq_axis, freqs_magnitude)
    plt.title("FFT of "+direction)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.xlim(0, 100)
    plt.show()

# plot_fft(datetimes,xs,sample_rate,"x")
# plot_fft(datetimes,ys,sample_rate,"y")
# plot_fft(datetimes,zs,sample_rate,"z")


def plot_fft2(axis):
    axis -= np.mean(axis)
    fft = np.fft.fft(axis)
    fftfreq = np.fft.fftfreq(len(axis))
    plt.ylabel("Amplitude")
    plt.xlabel("Frequency [Hz]")
    plt.plot(fftfreq[fftfreq>=0], np.abs(fft)[fftfreq>=0])
    plt.show()

# plot_fft2(xs)
# plot_fft2(ys)
# plot_fft2(zs)

#source: https://www.alphabold.com/fourier-transform-in-python-vibration-analysis/
for i in range(len(iter)-1):
    if(iter[i+1]<iter[i]):
        for_mean.append(iter[i])


avg_sample_rate = np.mean(for_mean)
def fft_plot3(axis,direction):
    sample_rate = avg_sample_rate
    total_second = (datetimes[-1] - datetimes[0]).total_seconds()
    N = sample_rate*total_second
    frequency = np.linspace(0.0, (sample_rate/2), int (N/2))

    freq_data = fft(axis)
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
# check: https://stackoverflow.com/questions/69356006/fast-fourier-transform-of-subset-of-vibration-dataset