import os
import sys
import tkinter as tk
from tkinter import filedialog, Listbox

PLOTTING_DIR = os.path.join(os.path.dirname(__file__), "..", "plotting")

def run_gui():
    root = tk.Tk()
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

    full_path = os.path.join(PLOTTING_DIR, selected_file)

    # Execute the selected graph script using the current Python interpreter
    os.system(f"{sys.executable} {full_path}")

if __name__ == "__main__":
    run_gui()
