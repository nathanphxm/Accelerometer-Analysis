import plotly.express as px
import frequency

axes = [frequency.frequency_x_per_day(),frequency.frequency_y_per_day(),frequency.frequency_z_per_day()]
axes_name = ['x','y','z']

def separate_plot():
    for axis in range(3):
        data = axes[axis]

        hour = [entry[0] for entry in data[1:]]
        freq = [entry[1] for entry in data[1:]]

        fig = px.line(x=hour, y=freq, title='Frequency of Movement in '+axes_name[axis]+'-axis',labels={'x': 'Hour', 'y': 'Frequency'}, template='plotly', width=800, height=400)

        fig.show()


