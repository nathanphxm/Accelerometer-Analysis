import re
import datetime
import argparse

def process_file(filename):
    timestamp_diff, lines = get_timestamp_diff_and_lines(filename)

    gps_filename = filename.replace('.txt', '_gps.txt')
    clean_filename = filename.replace('.txt', '_clean.txt')

    with open(gps_filename, 'w') as gps_file, \
         open(clean_filename, 'w') as clean_file:
        
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
                gps_file.write(','.join(values[3:11]) + '\n')
                continue

            if len(values) == 3 and values != ['0', '0', '0']:
                output = [current_timestamp, count] + values
                clean_file.write(','.join(map(str, output)) + '\n')
            
            count += 1


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
                dt = datetime.datetime(int(values[7]), int(values[6]), int(values[5]), int(values[8]), int(values[9]), int(values[10]))
                calculated_timestamp = int(dt.timestamp())
                break  

    return calculated_timestamp - given_timestamp, lines

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a file and split its content based on certain conditions.")
    parser.add_argument("filename", help="Path to the file to be processed.")
    args = parser.parse_args()

    process_file(args.filename)