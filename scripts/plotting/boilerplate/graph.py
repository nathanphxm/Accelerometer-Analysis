import matplotlib.pyplot as plt

def plot_graph():
    # Sample data
    x = [0, 1, 2, 3, 4, 5]
    y = [0, 1, 4, 9, 16, 25]

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Plot the data
    ax.plot(x, y, label='y = x^2', color='blue', marker='o')

    # Set the title and labels
    ax.set_title('A Basic Matplotlib Graph')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.legend()

    return fig