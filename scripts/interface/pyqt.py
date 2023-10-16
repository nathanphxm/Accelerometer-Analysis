import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "processing"))
import importlib
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QWidget, QFileDialog, QLabel, QComboBox, QHBoxLayout, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, QDateTime, QTime
from process_data import process_directory
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from PyQt5.QtWidgets import QCalendarWidget, QSlider, QDialog, QDateEdit, QMessageBox

class DateTimePicker(QDialog):
    def __init__(self, datetime_type, min_datetime, max_datetime, current_datetime, parent=None):
        super(DateTimePicker, self).__init__(parent)
        
        self.setWindowTitle(f"Select {datetime_type} time")
        self.layout = QVBoxLayout()

        self.calendar = QCalendarWidget()
        self.hour_slider = QSlider(Qt.Horizontal)
        self.minute_slider = QSlider(Qt.Horizontal)

        self.hour_label = QLabel()
        self.minute_label = QLabel()

        self.datetime_type = datetime_type
        self.min_datetime = min_datetime
        self.max_datetime = max_datetime
        self.current_datetime = current_datetime
        
        # Setup calendar
        self.calendar.setMinimumDate(self.min_datetime.date())
        self.calendar.setMaximumDate(self.max_datetime.date())
        self.calendar.setSelectedDate(self.current_datetime.date())
        self.calendar.clicked.connect(lambda: self.date_changed(datetime_type))
        
        # Setup hour slider
        self.hour_slider.setRange(0, 23)
        self.hour_slider.setValue(self.current_datetime.time().hour())
        self.hour_slider.valueChanged.connect(lambda: self.hour_changed(datetime_type))
        
        # Setup minute slider
        self.minute_slider.setRange(0, 59)
        self.minute_slider.setValue(self.current_datetime.time().minute())
        self.minute_slider.valueChanged.connect(self.minute_changed)

        # Configure the OK button to set the selected date-time
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        
        # Add widgets to layout
        self.layout.addWidget(self.calendar)
        self.layout.addWidget(self.hour_label)
        self.layout.addWidget(self.hour_slider)
        self.layout.addWidget(self.minute_label)
        self.layout.addWidget(self.minute_slider)
        self.layout.addWidget(ok_button)
        
        self.setLayout(self.layout)
        
        self.adjust_time_bounds(datetime_type)
        self.update_displayed_datetime()
    
    def adjust_time_bounds(self, datetime_type):
        selected_date = self.calendar.selectedDate()
        if datetime_type == "start":
            if selected_date == self.min_datetime.date():
                self.hour_slider.setMinimum(self.min_datetime.time().hour())
            else:
                self.hour_slider.setMinimum(0)
        else:  # "end"
            if selected_date == self.max_datetime.date():
                self.hour_slider.setMaximum(self.max_datetime.time().hour())
            else:
                self.hour_slider.setMaximum(23)
                
        if datetime_type == "start" and selected_date == self.min_datetime.date() and self.hour_slider.value() == self.min_datetime.time().hour():
            self.minute_slider.setMinimum(self.min_datetime.time().minute())
        elif datetime_type == "end" and selected_date == self.max_datetime.date() and self.hour_slider.value() == self.max_datetime.time().hour():
            self.minute_slider.setMaximum(self.max_datetime.time().minute())
        else:
            self.minute_slider.setRange(0, 59)

    def date_changed(self, datetime_type):
        self.adjust_time_bounds(datetime_type)
        self.update_displayed_datetime()

    def hour_changed(self, datetime_type):
        self.adjust_time_bounds(datetime_type)
        self.update_displayed_datetime()

    def minute_changed(self):
        self.update_displayed_datetime()

    def update_displayed_datetime(self):
        selected_date = self.calendar.selectedDate()
        selected_hour = self.hour_slider.value()
        selected_minute = self.minute_slider.value()
        
        self.hour_label.setText(f"Hour: {selected_hour:02}")
        self.minute_label.setText(f"Minute: {selected_minute:02}")

    def get_selected_datetime(self):
        date = self.calendar.selectedDate()
        hour = self.hour_slider.value()
        minute = self.minute_slider.value()

        datetime_obj = QDateTime(date, QTime(hour, minute))
        return datetime_obj

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

        #Button clicks
        self.button1.clicked.connect(lambda: self.set_datetime("start"))
        self.button2.clicked.connect(lambda: self.set_datetime("end"))
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

                # Assuming accel_data timestamps are Unix timestamps and the first column of each row is a timestamp
                start_timestamp = self.accel_data[0][0]
                end_timestamp = self.accel_data[-1][0]

                # Convert Unix timestamps to QDateTime
                self.start_datetime = QDateTime.fromSecsSinceEpoch(start_timestamp)
                self.end_datetime = QDateTime.fromSecsSinceEpoch(end_timestamp)

            except Exception as e:
                print(f"An error occurred: {str(e)}")

    def set_datetime(self, datetime_type):
        # Convert integer timestamp to QDateTime object
        if isinstance(self.accel_data[0][0], int):
            # If timestamp is seconds since the Unix epoch
            start_datetime = QDateTime.fromSecsSinceEpoch(self.accel_data[0][0])
            end_datetime = QDateTime.fromSecsSinceEpoch(self.accel_data[-1][0])
        else:
            # Assuming the first element of each data row is a timestamp string
            start_datetime = QDateTime.fromString(self.accel_data[0][0], "yyyy-MM-dd HH:mm:ss")
            end_datetime = QDateTime.fromString(self.accel_data[-1][0], "yyyy-MM-dd HH:mm:ss")

        # Determine the minimum and maximum allowable datetime based on the other button and the data range
        if datetime_type == "start":
            min_datetime = start_datetime
            max_datetime = QDateTime.fromString(self.button2.text().replace("End Time: ", ""), "yyyy-MM-dd HH:mm:ss") if "End Time:" in self.button2.text() else end_datetime
        else: # end
            max_datetime = end_datetime
            min_datetime = QDateTime.fromString(self.button1.text().replace("Start Time: ", ""), "yyyy-MM-dd HH:mm:ss") if "Start Time:" in self.button1.text() else start_datetime

        if datetime_type == "start":
            current_datetime = self.start_datetime
        elif datetime_type == "end":
            current_datetime = self.end_datetime

        dialog = DateTimePicker(datetime_type, min_datetime, max_datetime, current_datetime, self)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            selected_datetime = dialog.get_selected_datetime()
            if datetime_type == "start":
                # Ensure that the new start time is before the current end time
                current_end_time = QDateTime.fromString(self.button2.text().replace("End Time: ", ""), "yyyy-MM-dd HH:mm:ss") if "End Time:" in self.button2.text() else self.end_datetime
                if selected_datetime >= current_end_time:
                    self.show_warning("Start time must be before the end time!")
                    return
                self.button1.setText(f"Start Time: {selected_datetime.toString('yyyy-MM-dd HH:mm:ss')}")
            else:  # end
                # Ensure that the new end time is after the current start time
                current_start_time = QDateTime.fromString(self.button1.text().replace("Start Time: ", ""), "yyyy-MM-dd HH:mm:ss") if "Start Time:" in self.button1.text() else self.start_datetime
                if selected_datetime <= current_start_time:
                    self.show_warning("End time must be after the start time!")
                    return
                self.button2.setText(f"End Time: {selected_datetime.toString('yyyy-MM-dd HH:mm:ss')}")


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

    def show_warning(self, message):
        """Show a warning message to the user."""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("Warning")
        msg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = AppWindow()
    mainWin.show()
    sys.exit(app.exec_())
