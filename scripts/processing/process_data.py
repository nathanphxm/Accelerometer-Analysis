import os
import re

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
                        current_timestamp = split_data[0].replace('*', '') 
                        continue
                    elif len(split_data) == 3:
                        accel_data.append([current_timestamp] + split_data)
                    elif len(split_data) == 11:
                        gps_data.append([current_timestamp] + split_data)
    
    print(accel_data[0])
    print(gps_data[0])
    
    return accel_data, gps_data
