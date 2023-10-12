### not required (testing)

import plotly.express as px
import plotly.graph_objects as go
import scripts.plotting.freq.frequency as frequency

axes = [frequency.frequency_x_per_day(),frequency.frequency_y_per_day(),frequency.frequency_z_per_day()]
axes_name = ['x','y','z']

def separate_plot():
    for axis in range(3):
        data = axes[axis]

        hour = [entry[0] for entry in data[1:]]
        freq = [entry[1] for entry in data[1:]]

        fig = px.line(x=hour, y=freq, title='Frequency of Movement in '+axes_name[axis]+'-axis',labels={'x': 'Hour', 'y': 'Frequency'}, template='plotly', width=800, height=400)

        fig.show()

def combined_plot():
    colors = ['red', 'green', 'blue']

    fig = go.Figure()

    for axis in range(3):
        data = axes[axis]
        hour = [entry[0] for entry in data[1:]]
        freq = [entry[1] for entry in data[1:]]
        
        fig.add_trace(go.Scatter(x=hour, y=freq, mode='lines', name=axes_name[axis] + '-axis', line=dict(color=colors[axis])))

    fig.update_layout(title='Frequency of Movement in XYZ Axes', xaxis_title='Hour', yaxis_title='Frequency', width=800, height=400)

    fig.show()

combined_plot()
