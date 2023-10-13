### required by client

# The main function for this code is to highlight different activity level (low, moderate, high) on the cumulative frequency graph.
# Two threshold values are adjustable to determine the categorisation of activity level.
# Month and day can be selected to adjust the intended timeframe.

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

import datetime

# funtion to change timestamp to normal datetime
def parse_timestamp(unix_timestamp):
    timestamp = datetime.datetime.fromtimestamp(unix_timestamp)
    return timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute, timestamp.second

# function to read and process file into useable format
def read_file(filename):
    formatted_data = [['Year', 'Month', 'Day', 'Hour', 'Minutes', 'Seconds', 'Index', 'X', 'Y', 'Z']]
    
    with open(filename, 'r') as file:
        lines = file.readlines()
        
        for line in lines:
            col = line.strip().split(',')
            year, month, day, hour, minutes, seconds = parse_timestamp(int(col[0]))
            formatted_line = [year, month, day, hour, minutes, seconds] + col[1:]
            formatted_data.append(formatted_line)
    
    return formatted_data

# choose file required to be calculated and visualised
#file_data = read_file('../../../resources/file011_clean.txt')
#file_data = read_file('../../../paddock_data/green131_gps0459_file011_clean.txt')
#file_data = read_file('../../../paddock_data/pink181_gps1032_file011_clean.txt')
file_data = read_file('../../../paddock_data/yellow133_gps1098_file011_clean.txt')

# function to filter out time selection
def get_filtered_data(month, day=None, hour=None, minute=None, second=None):
    filtered_data = [['Index', 'X', 'Y', 'Z']]
    
    for line in file_data[1:]:
        if line[1] == month and (day is None or line[2] == day) and \
           (hour is None or line[3] == hour) and (minute is None or line[4] == minute) and \
           (second is None or line[5] == second):
            filtered_data.append(line[6:])
    
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
def frequency_per_day_by_minute(month, day):
    frequencies = [["Time", "Frequency of movement"]]
    
    for hour in range(24):
        for minute in range(60):
            data = get_filtered_data(month, day, hour, minute)
            frequency = calculate_frequency(data)  
            time_str = f"{month}/{day} {hour:02d}:{minute:02d}"
            frequencies.append([time_str, frequency])
        print(frequencies)
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

# run all functions required to calculate cumulative frequency, categorise activity level and visualise them
if __name__ == "__main__":
    month = 2
    day = 19

    freq_data = frequency_per_day_by_minute(month, day)

    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from datetime import datetime

    # Extract x-axis (time) and y-axis (frequency) data
    time_str = [entry[0] for entry in freq_data[1:]]  # Skipping the header row
    cumulative_freq = 0
    frequency = []
    for entry in freq_data[1:]:
        cumulative_freq += entry[1]
        frequency.append(cumulative_freq)

    # Convert time strings to datetime objects
    time = [datetime.strptime(ts, "%m/%d %H:%M") for ts in time_str]

    # Define thresholds for low, moderate, and high activity
    low_activity_threshold = 500
    high_activity_threshold = 1000

    # Create a line plot for cumulative frequency
    plt.figure(figsize=(12, 6), facecolor='white')
    plt.plot(time, frequency, marker='o', color='blue', label='Cumulative Frequency')

    import csv

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

    plt.xlabel('Time')
    plt.ylabel('Cumulative Frequency of Movement')
    plt.title(f'Cumulative Frequency of Movement on {month}/{day} by Minute')

    # Format the x-axis to display time at 1-hour intervals
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

    # Set the x-axis limits to 00:00 to 23:59
    plt.xlim(datetime(time[0].year, time[0].month, time[0].day, 0, 0), 
             datetime(time[-1].year, time[-1].month, time[-1].day, 23, 59))

    # Customise legend
    handles = [plt.Rectangle((0, 0), 1, 1, color=color_by_activity(act)) for act in ["Low Activity", "Moderate Activity", "High Activity"]]
    plt.legend(handles, ["Low Activity", "Moderate Activity", "High Activity"])

    plt.xticks(rotation=90)
    plt.grid(False)

    # Display the plot
    plt.tight_layout()
    plt.show()