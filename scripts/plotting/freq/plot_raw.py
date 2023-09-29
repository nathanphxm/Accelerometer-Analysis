### not required (testing - delta graph is more suitable)

import datetime
import plotly.subplots as sp
import plotly.graph_objs as go

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

file_data = read_file('../../../resources/file011_clean.txt')

print(file_data[:6])

time = [entry[0] for entry in file_data[1:]]
x_freq = [int(entry[2]) for entry in file_data[1:]]
y_freq = [int(entry[3]) for entry in file_data[1:]]
z_freq = [int(entry[4]) for entry in file_data[1:]]

fig = sp.make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=('X-Axis', 'Y-Axis', 'Z-Axis'))

fig.add_trace(go.Scatter(x=time, y=x_freq, mode='lines', name='X-Axis'), row=1, col=1)
fig.add_trace(go.Scatter(x=time, y=y_freq, mode='lines', name='Y-Axis'), row=2, col=1)
fig.add_trace(go.Scatter(x=time, y=z_freq, mode='lines', name='Z-Axis'), row=3, col=1)

fig.update_layout(title='Frequency of Movement', showlegend=True, template='plotly', width=1500, height=800)

fig.show()
