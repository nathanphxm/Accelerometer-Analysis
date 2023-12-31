'''
A script to plot delta acceleration of each axis, without the highlighting.
The structure of the code follows: file reading -> calculation of diff -> plotting 
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def plot_graph(data):
    #data reading
    timestamps = [row[0] for row in data]
    accel_x = np.array([row[2] for row in data], dtype=float)
    accel_y = np.array([row[3] for row in data], dtype=float)
    accel_z = np.array([row[4] for row in data], dtype=float)
    datetimes = [datetime.fromtimestamp(ts) for ts in timestamps]

    #calculating the difference in acceleration
    diff_x = np.diff(accel_x)
    diff_y = np.diff(accel_y)
    diff_z = np.diff(accel_z)
    forplot_datetime = datetimes[1:]
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6, 6))
    timestamps = [mdates.date2num(dt) for dt in forplot_datetime]

    #function to plot the subplots, for modularisation of code
    def plot_subplot(ax, diff):
        ax.plot(timestamps, diff, color="black")

        ax.set_xlim(min(timestamps), max(timestamps))
        ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=60))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.tick_params(axis='x', rotation=45)

    plot_subplot(
        ax1,
        diff_x
    )
    ax1.set_title('Changes in x-axis reading over time')
    ax1.set_ylabel('\u0394 X')

    plot_subplot(
        ax2,
        diff_y
    )
    ax2.set_title('Changes in y-axis reading over time')
    ax2.set_ylabel('\u0394 Y')

    plot_subplot(
        ax3,
        diff_z
    )
    ax3.set_title('Changes in z-axis reading over time')
    ax3.set_ylabel('\u0394 Z')

    plt.tight_layout()
    return fig
