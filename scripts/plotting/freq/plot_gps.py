import matplotlib.pyplot as plt
from datetime import datetime

def read_gps_file(filename):
    formatted_data = []

    with open(filename, 'r') as file:
        lines = file.readlines()

        for line in lines:
            col = line.strip().split(',')
            formatted_data.append(col)

    return formatted_data

#gps_data = read_gps_file('../../../resources/file011_gps.txt')
#gps_data = read_gps_file('../../../paddock_data/green131_gps0459_file011_gps.txt')
#gps_data = read_gps_file('../../../paddock_data/pink181_gps1032_file011_gps.txt')
gps_data = read_gps_file('../../../paddock_data/yellow133_gps1098_file011_gps.txt')

def get_filtered_data(month, day=None, hour=None, minute=None, second=None):
    filtered_data = []

    for line in gps_data[1:]:
        if line[3] == month and (day is None or line[2] == day) and \
           (hour is None or line[5] == hour) and (minute is None or line[6] == minute) and \
           (second is None or line[7] == second):
            filtered_data.append(line)

    return filtered_data

import matplotlib.dates as mdates

if __name__ == "__main__":
    month = '2'
    day = '19'

    filtered_data = get_filtered_data(month, day)

    latitudes = [float(entry[0]) for entry in filtered_data]
    longitudes = [float(entry[1]) for entry in filtered_data]
    times = [datetime(int(entry[4]), int(entry[3]), int(entry[2]), int(entry[5]), int(entry[6]), int(entry[7])) for entry in filtered_data]

    fig, ax1 = plt.subplots()

    # Primary Y-axis for Latitude
    ax1.plot(times, latitudes, color='blue', label='Latitude')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Latitude', color='blue')
    ax1.tick_params(axis='x', rotation=90)
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=15))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    plt.xlim(datetime(times[0].year, times[0].month, times[0].day, 0, 0), datetime(times[0].year, times[0].month, times[0].day, 23, 59))

    # Secondary Y-axis for Longitude
    ax2 = ax1.twinx()
    ax2.plot(times, longitudes, color='red', label='Longitude')
    ax2.set_ylabel('Longitude', color='red')

    fig.suptitle('GPS Data Over Time')

    plt.show()