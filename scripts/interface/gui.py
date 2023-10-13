import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "processing"))
import tkinter as tk
from tkinter import ttk  # For the Combobox widget
from tkinter import filedialog
from tkinter import messagebox
# from ttkthemes import ThemedTk
import importlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from process_data import process_directory
from tkcalendar import DateEntry
from tkcalendar import Calendar
from datetime import timezone, timedelta, datetime, time
import csv

PLOTTING_DIR = os.path.join(os.path.dirname(__file__), "..", "plotting")
load_data_button = None
start_datetime = None
end_datetime = None
canvas_frame = None
ui_frame = None
accelerometer_data = []
gps_data = []
data_from_graph = []
GMT8 = timezone(timedelta(hours=8))

def styled_button(master, **kwargs):
    BUTTON_COLOR = "#3F51B5"
    BUTTON_FOREGROUND = "#FFFFFF"
    HOVER_COLOR = "#303F9F"
    #3F51B5
    
    button = tk.Button(
        master, 
        font=("Open Sans", 12, "bold"), 
        bg=BUTTON_COLOR, 
        fg=BUTTON_FOREGROUND, 
        borderwidth=0, 
        padx=15, 
        pady=2, 
        highlightthickness=0, 
        activebackground=BUTTON_COLOR, 
        activeforeground=BUTTON_FOREGROUND,
        cursor="hand2",
        **kwargs
    )

    # Event handlers for hover effect
    def on_hover(event):
        button.config(bg=HOVER_COLOR)

    def on_leave(event):
        button.config(bg=BUTTON_COLOR)
    
    # Bind the events
    button.bind("<Enter>", on_hover)
    button.bind("<Leave>", on_leave)

    return button

def load_data():
    global load_data_button, loading_label, accelerometer_data, gps_data
    directory = filedialog.askdirectory()  # Open directory selection dialog
    if directory:
        try:
            #show that data is loading
            loading_label.config(text="Processing data, please wait...", fg="white")
            root.update_idletasks()  # Process all pending GUI tasks
            if sys.platform != "linux" and sys.platform != "linux2":   
                root.config(cursor="wait")
            root.update()  # Update the GUI
            root.update_idletasks()  # Process all pending GUI tasks again

            accelerometer_data, gps_data = process_directory(directory)
            print(f"Loaded {len(accelerometer_data)} accelerometer data points.")

            #reset loading feedback
            root.config(cursor="")
            loading_label.config(text="")

            # If a directory is selected, hide the load_data_button and display the rest of the GUI components
            load_data_button.pack_forget()
            loading_label.config(text=f"Current Directory: {directory}")
            display_gui_components()
        except Exception as e:
            # Reset loading feedback
            root.config(cursor="")
            loading_label.config(text="")
            
            # Show error message
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            
            # Display the load_data_button again
            load_data_button.pack(pady=20)

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

    def on_hour_changed(event=None):
        selected_date = datetime.strptime(calendar.get_date(), '%m/%d/%y').date()
        # Reset minute scale to full range initially
        minute_scale.config(from_=0, to=59)
        
        if selected_date == min_datetime.date():
            if hour_scale.get() == min_datetime.hour:
                minute_scale.config(from_=min_datetime.minute)
        elif selected_date == max_datetime.date():
            if hour_scale.get() == max_datetime.hour:
                minute_scale.config(to=max_datetime.minute)

    hour_scale.bind("<B1-Motion>", on_hour_changed)  # Bind the function to the hour slider's change event

    def on_ok():
        selected_date_str = calendar.get_date()
        selected_date = datetime.strptime(selected_date_str, '%m/%d/%y').date()
        selected_time = time(hour=hour_scale.get(), minute=minute_scale.get())
        selected_datetime = datetime.combine(selected_date, selected_time)
        popup.selected_datetime = selected_datetime
        popup.destroy()

    def on_cancel():
        popup.destroy()

    ok_button = styled_button(popup, text="OK", command=on_ok)
    ok_button.pack(side=tk.LEFT, padx=10, pady=10)

    cancel_button = styled_button(popup, text="Cancel", command=on_cancel)
    cancel_button.pack(side=tk.RIGHT, padx=10, pady=10)

    popup.grab_set()  # Makes the popup modal
    root.wait_window(popup)  # Waits until the popup is closed
    return getattr(popup, 'selected_datetime', None)

