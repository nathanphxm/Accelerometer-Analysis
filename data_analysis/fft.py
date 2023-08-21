import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

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

sample_rate = len(datetimes)
def plot_fft(time,axis,sample_rate,direction):
    # This returns the fourier transform coeficients as complex numbers
    transformed_axis = np.fft.fft(axis)

    # Take the absolute value of the complex numbers for magnitude spectrum
    freqs_magnitude = np.abs(transformed_axis)

    # Create frequency x-axis that will span up to sample_rate
    freq_axis = np.linspace(0, sample_rate, len(freqs_magnitude))

    # Plot frequency domain
    plt.plot(freq_axis, freqs_magnitude)
    plt.title("FFT of "+direction)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.xlim(0, 100)
    plt.show()

plot_fft(time,xs,sample_rate,"x")
plot_fft(time,ys,sample_rate,"y")
plot_fft(time,zs,sample_rate,"z")
