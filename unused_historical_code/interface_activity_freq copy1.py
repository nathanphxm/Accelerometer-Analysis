### required by client (gui activity freq v1)

# The main function for this code is to highlight different activity level (low, moderate, high) on the cumulative frequency graph.
# Two threshold values are adjustable to determine the categorisation of activity level.
# Month and day can be selected to adjust the intended timeframe.

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from datetime import timedelta
import csv

def get_start_end_time(data):
    start_time = datetime.fromtimestamp(data[0][0])
    end_time = datetime.fromtimestamp(data[-1][0])
    return start_time, end_time

# function to filter out time selection
def get_filtered_data(data, current_time):
    filtered_data = [['Index', 'X', 'Y', 'Z']]
    next_minute = current_time + timedelta(minutes = 1)

    def filter_minute(line):
        timestamp = datetime.fromtimestamp(line[0])
        if timestamp>=current_time and timestamp<next_minute:
            return True
        return False 
    
    filtered = filter(filter_minute, data)
    filtered_min = map(lambda x: x[1:], filtered)
    filtered_data += filtered_min

    return filtered_data

# function to calculate frequency of movement
def calculate_frequency(data):
    frequency = 0
    previous_values = [None, None, None]
    
    for line in data[1:]:
        values = [int(value) for value in line[1:4]]  # X, Y, Z values
        
        if None in previous_values:
            previous_values = values
        else:
            if any(abs(values[i] - previous_values[i]) >= 10 for i in range(3)):
                frequency += 1
            previous_values = values
    
    return frequency

# function to calculate frequency of movement per minute
def frequency_per_day_by_minute(data):
    frequencies = [["Time", "Frequency of movement"]]
    
    start_time, end_time = get_start_end_time(data)
    current_time = start_time

    while current_time <= end_time:

        print(current_time)
        
        filtered_data = get_filtered_data(data, current_time)
        frequency = calculate_frequency(filtered_data)
        time_str = current_time
        frequencies.append([time_str, frequency])

        current_time += timedelta(minutes = 1)
    
    return frequencies

# function to classify different activity level
def classify_activity(frequency, low_threshold, high_threshold):
    if frequency <= low_threshold:
        return "Low Activity"
    elif frequency <= high_threshold:
        return "Moderate Activity"
    else:
        return "High Activity"

# function to provide different colour to each activity level
def color_by_activity(activity):
    if activity == "Low Activity":
        return 'blue'
    elif activity == "Moderate Activity":
        return 'green'
    else:
        return 'red'
    
# function to plot graph of processed frequency data
def plot_graph(data):

    freq_data = frequency_per_day_by_minute(data)
    
    # Extract x-axis (time) and y-axis (frequency) data
    time = [entry[0] for entry in freq_data[1:]]  # Skipping the header row
    cumulative_freq = 0
    frequency = []
    for entry in freq_data[1:]:
        cumulative_freq += entry[1]
        frequency.append(cumulative_freq)

    # Define thresholds for low, moderate, and high activity
    low_activity_threshold = 500
    high_activity_threshold = 1000

    # Create a line plot for cumulative frequency
    fig = plt.figure(figsize=(12, 6), facecolor='white')
    plt.plot(time, frequency, marker='o', color='blue', label='Cumulative Frequency')

    # Create a list to store the rows for the CSV
    csv_rows = [['Datetime', 'Frequency per Minute', 'Activity Level']]

    # Add lower-opacity squares to differentiate activity levels
    for i in range(len(time)):
        all_freq = freq_data[1:]
        freq = all_freq[i][1]
        act_level = classify_activity(freq, low_activity_threshold, high_activity_threshold)
        color = color_by_activity(act_level)
        plt.fill_between([time[i]], cumulative_freq, color=color, alpha=0.3)
        row = [time[i], freq, act_level]
        csv_rows.append(row)

    # Specify the CSV file path
    csv_file_path = 'output.csv'

    # Write the data to the CSV file
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(csv_rows)

    # Display a message indicating where the CSV file was saved
    print(f'CSV file saved at: {csv_file_path}')

    plt.xlabel('Time (GMT+8)')
    plt.ylabel('Cumulative Frequency of Movement')
    plt.title(f'Cumulative Frequency of Movement by Minute')

    # Format the x-axis to display time at 1-hour intervals
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

    # Customise legend
    handles = [plt.Rectangle((0, 0), 1, 1, color=color_by_activity(act)) for act in ["Low Activity", "Moderate Activity", "High Activity"]]
    plt.legend(handles, ["Low Activity", "Moderate Activity", "High Activity"])

    plt.xticks(rotation=90)
    plt.grid(False)

    # Display the plot
    plt.tight_layout()

    return fig