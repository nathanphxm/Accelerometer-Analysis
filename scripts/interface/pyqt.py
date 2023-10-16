import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "processing"))
import importlib
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QWidget, QFileDialog, QLabel, QComboBox, QHBoxLayout, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt
from process_data import process_directory
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class Canvas(FigureCanvas):
    def __init__(self, parent=None):
        fig = plt.figure(figsize=(5, 4), dpi=100)
        
        super(Canvas, self).__init__(fig)
        self.ax = self.figure.add_subplot(111)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def plot(self, fig):
        self.figure.clear()
        new_ax = fig.gca()
        self.ax = self.figure.add_axes(new_ax.get_position(), projection=new_ax.name)
        self.ax.figure = self.figure
        self.figure.axes.append(self.ax)
        self.ax.clear()

        for line in new_ax.lines:
            self.ax.add_line(line)
        self.ax.set_title(new_ax.get_title())
        self.ax.set_xlabel(new_ax.get_xlabel())
        self.ax.set_ylabel(new_ax.get_ylabel())
        self.ax.set_xlim(new_ax.get_xlim())
        self.ax.set_ylim(new_ax.get_ylim())
        self.ax.legend(loc='best')
        self.draw()

    def set_figure(self, fig):
        self.figure = fig
        self.draw()

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # UI setup
        self.setWindowTitle('PyQt App')
        self.setGeometry(100, 100, 800, 600)

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.layout = QVBoxLayout()
        self.buttons_layout = QHBoxLayout()

        self.loading_label = QLabel("Please load data...", self)
        self.loading_label.setAlignment(Qt.AlignCenter)

        self.load_data_button = QPushButton("Load Data", self)
        self.load_data_button.clicked.connect(self.load_data)

        # Create four buttons with the specified labels
        self.button1 = QPushButton("Start Time", self)
        self.button2 = QPushButton("End Time", self)
        self.button3 = QPushButton("Display Graph", self)
        self.button4 = QPushButton("Print Data", self)

        # Add buttons to horizontal layout
        self.buttons_layout.addWidget(self.button1)
        self.buttons_layout.addWidget(self.button2)
        self.buttons_layout.addWidget(self.button3)
        self.buttons_layout.addWidget(self.button4)

        # Create a dropdown box with placeholder
        self.dropdown = QComboBox(self)
        self.dropdown.addItem("Select Graph Type")  # Default placeholder item
        self.populate_graph_scripts()

        # Initially hide the buttons and dropdown
        self.button1.hide()
        self.button2.hide()
        self.button3.hide()
        self.button4.hide()
        self.dropdown.hide()

                # Add Matplotlib Canvas
        self.canvas = Canvas(self)
        self.layout.addWidget(self.canvas)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout.addWidget(self.toolbar)

        self.button3.clicked.connect(self.display_graph)
        self.button4.clicked.connect(self.print_data)

        # UI setup adjustments
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas, 1)  # This will allow the canvas to expand and take available space
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.loading_label, alignment=Qt.AlignCenter)  # Moved label just above combobox
        self.layout.addWidget(self.dropdown)
        self.layout.addLayout(self.buttons_layout)
        self.layout.addWidget(self.load_data_button, alignment=Qt.AlignBottom)

        self.main_widget.setLayout(self.layout)

    def populate_graph_scripts(self):
        # Assuming the plotting directory is on the same level as interface and one directory up from current script
        plotting_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "plotting")

        # For each subdirectory in plotting, find python files
        self.graph_scripts = {}
        for subdir in os.listdir(plotting_dir):
            sub_path = os.path.join(plotting_dir, subdir)
            if os.path.isdir(sub_path):
                for file in os.listdir(sub_path):
                    if file.endswith('.py'):
                        script_name = os.path.splitext(file)[0]
                        self.graph_scripts[script_name] = os.path.join(sub_path, file)
                        self.dropdown.addItem(script_name)

    def load_data(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            try:
                self.loading_label.setText(f"Current Directory: {directory}")
                
                # Call the process_directory function and store the result in self.data
                self.accel_data, self.gps_data = process_directory(directory)

                # Show the buttons and dropdown when a directory is loaded
                self.button1.show()
                self.button2.show()
                self.button3.show()
                self.button4.show()
                self.dropdown.show()

            except Exception as e:
                self.loading_label.setText(f"An error occurred: {str(e)}")
    
    def display_graph(self):
        selected_script = self.dropdown.currentText()
        if selected_script and hasattr(self, 'accel_data') and self.accel_data is not None:
            # Import the module dynamically and call the plot_graph function with data
            script_path = self.graph_scripts[selected_script]
            spec = importlib.util.spec_from_file_location(selected_script, script_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            fig = module.plot_graph(self.accel_data)
            
            # Update Canvas with the new figure
            self.canvas.set_figure(fig)

            # Remove the existing toolbar
            if hasattr(self, "toolbar"):
                self.layout.removeWidget(self.toolbar)
                self.toolbar.deleteLater()
                self.toolbar = None
            
            # Create and add a new toolbar linked with the updated Canvas
            self.toolbar = NavigationToolbar(self.canvas, self)
            self.layout.insertWidget(2, self.toolbar)

    def print_data(self):
        if hasattr(self, 'accel_data') and self.accel_data is not None:
            print(self.accel_data[0])
            print(self.accel_data[-1])
        else:
            print("No data loaded.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = AppWindow()
    mainWin.show()
    sys.exit(app.exec_())
