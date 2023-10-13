# Accelerometer data analysis and visualisation software suite
Created for CITS3200 2023 Semester 2 with love from Group 6.


## Installing prerequisites

- Windows (tested on 10? 11?), macOS (tested on 13.x Ventura and 14.x Sonoma), Linux (tested on Ubuntu xx.xx.x)
- Python 3 (tested on 3.9.x, 3.11.x, TBA)
- tkinter (for graphical interfaces)
- matplotlib (for graphing)

*Specific versions of software are not required unless specified; anything noted with an **x** can be treated as any number.*

### macOS
**1. Ensure that Python 3.x is installed on the machine.**
In Terminal, or your favourite terminal emulator:
```bash
$ python3 --version
Python 3.xx.x
```

**2. Ensure next that `pip` is installed on the machine.**

```bash
$ pip3 --version
pip 23.2.1 from [...]
```
if the above does not work, try:
```bash
$ python3 -m pip --version
pip 23.2.1 from [...]
```

If `pip` is not installed:

```bash
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```

```bash
$ python3 get-pip.py
```

**3. Ensure next that `git` is installed on the machine.**
```bash
$ git --version
git version 2.xx.x (Apple Git-xxx)
```

If git is not installed, a window will display prompting you to install the _command line developer tools_. Install it from within that window.
![Window displaying command line developer tools install prompt](https://user-images.githubusercontent.com/8599/195653334-7fde0a5e-1168-4be4-b3a2-313c6bb836b8.png)

### Linux
In Terminal, or your favourite terminal emulator:
**1. Ensure that Python 3.x is installed on the machine.**
```bash
$ python3 --version
Python 3.xx.x
```

**2. Ensure next that `pip` is installed on the machine.**

```bash
$ pip3 --version
pip 23.2.1 from [...]
```

If `pip` is not installed:

```bash
$ sudo apt-get update && sudo apt-get upgrade -y
$ sudo apt-get install python3-pip -y
```
**2. Ensure next that `git` is installed on the machine.**
```bash
$ git --version
$ 
```

### Windows
In Terminal, or your favourite terminal emulator (Command Prompt may work!):
**1. Ensure that Python 3.x is installed on the machine.**
```powershell
$ python3 --version
Python 3.xx.x
```
Note: If Python 3.x is not currently installed on the system, a Microsoft Store window will open. Install it from that window.

## Installing the software

### macOS

1. Create an empty folder where you would like to store the program.
2. Launch `Terminal` on your machine, and `cd` into that directory:
```bash
$ cd <path/to/dir>
```
*To make it easier, you can do this:*

![Drag a folder into a terminal window to reveal its path](https://github.com/nathanphxm/Accelerometer-Analysis/blob/4862fac1fc564749b92ba0f82d849cf0e2dd8cd6/docs/drag-for-path.gif)

3. Clone the repository into that folder

```bash
$ git clone https://github.com/nathanphxm/Accelerometer-Analysis
```

4. Install prerequisite Python packages

```bash
$ pip3 install -r requirements.txt
```
if the above does not work, try:
```bash
$ python3 -m pip install -r requirements.txt
```

### Linux

1. Create an empty folder where you would like to store the program.
2. Launch `Terminal` on your machine, and `cd` into that directory:
```bash
$ cd <path/to/dir>
```
3. Clone the repository into that folder
```bash
$ git clone https://github.com/nathanphxm/Accelerometer-Analysis
```
4. Install prerequisite Python packages
```bash
$ pip3 install -r requirements.txt
```


### Windows



## Using the software

With the application directory open in a terminal window:

```bash
$ python3 start.py
Do you want to use the GUI or CLI? (gui/cli):
```

Choose an option by typing it in the prompt. 

#### Using the graphical user interface:
1. Click "Load Data" and select the folder containing data you want to be analysed and visualised.
2. Click "Set Start Date & Time" and "Set End Date & Time" to select the timeframe and click "OK".
3. From the drop-down list, select the code respective to the graph you want to see.
4. Click "Print Data" to get the cleaned csv file.
5. Click "Display Graph" to show graph.

#### Using the command-line interface:

```bash
Do you want to use the GUI or CLI? (gui/cli): cli
Welcome to the CLI interface for the Sheep Tracker project.
----------------------------------------
[D]irectory analysis
[F]ile analysis
[E]xit
----------------------------------------
Choose an option:
```

Choose an option by entering `d` for directory analysis, `f` for individual file analysis or `e` to exit.

**Entering path for analysis:**

Similar to above, you can drag in a folder or an individual file into the prompt.

![Drag a folder worth of data into the prompt](https://github.com/nathanphxm/Accelerometer-Analysis/blob/f5564f394473758a5b7e6434a34b5d2e19121c6d/docs/drag-for-path-2.gif)



## Data visualisation

### Activity level based on frequency of movement (interface_activity_freq.py)
[Approx running time: less than 10 seconds, if it takes longer than this, it might be an error in data file.] 

Sample graph: Activity level on cumulative frequency graph (24 hours) 

This graph show you the activity level (low, moderate, high) of sheep based on its frequency of movement per minute, in addition to a line showing its cumulative frequency for reference.

Running this code in GUI will also output a "output.csv" file containing 'Datetime', 'Frequency per Minute', 'Activity Level' for the period selected to your directory folder.

![Sample output for 24 hours](./sample_demo_gui/Activity%20level%20on%20cumulative%20frequency%20graph%20(24%20hours).jpeg)

Threshold values are adjustable in the python code (line 15, 16) to determine the categorisation of activity level.

Frequency threshold value is adjustable in the python code (line 19) to determine how large the difference between x(t),y(t),z(t) and x(t+1),y(t+1),z(t+1) is needed to detect a movement calculating into frequency. Frequecny will be added into that minute if either of the axes has a difference of the threshold value you set (e.g. in the sample case, is a difference of 10).

![Adjustable threshold in python code](./sample_demo_gui/Activity%20Freq%20code.png)

By adjusting the timeframe in GUI, you can select certain hour to visualise the data (e.g. in this case is 4 hours).

Sample graph: Activity level on cumulative frequency graph (4 hours) 
![Sample output for 4 hours](./sample_demo_gui/Activity%20level%20on%20cumulative%20frequency%20graph%20(4%20hours).jpeg)

### Frequency of movement per minute (interface_freq.py)
[Approx running time: less than 5 seconds, if it takes longer than this, it might be an error in data file.]

Sample graph: Frequency per minute graph (24 hours) 

This graph show you the total activity of the sheep per minute (frequency of movement), based on the difference between each movement at timestamp(0) and timestamp(1).

![Sample output for 24 hours](./sample_demo_gui/Frequency%20per%20minute%20(24%20hours).png)

Frequency threshold value is adjustable in the python code (line 12) to determine how large the difference between x(t),y(t),z(t) and x(t+1),y(t+1),z(t+1) is needed to detect a movement calculating into frequency. Frequency will be added into that minute if either of the axes has a difference of the threshold value you set (e.g. in the sample case, is a difference of 10).

![Adjustable threshold in python code](./sample_demo_gui/Freq%20code.png)

By adjusting the timeframe in GUI, you can select certain hour to visualise the data (e.g. in this case is 4 hours).

Sample graph: Frequency per minute graph (4 hours) 
![Sample output for 4 hours](./sample_demo_gui/Frequency%20per%20minute%20(4%20hours).png)

#### Fast Fourier Transform graph (Interface_fft.py)
Runtime: around 10 seconds for 24 hour data

The following figure shows the Fast Fourier Transform graph on the X axis, Y axis, and Z axis data. The FFT plots give a rough idea of the frequency content in the signal. 

In the plot, the x-axis shows varying frequency measured in hertz and y-axis shows the amplitude of the given frequency in the data. Since the data is a time series data, the FFT plot does not give too much information on identifying pattern throughout the time of the day, and is useful just for preliminary analysis of the data to figure out distribution of frequencies intensity in a given timeframe.

![FFT plot output for 24 hours data](https://github.com/nathanphxm/Accelerometer-Analysis/blob/f5564f394473758a5b7e6434a34b5d2e19121c6d/docs/FFT plot.png)




#### Acceleration Difference per sample point(Interface_diff)
Runtime: around 20 second for 24 hour data

The following figure shows an acceleration difference graph for the X axis, Y axis, and Z axis data. Given the accelerometer data xi = x1, x2, .., xn. where n = length of file. The difference of x[i+1] and x[i] is calculated and plotted against the timestamps. The main aim of this plot is to reduce noise from the data, and get a better clarity on the visuals of the data points. Through this plot, a time series analysis can be observed and patterns on data can be inferred.

![accel difference plot output for 24 hours data](https://github.com/nathanphxm/Accelerometer-Analysis/blob/f5564f394473758a5b7e6434a34b5d2e19121c6d/docs/Acceleration Difference.png)

#### Activity highlighting through difference of acceleratioon (Interface_diff_highlights.py)
Runtime: around 1 minute for 24 hour data

Following on the acceleration difference plot, depending on the values of the difference per data point, the rows are categorised into 3 levels: "high activity", "medium activity", and "low activity". The aim of this graph is to give a clear visualisation on how intense the activities of the sheep are throughout the day. In the actual graph, there are sections colored in blue for medium activity and red for high activity. The low activity are not colored, as this over populated the graph with colors, possibly obstructing the interests of the analysis, which is finding the important times when sheep activity peaks. The graph below shows the actual plot of the highlighted graph.

![highlighted acceleration difference plot output for 24 hours data](https://github.com/nathanphxm/Accelerometer-Analysis/blob/f5564f394473758a5b7e6434a34b5d2e19121c6d/docs/Acceleration Difference Highlighted.png)

The threshold of values used for the highlighting can be adjusted in the python scripts by changing the value of the global variable LOW_THRESHOLD and MEDIUM_THRESHOLD in line 12.

![changing threshold value](https://github.com/nathanphxm/Accelerometer-Analysis/blob/f5564f394473758a5b7e6434a34b5d2e19121c6d/docs/Changing Threshold.png)
