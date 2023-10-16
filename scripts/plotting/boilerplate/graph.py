import matplotlib.pyplot as plt

def plot_graph(data):
    """
    THIS IS A SAMPLE FILE DESIGNED TO DEMONSTRATE STRUCTURE ONLY. 
    THIS GRAPH DOES NOT EXECUTE - PLEASE ONLY USE AS A SAMPLE.
    
    Parameters:
    - data: List of lists/tuples containing accelerometer data of the form:
            [[Timestamp, Interval, ACCEL_X, ACCEL_Y, ACCEL_Z], ...]

    Returns:
    - fig: Matplotlib figure object
    """

    # Extract the data into separate lists for easier plotting
    timestamps = [row[0] + (row[1]-1) * (1.0/max([x[1] for x in data if x[0] == row[0]])) for row in data]
    accel_x = [row[2] for row in data]
    accel_y = [row[3] for row in data]
    accel_z = [row[4] for row in data]

    # Create a new figure
    fig, ax = plt.subplots()

    # Plot the data
    ax.plot(timestamps, accel_x, label='ACCEL_X', color='r')
    ax.plot(timestamps, accel_y, label='ACCEL_Y', color='g')
    ax.plot(timestamps, accel_z, label='ACCEL_Z', color='b')

    # Set labels, title, and legend
    ax.set_xlabel('Time')
    ax.set_ylabel('Acceleration Value')
    ax.set_title('Accelerometer Data Over Time')
    ax.legend(loc='upper left')

    return fig