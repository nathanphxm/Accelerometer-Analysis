import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "processing"))
import tkinter as tk
from tkinter import ttk  # For the Combobox widget
from tkinter import filedialog
from tkinter import messagebox
import importlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from process_data import process_directory
from tkcalendar import DateEntry
from tkcalendar import Calendar
from datetime import datetime, time
import csv

PLOTTING_DIR = os.path.join(os.path.dirname(__file__), "..", "plotting")
load_data_button = None
start_datetime = None
end_datetime = None
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

def get_datetime_popup(initial_datetime=None, min_datetime=None, max_datetime=None):
    popup = tk.Toplevel(root)
    popup.title("Select Date and Time")

    calendar = Calendar(popup, selectmode="day")
    calendar.pack(pady=10, padx=10)
    calendar.calevent_remove("all")  # Remove all events
    calendar.config(mindate=min_datetime.date(), maxdate=max_datetime.date())

    hour_scale = tk.Scale(popup, from_=0, to=23, orient=tk.HORIZONTAL, label="Hour")
    hour_scale.pack(pady=10, padx=10, fill=tk.X)

    minute_scale = tk.Scale(popup, from_=0, to=59, orient=tk.HORIZONTAL, label="Minute")
    minute_scale.pack(pady=10, padx=10, fill=tk.X)

    def on_date_selected(event):
        selected_date = datetime.strptime(calendar.get_date(), '%m/%d/%y').date()
        
        # Reset scales to full range
        hour_scale.config(from_=0, to=23)
        minute_scale.config(from_=0, to=59)
        
        if selected_date == min_datetime.date():
            hour_scale.config(from_=min_datetime.hour)
            if hour_scale.get() < min_datetime.hour:
                hour_scale.set(min_datetime.hour)
            if hour_scale.get() == min_datetime.hour:
                minute_scale.config(from_=min_datetime.minute)
        elif selected_date == max_datetime.date():
            hour_scale.config(to=max_datetime.hour)
            if hour_scale.get() > max_datetime.hour:
                hour_scale.set(max_datetime.hour)
            if hour_scale.get() == max_datetime.hour:
                minute_scale.config(to=max_datetime.minute)

        if selected_date == max_datetime.date():
            hour_scale.config(from_=0, to=max_datetime.hour)
            minute_scale.config(from_=0, to=max_datetime.minute)

    if initial_datetime:
        calendar.selection_set(initial_datetime.date())
        if initial_datetime == min_datetime:
            hour_scale.config(from_=min_datetime.hour)
            minute_scale.config(from_=min_datetime.minute)
        elif initial_datetime == max_datetime:
            hour_scale.set(max_datetime.hour)
            minute_scale.set(max_datetime.minute)
        on_date_selected(None)

    calendar.bind("<<CalendarSelected>>", on_date_selected)

    def on_ok():
        selected_date_str = calendar.get_date()
        selected_date = datetime.strptime(selected_date_str, '%m/%d/%y').date()
        selected_time = time(hour=hour_scale.get(), minute=minute_scale.get())
        selected_datetime = datetime.combine(selected_date, selected_time)
        popup.selected_datetime = selected_datetime
        popup.destroy()

    def on_cancel():
        popup.destroy()

    ok_button = tk.Button(popup, text="OK", command=on_ok)
    ok_button.pack(side=tk.LEFT, padx=10, pady=10)

    cancel_button = tk.Button(popup, text="Cancel", command=on_cancel)
    cancel_button.pack(side=tk.RIGHT, padx=10, pady=10)

    popup.grab_set()  # Makes the popup modal
    root.wait_window(popup)  # Waits until the popup is closed
    return getattr(popup, 'selected_datetime', None)

def display_gui_components():
    # Frame for top buttons
    top_frame = tk.Frame(root)
    top_frame.pack(side=tk.TOP, fill=tk.X)

    min_datetime = datetime.utcfromtimestamp(accelerometer_data[0][0])
    max_datetime = datetime.utcfromtimestamp(accelerometer_data[-1][0])

    # Start date and time button
    def set_start_datetime():
        global start_datetime
        max_dt = end_datetime if end_datetime else max_datetime
        selected_datetime = get_datetime_popup(initial_datetime=min_datetime, min_datetime=min_datetime, max_datetime=max_dt)
        if selected_datetime:
            start_datetime_button.config(text=selected_datetime.strftime('%Y-%m-%d %H:%M'))
            start_datetime_button.selected_datetime = selected_datetime
            start_datetime = selected_datetime  # Update the global variable

    start_datetime_button = tk.Button(top_frame, text="Set Start Date & Time", command=set_start_datetime)
    start_datetime_button.pack(side=tk.LEFT, padx=5, pady=10)

    # End date and time button
    def set_end_datetime():
        global end_datetime
        min_dt = start_datetime if start_datetime else min_datetime
        selected_datetime = get_datetime_popup(initial_datetime=max_datetime, min_datetime=min_dt, max_datetime=max_datetime)
        if selected_datetime:
            end_datetime_button.config(text=selected_datetime.strftime('%Y-%m-%d %H:%M'))
            end_datetime_button.selected_datetime = selected_datetime
            end_datetime = selected_datetime  # Update the global variable

    end_datetime_button = tk.Button(top_frame, text="Set End Date & Time", command=set_end_datetime)
    end_datetime_button.pack(side=tk.LEFT, padx=5, pady=10)

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
    global accelerometer_data

     # Check if timestamps are selected
    if start_datetime is None or end_datetime is None:
        messagebox.showwarning("Warning", "Please select both start and end timestamps before printing.")
        return
        
    # Prompt the user for a file name/location
    file_name = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if not file_name:
        return

    # Convert the selected start and end datetimes to Unix timestamps
    start_ts = start_datetime.timestamp()
    end_ts = end_datetime.timestamp()

    # Filter the accelerometer data based on the selected time range
    filtered_data = [data for data in accelerometer_data if start_ts <= data[0] <= end_ts]

    # Write the filtered data to the chosen file in CSV format
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Timestamp", "Interval", "ACCEL_X", "ACCEL_Y", "ACCEL_Z"])
        writer.writerows(filtered_data)

    print(f"Data saved to {file_name}")

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
