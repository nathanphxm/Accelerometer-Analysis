import os
import re
from datetime import datetime, timedelta

def gps_to_unix(gps_entry):
    """Converts GPS data entry to a UNIX timestamp."""
    timestamp, _, _, _, lat, lon, day, month, year, hour, minute, second = gps_entry
    dt = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
    unix_timestamp = int(dt.timestamp())
    return unix_timestamp

def process_directory(directory):
    # Regex pattern for filenames
    pattern = re.compile(r'^file[0-9]{3}\.txt$')
    
    # The header line
    header = "ACCEL_X,ACCEL_Y,ACCEL_Z,LAT,LON,DAY,MONTH,YEAR,HOUR,MINUTE,SECOND\n"
    
    accel_data = []
    gps_data = []
    current_timestamp = None
    
    # List all files in the directory
    for filename in sorted(os.listdir(directory)):
        if pattern.match(filename):  # if the filename matches the desired format
            with open(os.path.join(directory, filename), 'r') as f:
                for line in f:
                    if line == header:
                        current_timestamp = None
                        continue
                                
                    split_data = line.strip().split(',')
                    if line.startswith("*"):
                        current_timestamp = int(split_data[0].replace('*', ''))
                        continue
                    elif current_timestamp is not None:
                        if len(split_data) == 3:
                            accel_data.append([current_timestamp] + [int(val) for val in split_data])
                        elif len(split_data) == 11:
                            gps_data.append([current_timestamp] + split_data)
        
    # Determine the UNIX timestamp and the original timestamp for the first GPS entry
    first_unix_timestamp = gps_to_unix(gps_data[0])
    first_original_timestamp = int(gps_data[0][0])

    # Calculate the base UNIX timestamp for the accelerometer data
    base_unix_timestamp = first_unix_timestamp - first_original_timestamp

    # Convert accelerometer timestamps
    previous_timestamp = None
    interval_counter = 1
    for i, entry in enumerate(accel_data):
        original_timestamp = int(entry[0])
        new_unix_timestamp = base_unix_timestamp + original_timestamp

        # Check if current timestamp is same as previous, if not reset counter
        if previous_timestamp != new_unix_timestamp:
            interval_counter = 1
        else:
            interval_counter += 1

        accel_data[i] = [new_unix_timestamp, interval_counter] + entry[1:]

        # Update previous timestamp to current timestamp
        previous_timestamp = new_unix_timestamp

    # Replace timestamps in gps_data
    for i, entry in enumerate(gps_data):
        gps_data[i][0] = base_unix_timestamp + int(entry[0])

    print(accel_data[0])
    print(accel_data[1])

    print(accel_data[2])
    return accel_data, gps_data
