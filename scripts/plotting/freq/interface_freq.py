'''
The main function of this code is to calculate the frequency of movement per minute and visualise it.
Frequency threshold value is adjustable to determine how large the difference between x(t),y(t),z(t) and x(t+1),y(t+1),z(t+1) is needed to detect a movement calculating into frequency.
'''

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from datetime import timedelta

# Define frequency detecting threshold
freq_detect_threshold = 10

# function to calculate frequency of movement
def calculate_frequency(minute_list):
    frequency = 0
    previous_values = [None, None, None]
    
    for line in minute_list:
        values = [int(value) for value in line[1:4]]  # X, Y, Z values
        
        if None in previous_values:
            previous_values = values
        else:
            if any(abs(values[i] - previous_values[i]) >= freq_detect_threshold for i in range(3)):
                frequency += 1
            previous_values = values
    
    return frequency

# function to filter out time selection
def get_freq(data):
    frequencies = [["Time", "Frequency of movement"]]
    current_time = datetime.fromtimestamp(data[0][0])
    minute_list = []

    for line in data:
        if datetime.fromtimestamp(line[0]) < (current_time + timedelta(minutes = 1)):
            minute_list.append(line[1:])
        else:
            frequency = calculate_frequency(minute_list)
            time_str = current_time
            frequencies.append([time_str, frequency])
            current_time += timedelta(minutes = 1)
            print(current_time)
            minute_list = [line[1:]]

    return frequencies
    
# function to plot graph of processed frequency data
def plot_graph(data):

    freq_data = get_freq(data)
    
    # Extract x-axis (time) and y-axis (frequency) data
    time = [entry[0] for entry in freq_data[1:]]  # Skipping the header row
    frequency = [entry[1] for entry in freq_data[1:]]

    # Create a line plot for frequency
    fig = plt.figure(figsize=(12, 6), facecolor='white')
    plt.plot(time, frequency, marker= None, color='black', label='Frequency')

    plt.xlabel('Time (GMT+8)')
    plt.ylabel('Frequency of Movement')
    plt.title('Frequency of Movement by Minute')

    # Format the x-axis to display time at 1-hour intervals
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

    plt.xticks(rotation=90)
    plt.grid(False)

    # Display the plot
    plt.tight_layout()

    return fig