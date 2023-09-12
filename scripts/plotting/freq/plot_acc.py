import datetime
import matplotlib.pyplot as plt

def parse_timestamp(unix_timestamp):
    timestamp = datetime.datetime.fromtimestamp(unix_timestamp)
    return timestamp

def read_file(filename):
    formatted_data = [['time', 'Index', 'X', 'Y', 'Z']]
    
    with open(filename, 'r') as file:
        lines = file.readlines()
        
        for line in lines:
            col = line.strip().split(',')
            col[0] = parse_timestamp(int(col[0]))
            formatted_data.append(col)
    
    return formatted_data

#file_data = read_file('../../../resources/file011_clean.txt')
#file_data = read_file('../../../paddock_data/green131_gps0459_file011_clean.txt')
#file_data = read_file('../../../paddock_data/pink181_gps1032_file011_clean.txt')
file_data = read_file('../../../paddock_data/yellow133_gps1098_file011_clean.txt')

print(file_data[:6])

time = [entry[0] for entry in file_data[1:]]
x_freq = [int(entry[2]) for entry in file_data[1:]]
y_freq = [int(entry[3]) for entry in file_data[1:]]
z_freq = [int(entry[4]) for entry in file_data[1:]]

plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(time, x_freq, label='X-Axis')
plt.title('X-Axis')
plt.xlabel('Time')
plt.ylabel('Frequency')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(time, y_freq, label='Y-Axis')
plt.title('Y-Axis')
plt.xlabel('Time')
plt.ylabel('Frequency')
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(time, z_freq, label='Z-Axis')
plt.title('Z-Axis')
plt.xlabel('Time')
plt.ylabel('Frequency')
plt.legend()

plt.suptitle('Frequency of Movement')
plt.tight_layout()
plt.show()
