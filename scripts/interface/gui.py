import os
import sys
import tkinter as tk
from tkinter import filedialog, Listbox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import importlib

PLOTTING_DIR = os.path.join(os.path.dirname(__file__), "..", "plotting")

def run_gui():
    global root
    root = tk.Tk()
    
    # Maximizing the window based on the platform
    if sys.platform == "win32":
        root.state('zoomed')
    elif sys.platform == "linux" or sys.platform == "linux2":
        root.attributes('-zoomed', True)
    elif sys.platform == "darwin":
        # For macOS, this will set the window size to 80% of the screen width and height
        # Adjust these values if you want a different size.
        w, h = root.winfo_screenwidth() * 0.8, root.winfo_screenheight() * 0.8
        x, y = (root.winfo_screenwidth() - w) // 2, (root.winfo_screenheight() - h) // 2
        root.geometry(f"{int(w)}x{int(h)}+{int(x)}+{int(y)}")

    root.title("Graph Selection")

    listbox = Listbox(root)
    listbox.pack(pady=20, padx=20)

    # List all Python scripts from all subdirectories in the plotting folder
    for subdir, _, files in os.walk(PLOTTING_DIR):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                relative_path = os.path.relpath(os.path.join(subdir, file), PLOTTING_DIR)
                listbox.insert(tk.END, relative_path)

    btn = tk.Button(root, text="Display Graph", command=lambda: display_graph(listbox))
    btn.pack(pady=20)

    root.mainloop()

def display_graph(listbox):
    selected_file = listbox.get(tk.ACTIVE)
    if not selected_file:
        return

    # Convert the file path to module path.
    # E.g. "peaks/graph_test.py" -> "script.plotting.peaks.graph_test"
    module_path = "scripts.plotting." + selected_file.replace(os.sep, '.').rstrip('.py')

    # Dynamically import the module using the module path
    plot_module = importlib.import_module(module_path)

    fig = plot_module.plot_graph()

    # Embed the figure in the tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas.draw()

if __name__ == "__main__":
    run_gui()
