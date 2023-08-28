import datetime

def parse_timestamp(unix_timestamp):
    timestamp = datetime.datetime.fromtimestamp(unix_timestamp)
    return timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute, timestamp.second

def read_file(filename):
    formatted_data = [['Year', 'Month', 'Day', 'Hour', 'Minutes', 'Index', 'X', 'Y', 'Z']]
    
    with open(filename, 'r') as file:
        lines = file.readlines()
        
        for line in lines:
            col = line.strip().split(',')
            year, month, day, hour, minutes, seconds = parse_timestamp(int(col[0]))
            formatted_line = [year, month, day, hour, minutes, seconds] + col[1:]
            formatted_data.append(formatted_line)
    
    return formatted_data

file_data = read_file('../../../resources/file007_clean.txt')

def get_filtered_data(month, day=None, hour=None, minute=None, second=None):
    filtered_data = [['Index', 'X', 'Y', 'Z']]
    
    for line in file_data[1:]:
        if line[1] == month and (day is None or line[2] == day) and \
           (hour is None or line[3] == hour) and (minute is None or line[4] == minute) and \
           (second is None or line[5] == second):
            filtered_data.append(line[6:])
    
    return filtered_data

def calculate_frequency(data, axis_idx):
    frequency = 0
    previous_value = None
    
    for line in data[1:]:
        value = int(line[axis_idx])
        
        if previous_value is None:
            previous_value = value
        elif abs(value - previous_value) >= 10:
            frequency += 1
        previous_value = value
    
    return frequency

def frequency_per_day_by_second(month, day, axis_idx):
    frequencies = [["Time", "Frequency of movement"]]
    
    for hour in range(24):
        for minute in range(60):
            for second in range(60):
                data = get_filtered_data(month, day, hour, minute, second)
                frequency = calculate_frequency(data, axis_idx)  
                time_str = f"{month}/{day} {hour:02d}:{minute:02d}:{second:02d}"
                frequencies.append([time_str, frequency])
    
    return frequencies

def frequency_per_day_by_minute(month, day, axis_idx):
    frequencies = [["Time", "Frequency of movement"]]
    
    for hour in range(24):
        for minute in range(60):
            data = get_filtered_data(month, day, hour, minute)
            frequency = calculate_frequency(data, axis_idx)  
            time_str = f"{month}/{day} {hour:02d}:{minute:02d}"
            frequencies.append([time_str, frequency])
        print(frequencies)
    return frequencies

def frequency_per_day_by_hour(month, day, axis_idx):
    frequencies = [["Hour", "Frequency of movement"]]
    
    for hour in range(24):
        data = get_filtered_data(month, day, hour)
        frequency = calculate_frequency(data, axis_idx)
        frequencies.append([hour, frequency])
    
    return frequencies

if __name__ == "__main__":
    month = 2
    day = 15
    
    #x_frequencies = frequency_per_day_by_minute(month, day, 1)  # X-axis index
    #y_frequencies = frequency_per_day_by_minute(month, day, 2)  # Y-axis index
    z_frequencies = frequency_per_day_by_minute(month, day, 3)  # Z-axis index

    # print("X-axis Frequencies per Day by minute:")
    # for freq in x_frequencies:
    #     print(freq)
    
    # print("Y-axis Frequencies per Day by minute:")
    # for freq in y_frequencies:
    #     print(freq)
    
    print("Z-axis Frequencies per Day by minute:")
    print(z_frequencies)
    # for freq in z_frequencies:
    #     print(freq)
    

    # x_frequencies = frequency_per_day_by_hour(month, day, 1)  # X-axis index
    # y_frequencies = frequency_per_day_by_hour(month, day, 2)  # Y-axis index
    # z_frequencies = frequency_per_day_by_hour(month, day, 3)  # Z-axis index

    # print("X-axis Frequencies per Day")
    # for freq in x_frequencies:
    #     print(freq)
    
    # print("Y-axis Frequencies per Day:")
    # for freq in y_frequencies:
    #     print(freq)
    
    # print("Z-axis Frequencies per Day:")
    # for freq in z_frequencies:
    #     print(freq)


    # x_frequencies = frequency_per_day_by_second(month, day, 1)  # X-axis index
    # y_frequencies = frequency_per_day_by_second(month, day, 2)  # Y-axis index
    # z_frequencies = frequency_per_day_by_second(month, day, 3)  # Z-axis index

    # print("X-axis Frequencies per Day by second:")
    # for freq in x_frequencies:
    #     print(freq)
    
    # print("Y-axis Frequencies per Day by second:")
    # for freq in y_frequencies:
    #     print(freq)
    
    # print("Z-axis Frequencies per Day by second:")
    # for freq in z_frequencies:
    #     print(freq)
