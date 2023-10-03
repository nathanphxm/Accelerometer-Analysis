import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "processing"))
import tkinter as tk
from tkinter import ttk  # For the Combobox widget
from tkinter import filedialog
import importlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from process_data import process_directory

PLOTTING_DIR = os.path.join(os.path.dirname(__file__), "..", "plotting")
load_data_button = None
accelerometer_data = []
gps_data = []

def load_data():
    global load_data_button, loaded_directory_label, loading_label, accelerometer_data, gps_data
    directory = filedialog.askdirectory()  # Open directory selection dialog
    if directory:
        #show that data is loading
        loading_label.config(text="Processing data, please wait...", fg="red")
        root.update_idletasks()  # Process all pending GUI tasks
        root.config(cursor="wait")
        root.update()  # Update the GUI
        root.update_idletasks()  # Process all pending GUI tasks again

        accelerometer_data, gps_data = process_directory(directory)

        #reset loading feedback
        root.config(cursor="")
        loading_label.config(text="")

        # If a directory is selected, hide the load_data_button and display the rest of the GUI components
        load_data_button.pack_forget()
        loaded_directory_label.config(text=f"Current Directory: {directory}")
        display_gui_components()

def display_gui_components():
    # Frame for top buttons
    top_frame = tk.Frame(root)
    top_frame.pack(side=tk.TOP, fill=tk.X)

    # Create a Combobox
    combobox = ttk.Combobox(top_frame)
    combobox.pack(side=tk.LEFT, pady=20, padx=20)

    # Populate Combobox with Python scripts from all subdirectories in the plotting folder
    scripts = []
    for subdir, _, files in os.walk(PLOTTING_DIR):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                relative_path = os.path.relpath(os.path.join(subdir, file), PLOTTING_DIR)
                scripts.append(relative_path)

    combobox['values'] = scripts

    # Button to display graph
    btn = tk.Button(top_frame, text="Display Graph", command=lambda: display_graph(combobox))
    btn.pack(side=tk.RIGHT, padx=5, pady=10)

    # Button to print data
    print_button = tk.Button(top_frame, text="Print Data", command=print_data)
    print_button.pack(side=tk.RIGHT, padx=5, pady=10)

def print_data():
    global accelerometer_data, gps_data
    print(gps_data)

def display_graph(combobox):
    global current_canvas
    selected_file = combobox.get()
    if not selected_file:
        return

    module_path = "scripts.plotting." + selected_file.replace(os.sep, '.').rstrip('.py')

    # Dynamically import the module using the module path
    plot_module = importlib.import_module(module_path)

    fig = plot_module.plot_graph()

    # Remove the old canvas (if it exists)
    if current_canvas:
        current_canvas.get_tk_widget().destroy()
        
    # Embed the new figure in the tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas.draw()

    # Update current_canvas to hold a reference to the current canvas
    current_canvas = canvas

def run_gui():
    global load_data_button, loaded_directory_label, loading_label
    global root
    root = tk.Tk()

    # Maximizing the window based on the platform
    if sys.platform == "win32":
        root.state('zoomed')
    elif sys.platform == "linux" or sys.platform == "linux2":
        root.attributes('-zoomed', True)
    elif sys.platform == "darwin":
        w, h = root.winfo_screenwidth() * 0.8, root.winfo_screenheight() * 0.8
        x, y = (root.winfo_screenwidth() - w) // 2, (root.winfo_screenheight() - h) // 2
        root.geometry(f"{int(w)}x{int(h)}+{int(x)}+{int(y)}")

    # Label to display the path of the loaded directory
    loaded_directory_label = tk.Label(root, text="")
    loaded_directory_label.pack(pady=10)

    loading_label = tk.Label(root, text="")
    loading_label.pack(pady=10)

    # Initially, only display the "Load Data" button in the middle
    load_data_button = tk.Button(root, text="Load Data", command=load_data)
    load_data_button.pack(pady=20)

    root.mainloop()

current_canvas = None

if __name__ == "__main__":
    run_gui()