def display_gui_components():
    global ui_frame

    min_datetime = datetime.fromtimestamp(accelerometer_data[0][0], GMT8)
    max_datetime = datetime.fromtimestamp(accelerometer_data[-1][0], GMT8)

    # Start date and time button
    def set_start_datetime():
        global start_datetime
        max_dt = end_datetime if end_datetime else max_datetime
        selected_datetime = get_datetime_popup(initial_datetime=min_datetime, min_datetime=min_datetime, max_datetime=max_dt)
        if selected_datetime:
            start_datetime_button.config(text=selected_datetime.strftime('%Y-%m-%d %H:%M'))
            start_datetime_button.selected_datetime = selected_datetime
            start_datetime = selected_datetime  # Update the global variable

    start_datetime_button = styled_button(ui_frame, text="Set Start Date & Time", command=set_start_datetime)
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

    end_datetime_button = styled_button(ui_frame, text="Set End Date & Time", command=set_end_datetime)
    end_datetime_button.pack(side=tk.LEFT, padx=5, pady=10)

    # Create a Combobox
    combobox = ttk.Combobox(ui_frame)
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
    btn = styled_button(ui_frame, text="Display Graph", command=lambda: display_graph(combobox))
    btn.pack(side=tk.RIGHT, padx=5, pady=10)

    # Button to print data
    print_button = styled_button(ui_frame, text="Print Data", command=print_data)
    print_button.pack(side=tk.RIGHT, padx=5, pady=10)

def print_data():
    global accelerometer_data
    try:
        print(accelerometer_data[0])
        print(accelerometer_data[1])
        print(accelerometer_data[2])
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
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while printing the data: {e}")

def display_graph(combobox):
    global current_canvas
    global start_datetime, end_datetime
    try:
        selected_file = combobox.get()
        
        if not start_datetime or not end_datetime:
            messagebox.showerror("Error", "Both start and end times must be selected.")
            return
        
        if not selected_file:
            messagebox.showerror("Error", "No graph type selected.")
            return

        module_path = "scripts.plotting." + selected_file.replace(os.sep, '.').rstrip('.py')

        # Dynamically import the module using the module path
        plot_module = importlib.import_module(module_path)

        # Convert the selected start and end datetimes to Unix timestamps
        start_ts = start_datetime.timestamp()
        end_ts = end_datetime.timestamp()

        # Filter the accelerometer data based on the selected time range
        filtered_data = [data for data in accelerometer_data if start_ts <= data[0] <= end_ts]
        fig = plot_module.plot_graph(filtered_data)

        # Remove the old canvas (if it exists)
        if current_canvas:
            current_canvas.get_tk_widget().destroy()
            
        # Embed the new figure in the tkinter window
        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas.draw()

        # Update current_canvas to hold a reference to the current canvas
        current_canvas = canvas
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while displaying the graph: {e}")

def on_close():
    print("Closing application...")
    
    # Destroy the window after cleanup
    root.destroy()
    root.quit()

def run_gui():
    global load_data_button, loading_label
    global canvas_frame, ui_frame
    global root
    root = tk.Tk()
    # root = ThemedTk(theme="arc")

        # Frame for top buttons
    ui_frame = tk.Frame(root)
    ui_frame.pack(side=tk.TOP, fill=tk.X)
    ui_frame.config(bg="#E0E0E0")

    root.config(bg='#E0E0E0')
    root.protocol("WM_DELETE_WINDOW", on_close)

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
    loading_label = tk.Label(ui_frame, text="", bg="#E0E0E0")
    loading_label.pack(pady=10)

    # Initially, only display the "Load Data" button in the middle
    load_data_button = styled_button(ui_frame, text="Load Data", command=load_data)
    load_data_button.pack(pady=20)
    
    canvas_frame = tk.Frame(root, bg='white')
    canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1, pady=10)
    
    root.mainloop()

current_canvas = None

if __name__ == "__main__":
    run_gui()
