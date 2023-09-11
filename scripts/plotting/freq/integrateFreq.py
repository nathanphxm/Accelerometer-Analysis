import datetime

def parse_timestamp(unix_timestamp):
    timestamp = datetime.datetime.fromtimestamp(unix_timestamp)
    return timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute, timestamp.second

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

file_data = read_file('../../../resources/file011_clean.txt')

def get_filtered_data(month, day=None, hour=None, minute=None, second=None):
    filtered_data = [['Index', 'X', 'Y', 'Z']]
    
    for line in file_data[1:]:
        if line[1] == month and (day is None or line[2] == day) and \
           (hour is None or line[3] == hour) and (minute is None or line[4] == minute) and \
           (second is None or line[5] == second):
            filtered_data.append(line[6:])
    
    return filtered_data

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

def frequency_per_day_by_second(month, day):
    frequencies = [["Time", "Frequency of movement"]]
    
    for hour in range(24):
        for minute in range(60):
            for second in range(60):
                data = get_filtered_data(month, day, hour, minute, second)
                frequency = calculate_frequency(data)  
                time_str = f"{month}/{day} {hour:02d}:{minute:02d}:{second:02d}"
                frequencies.append([time_str, frequency])
    
    return frequencies

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

def frequency_per_day_by_hour(month, day):
    frequencies = [["Hour", "Frequency of movement"]]
    
    for hour in range(24):
        data = get_filtered_data(month, day, hour)
        frequency = calculate_frequency(data)
        frequencies.append([hour, frequency])
    
    return frequencies

if __name__ == "__main__":
    month = 2
    day = 19
    
    freq = frequency_per_day_by_minute(month, day)
    print(freq)

    #x_frequencies = frequency_per_day_by_minute(month, day, 1)  # X-axis index
    #y_frequencies = frequency_per_day_by_minute(month, day, 2)  # Y-axis index
    #z_frequencies = frequency_per_day_by_minute(month, day, 3)  # Z-axis index    

    # x_frequencies = frequency_per_day_by_hour(month, day, 1)  # X-axis index
    # y_frequencies = frequency_per_day_by_hour(month, day, 2)  # Y-axis index
    # z_frequencies = frequency_per_day_by_hour(month, day, 3)  # Z-axis index

    # x_frequencies = frequency_per_day_by_second(month, day, 1)  # X-axis index
    # y_frequencies = frequency_per_day_by_second(month, day, 2)  # Y-axis index
    # z_frequencies = frequency_per_day_by_second(month, day, 3)  # Z-axis index

    # print("X-axis Frequencies per Day")
    # for freq in x_frequencies:
    #     print(freq)
    
    # print("Y-axis Frequencies per Day:")
    # for freq in y_frequencies:
    #     print(freq)
    
    # print("Z-axis Frequencies per Day:")
    # for freq in z_frequencies:
    #     print(freq)

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

month = 2
day = 19
freq_data = frequency_per_day_by_minute(month, day)

# Extract x-axis (time) and y-axis (frequency) data
time_str = [entry[0] for entry in freq_data[1:]]  # Skipping the header row
frequency = [entry[1] for entry in freq_data[1:]]  # Skipping the header row

# Convert time strings to datetime objects
time = [datetime.strptime(ts, "%m/%d %H:%M") for ts in time_str]

# Create a line plot
plt.figure(figsize=(12, 6), facecolor='white')
plt.plot(time, frequency, linestyle='-')
plt.xlabel('Time')
plt.ylabel('Frequency of Movement')
plt.title(f'Frequency of Movement on {month}/{day} by Minute')

# Format the x-axis to display time at 15-minute intervals
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=15))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

plt.grid(False)

# Display the plot
plt.tight_layout()
plt.show()