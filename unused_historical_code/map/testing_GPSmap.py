### not required (testing)

import plotly.graph_objects as go
from datetime import datetime

def read_gps_file(filename):
    formatted_data = []

    with open(filename, 'r') as file:
        lines = file.readlines()

        for line in lines:
            col = line.strip().split(',')
            formatted_data.append(col)

    return formatted_data

gps_data = read_gps_file('../../../resources/file011_gps.txt')

def get_filtered_data(month, day=None, hour=None, minute=None, second=None):
    filtered_data = []

    for line in gps_data[1:]:
        if line[3] == month and (day is None or line[2] == day) and \
           (hour is None or line[5] == hour) and (minute is None or line[6] == minute) and \
           (second is None or line[7] == second):
            filtered_data.append(line)

    return filtered_data

if __name__ == "__main__":
    month = '2'
    day = '19'

    filtered_data = get_filtered_data(month, day)

    latitudes = [float(entry[0]) for entry in filtered_data]
    longitudes = [float(entry[1]) for entry in filtered_data]
    times = [datetime(int(entry[4]), int(entry[3]), int(entry[2]), int(entry[5]), int(entry[6]), int(entry[7])) for entry in filtered_data]

    fig = go.Figure()

    # Primary Y-axis for Latitude
    fig.add_trace(go.Scatter(x=times, y=latitudes, mode='lines', name='Latitude'))

    # Secondary Y-axis for Longitude
    fig.add_trace(go.Scatter(x=times, y=longitudes, mode='lines', name='Longitude', yaxis="y2"))

    fig.update_layout(
        title="GPS Data Over Time",
        xaxis_title="Time",
        yaxis_title="Latitude",
        yaxis2=dict(title="Longitude", overlaying="y", side="right"),
    )

    fig.show()
