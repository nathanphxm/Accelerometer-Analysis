import datetime
import plotly.express as px

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

file_data = read_file('./resources/file011_clean.txt')

def get_filtered_data(month, day=None, start_hour=None, end_hour=None, start_minute=None, end_minute=None, start_second=None, end_second=None):
    filtered_data = [['Index', 'X', 'Y', 'Z']]
    
    for line in file_data[1:]:
        if line[1] == month and (day is None or line[2] == day) and \
           (start_hour is None or start_hour <= line[3] <= end_hour) and \
           (start_minute is None or start_minute <= line[4] <= end_minute) and \
           (start_second is None or start_second <= line[5] <= end_second):
            filtered_data.append(line[6:])
    
    return filtered_data

# Modify the calculate_frequency function to consider frequency per second
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

# Modify the frequency calculation functions to consider the specified time range
def frequency_per_day_by_second(month, day, start_hour, end_hour):
    frequencies = [["Time", "Frequency of movement"]]
    
    for hour in range(start_hour, end_hour + 1):
        for minute in range(60):
            for second in range(60):
                data = get_filtered_data(month, day, start_hour, end_hour, 0, 59, 0, 59)
                frequency = calculate_frequency(data)  
                time_str = f"{month}/{day} {hour:02d}:{minute:02d}:{second:02d}"
                frequencies.append([time_str, frequency])
    
    return frequencies

# Modify other frequency calculation functions similarly

if __name__ == "__main__":
    month = 2
    day = 19
    start_hour = 12
    end_hour = 13
    
    data = frequency_per_day_by_second(month, day, start_hour, end_hour)
    print(data)

    time = [entry[0] for entry in data[1:]]
    freq = [entry[1] for entry in data[1:]]

    fig = px.line(x=time, y=freq, title='Frequency of Movement (integrated)',labels={'x': 'Time', 'y': 'Frequency'}, template='plotly', width=1500, height=600)

    fig.show()