# import datetime
# import pandas as pd
# import plotly.graph_objects as go
# import numpy as np

# def parse_timestamp(unix_timestamp):
#     timestamp = datetime.datetime.fromtimestamp(unix_timestamp)
#     return timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute, timestamp.second

# def read_file(filename):
#     formatted_data = []
#     column = ['Year', 'Month', 'Day', 'Hour', 'Minutes', 'Seconds', 'Index', 'X', 'Y', 'Z']
    
#     with open(filename, 'r') as file:
#         lines = file.readlines()
        
#         for line in lines:
#             col = line.strip().split(',')
#             year, month, day, hour, minutes, seconds = parse_timestamp(int(col[0]))
#             formatted_line = [year, month, day, hour, minutes, seconds] + col[1:]
#             formatted_data.append(formatted_line)
    
#     return pd.DataFrame(formatted_data, columns=column)

# file_data = read_file('../../../resources/file011_clean.txt')

# file_data['X'] = pd.to_numeric(file_data['X'], errors='coerce')
# file_data['Y'] = pd.to_numeric(file_data['Y'], errors='coerce')
# file_data['Z'] = pd.to_numeric(file_data['Z'], errors='coerce')

# # Create the plot
# fig = go.Figure(data=[
#     go.Scatter3d(
#         x=file_data['X'],
#         y=file_data['Y'],
#         z=file_data['Z'],
#         mode='markers',
#         marker=dict(
#             size=5,
#             color='rgba(244, 22, 100, 0.6)',
#             opacity=0.6
#         )
#     )
# ])

# # Update layout
# fig.update_layout(
#     scene=dict(
#         xaxis=dict(nticks=4, range=[-100, 100]),
#         yaxis=dict(nticks=4, range=[-50, 100]),
#         zaxis=dict(nticks=4, range=[-100, 100]),
#     ),
#     width=700,
#     margin=dict(r=20, l=10, b=10, t=10)
# )

# fig.show()






import datetime
import pandas as pd
import plotly.express as px

pd.set_option("display.max_rows", None)

def parse_timestamp(unix_timestamp):
    timestamp = datetime.datetime.fromtimestamp(unix_timestamp)
    return timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute, timestamp.second

def read_file(filename):
    formatted_data = []
    column = ['Year', 'Month', 'Day', 'Hour', 'Minutes', 'Seconds', 'Index', 'X', 'Y', 'Z']
    
    with open(filename, 'r') as file:
        lines = file.readlines()
        
        for line in lines:
            col = line.strip().split(',')
            year, month, day, hour, minutes, seconds = parse_timestamp(int(col[0]))
            formatted_line = [year, month, day, hour, minutes, seconds] + col[1:]
            formatted_data.append(formatted_line)
    
    return pd.DataFrame(formatted_data, columns=column)

file_data = read_file('../../../resources/file011_clean.txt')

# Print a few rows to verify the data
print("Data head:")
print(file_data.head())

# Check data types and non-integer values in 'X', 'Y', 'Z' columns
print("Data types:")
print(file_data.dtypes)

# Check the range of values in 'X', 'Y', 'Z' columns
print("Value ranges:")
print("X:", file_data['X'].min(), file_data['X'].max())
print("Y:", file_data['Y'].min(), file_data['Y'].max())
print("Z:", file_data['Z'].min(), file_data['Z'].max())

# Use the Pandas DataFrame as data argument
df = file_data[['X', 'Y', 'Z']].astype(int)
print("Data types after conversion:")
print(df.dtypes)

# Print a few rows of the converted data
print("Converted data head:")
print(df.head())

# Check if df has any data
print("Number of rows in df:", len(df))

df = df[:2000]
# Create the 3D scatter plot
fig = px.scatter_3d(df, x='X', y='Y', z='Z', size_max=2)
# fig = px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_width')
fig.show()



