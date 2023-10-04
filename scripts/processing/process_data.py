import re
import datetime
import os

def process_file(filename):
    timestamp_diff, lines = get_timestamp_diff_and_lines(filename)

    accelerometer_data = []
    gps_data = []

    current_timestamp = 0
    count = 1
    for line in lines:
        line = line.strip()
        values = line.split(',')
        
        match = re.match(r'\*(\d+)', line)
        if match:
            current_timestamp = int(match.group(1)) + timestamp_diff
            count = 1
            continue

        if len(values) == 11:
            gps_data.append(values[3:11])
            continue

        if len(values) == 3 and values != ['0', '0', '0']:
            output = [current_timestamp, count] + values
            accelerometer_data.append(output)
        
        count += 1

    return accelerometer_data, gps_data


def get_timestamp_diff_and_lines(filename):
    calculated_timestamp = 0
    given_timestamp = 0
    lines = []
    
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            values = line.split(',')
            
            match = re.match(r'\*(\d+)', line)
            if match:
                given_timestamp = int(match.group(1))

            if len(values) == 11:
                dt = datetime.datetime(int(values[7]), int(values[6]), int(values[5]), int(values[8]), int(values[9]), int(values[10]), tzinfo=datetime.timezone.utc)
                calculated_timestamp = int(dt.timestamp())
                break  

    return calculated_timestamp - given_timestamp, lines

def process_directory(directory):
    # List all files in the directory
    files = os.listdir(directory)

    # Filter out files that match the pattern
    pattern = re.compile(r'file\d{3}\.txt')
    matching_files = [f for f in files if pattern.match(f)]

    # Process each file and concatenate the data
    all_accelerometer_data = []
    all_gps_data = []
    for filename in matching_files:
        filepath = os.path.join(directory, filename)
        accelerometer_data, gps_data = process_file(filepath)
        all_accelerometer_data.extend(accelerometer_data)
        all_gps_data.extend(gps_data)

    return all_accelerometer_data, all_gps_data