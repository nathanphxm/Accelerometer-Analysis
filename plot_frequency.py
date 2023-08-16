import plotly.express as px

data = [
    ['Hour', 'Frequency of movement in x-axis'],
    [0, 0], [1, 16005], [2, 16332], [3, 24628], [4, 19297], [5, 22215],
    [6, 27964], [7, 48192], [8, 46205], [9, 74172], [10, 74883], [11, 74028],
    [12, 42371], [13, 35341], [14, 11918], [15, 23325], [16, 18761],
    [17, 27914], [18, 15488], [19, 11635], [20, 19323], [21, 69447],
    [22, 73365], [23, 71908], [24, 0]
]

hour = [entry[0] for entry in data[1:]]
frequency = [entry[1] for entry in data[1:]]


fig = px.line(x=hour, y=frequency, title='Frequency of Movement in x-axis',
              labels={'x': 'Hour', 'y': 'Frequency'},
              template='plotly', width=800, height=400)


fig.show()
