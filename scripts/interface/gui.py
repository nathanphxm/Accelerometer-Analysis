import os
import sys
import tkinter as tk
from tkinter import ttk  # For the Combobox widget
import importlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
        w, h = root.winfo_screenwidth() * 0.8, root.winfo_screenheight() * 0.8
        x, y = (root.winfo_screenwidth() - w) // 2, (root.winfo_screenheight() - h) // 2
        root.geometry(f"{int(w)}x{int(h)}+{int(x)}+{int(y)}")

    root.title("Graph Selection")

    # Create a Combobox
    combobox = ttk.Combobox(root)
    combobox.pack(pady=20, padx=20)

    # Populate Combobox with Python scripts from all subdirectories in the plotting folder
    scripts = []
    for subdir, _, files in os.walk(PLOTTING_DIR):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                relative_path = os.path.relpath(os.path.join(subdir, file), PLOTTING_DIR)
                scripts.append(relative_path)

    combobox['values'] = scripts

    btn = tk.Button(root, text="Display Graph", command=lambda: display_graph(combobox))
    btn.pack(pady=20)

    root.mainloop()


current_canvas = None

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

if __name__ == "__main__":
    run_gui()
