import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from scipy.fftpack import fft,fftfreq

def plot_fft(axis, sample_rate, direction, ax):
    transformed_axis = np.fft.fft(axis)
    freqs_magnitude = np.abs(transformed_axis)
    freq_axis = np.linspace(0, sample_rate, len(freqs_magnitude))

    ax.plot(freq_axis, freqs_magnitude)
    ax.set_title("FFT of " + direction)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude")
    ax.set_xlim(0, 100)

def plot_fft2(axis, total_second, direction, ax):
    sample_rate = 25
    N = sample_rate*total_second
    frequency = np.linspace(0.0, (sample_rate/2), int (N/2))

    freq_data = fft(axis)
    y = 2/N * np.abs (freq_data [0: int(N/2)])
    #y = y - np.mean(y)

    ax.plot(frequency[frequency>=0.2], y[frequency>=0.2])
    ax.set_ylim(0,1)
    ax.set_title('Frequency domain Signal of ' + direction)
    ax.set_xlabel('Frequency in Hz')
    ax.set_ylabel("Amplitude")

def plot_graph():
    with open('./sample_data/file007_clean.txt', 'r') as file:
        lines = file.readlines()

    times, xs, ys, zs = [], [], [], []

    for line in lines:
        timestamp, iteration, x, y, z = map(int, line.split(","))
        time = timestamp + (iteration - 1) / 25.0
        times.append(time)
        xs.append(x)
        ys.append(y)
        zs.append(z)

    # Convert timestamps to datetime objects
    datetimes = [datetime.utcfromtimestamp(ts) for ts in times]
    total_second = (datetimes[-1] - datetimes[0]).total_seconds()

    fig = plt.figure(figsize=(6, 6))
    ax1 = fig.add_subplot(3, 1, 1)
    ax2 = fig.add_subplot(3, 1, 2)
    ax3 = fig.add_subplot(3, 1, 3)

    plot_fft2(xs, total_second, "x", ax1)
    plot_fft2(ys, total_second,"y", ax2)
    plot_fft2(zs, total_second,"z", ax3)

    fig.tight_layout()
    return fig
