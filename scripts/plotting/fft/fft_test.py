import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def plot_fft(time, axis, sample_rate, direction, ax):
    transformed_axis = np.fft.fft(axis)
    freqs_magnitude = np.abs(transformed_axis)
    freq_axis = np.linspace(0, sample_rate, len(freqs_magnitude))

    ax.plot(freq_axis, freqs_magnitude)
    ax.set_title("FFT of " + direction)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude")
    ax.set_xlim(0, 100)

def plot_graph():
    with open('./resources/file007_clean.txt', 'r') as file:
        lines = file.readlines()

    times, xs, ys, zs = [], [], [], []

    for line in lines:
        timestamp, iteration, x, y, z = map(int, line.split(","))
        time = timestamp + (iteration - 1) / 25.0
        times.append(time)
        xs.append(x)
        ys.append(y)
        zs.append(z)

    sample_rate = len(times)

    fig = plt.figure(figsize=(6, 6))
    ax1 = fig.add_subplot(3, 1, 1)
    ax2 = fig.add_subplot(3, 1, 2)
    ax3 = fig.add_subplot(3, 1, 3)

    plot_fft(times, xs, sample_rate, "x", ax1)
    plot_fft(times, ys, sample_rate, "y", ax2)
    plot_fft(times, zs, sample_rate, "z", ax3)

    fig.tight_layout()
    return fig
