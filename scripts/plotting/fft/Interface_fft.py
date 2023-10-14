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
import matplotlib.dates as mdates

#function to plot FFT graph from the given set of data
def fft_calc(sample_rate, total_second, axis):
    N = sample_rate*total_second
    frequency = np.linspace(0.0, (sample_rate/2), int (N/2)) # forming the frequency domain

    freq_data = fft(axis) # performing FFT to the data
    y = 2/N * np.abs (freq_data [0: int(N/2)])
    #y = y - np.mean(y)

    return frequency, y
    plt.plot(frequency[frequency>0.4], y[frequency>0.4])
    plt.ylim(0,1)
    plt.title('Frequency domain Signal of ' +direction)
    plt.xlabel('Frequency in Hz')
    plt.ylabel("Amplitude")

def plot_graph(data):

    # Extract the data into separate lists for easier plotting
    timestamps = [row[0] for row in data]
    iter = [row[1] for row in data]
    accel_x = np.array([row[2] for row in data]).astype(float)  # Convert to numeric type
    accel_y = np.array([row[3] for row in data]).astype(float)
    accel_z = np.array([row[4] for row in data]).astype(float)

    for_mean = []
    frequency = []
    y = []

    # Convert timestamps to datetime objects
    # Convert timestamps to datetime objects
    datetimes = [datetime.fromtimestamp(ts) for ts in timestamps]

    # Calculate the total second in a file
    total_second = (datetimes[-1] - datetimes[0]).total_seconds()
    
    # calculating average sampling rate throughout the day
    for i in range(len(iter)-1):
        if(iter[i+1]<iter[i]):
            for_mean.append(iter[i])

    avg_sample_rate = np.mean(for_mean)

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6, 6))

    frequency, y = fft_calc(avg_sample_rate, total_second, accel_x)
    ax1.plot(frequency[frequency>0.4], y[frequency>0.4], color="b")
    ax1.set_title('Frequency domain Signal of X')
    ax1.set_xlabel('Frequency in Hz')
    ax1.set_ylabel('Amplitude')
    
    # Plot changes in y-axis reading over time
    frequency, y = fft_calc(avg_sample_rate, total_second, accel_y)
    ax2.plot(frequency[frequency>0.4], y[frequency>0.4], color="b")
    ax2.set_title('Frequency domain Signal of Y')
    ax2.set_xlabel('Frequency in Hz')
    ax2.set_ylabel('Amplitude')


    # Plot changes in z-axis reading over time
    frequency, y = fft_calc(avg_sample_rate, total_second, accel_z)
    ax3.plot(frequency[frequency>0.4], y[frequency>0.4], color="b")
    ax3.set_title('Frequency domain Signal of Z')
    ax3.set_xlabel('Frequency in Hz')
    ax3.set_ylabel('Amplitude')

    # Set the x-axis limits for all subplots (you can customize these limits)
    ax1.set_ylim(0, 1)
    ax2.set_ylim(0, 1)
    ax3.set_ylim(0, 1)

    plt.tight_layout()

    return fig
