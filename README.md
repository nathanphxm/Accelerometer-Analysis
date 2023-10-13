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

