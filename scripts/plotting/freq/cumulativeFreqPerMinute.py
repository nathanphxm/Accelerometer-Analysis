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

#file_data = read_file('../../../resources/file011_clean.txt')
#file_data = read_file('../../../paddock_data/green131_gps0459_file011_clean.txt')
#file_data = read_file('../../../paddock_data/pink181_gps1032_file011_clean.txt')
file_data = read_file('../../../paddock_data/yellow133_gps1098_file011_clean.txt')

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

if __name__ == "__main__":
    month = 2
    day = 19
    
    freq = frequency_per_day_by_minute(month, day)
    print(freq)

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

month = 2
day = 19
freq_data = frequency_per_day_by_minute(month, day)

# Extract x-axis (time) and y-axis (frequency) data
time_str = [entry[0] for entry in freq_data[1:]]  # Skipping the header row
cumulative_freq = 0
frequency = []
for entry in freq_data[1:]:
    cumulative_freq += entry[1]
    frequency.append(cumulative_freq)

# Convert time strings to datetime objects
time = [datetime.strptime(ts, "%m/%d %H:%M") for ts in time_str]

# Create a line plot
plt.figure(figsize=(12, 6), facecolor='white')
plt.plot(time, frequency, linestyle='-')
plt.xlabel('Time')
plt.ylabel('Frequency of Movement')
plt.title(f'Frequency of Movement on {month}/{day} by Minute')

# # Create a histogram
# plt.figure(figsize=(12, 6), facecolor='white')
# plt.hist(time, bins=len(time), weights=frequency, edgecolor='black', alpha=0.7)
# plt.xlabel('Time')
# plt.ylabel('Cumulative Frequency of Movement')
# plt.title(f'Cumulative Frequency of Movement on {month}/{day} by Minute')

# Format the x-axis to display time at 15-minute intervals
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

# Set the x-axis limits to 00:00 to 23:59
plt.xlim(datetime(time[0].year, time[0].month, time[0].day, 0, 0), datetime(time[-1].year, time[-1].month, time[-1].day, 23, 59))

plt.xticks(rotation=90)
plt.grid(False)

# Display the plot
plt.tight_layout()
plt.show()

    