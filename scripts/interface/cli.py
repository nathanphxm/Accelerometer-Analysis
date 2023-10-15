import os, sys, csv

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "processing"))
from process_data import process_directory
from process_data import process_file

def load_data_dir(dir):
    # strip whitespace from end of directory name
    dir = dir.replace('\\', '').rstrip()
    accelerometer_data, gps_data = process_directory(dir)
    choice = input("[P]rint data to console, [E]xport data to CSV, [R]eturn to menu or e[X]it? ").lower()

    if choice == "p":
        print_type = input("[A]ccelerometer data only, [G]PS data only, or [B]oth? ").lower()
        
        if print_type == "a":
            print(accelerometer_data)
        if print_type == "g":
            print(gps_data)
        if print_type == "b":
            print(accelerometer_data)
            print(gps_data)
    if choice == "e":
        base_filename = dir.split("/")[-1]
        export_type = input("[A]ccelerometer data only or [G]PS data only? ").lower()
        
        if export_type == "a":
            print("Exporting accelerometer data...")
            filename = base_filename + "_accel.csv"
            with open(filename, "w") as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "Interval", "ACCEL_X", "ACCEL_Y", "ACCEL_Z"])
                writer.writerows(accelerometer_data)
            print("Exported accelerometer data to " + filename)
            sys.exit()
        if export_type == "g":
            print("Exporting GPS data...")
            filename = base_filename + "_gps.csv"
            with open(filename, "w") as file:
                writer = csv.writer(file)
                writer.writerow(["Latitude", "Longitude", "Day", "Month", "Year", "Hour", "Minute", "Second"])
                writer.writerows(gps_data)
            print("Exported GPS data to " + filename)
            sys.exit()
    if choice == "r":
        run_cli()
    if choice == "x":
        sys.exit()
            
    
def load_data_file(file):
    print("Analysing file: " + file)
    accelerometer_data, gps_data = process_file(file)
    choice = input("[P]rint data to console, [E]xport data to CSV, [R]eturn to menu or e[X]it? ").lower()

    if choice == "p":
        print_type = input("[A]ccelerometer data only, [G]PS data only, or [B]oth? ").lower()
        
        if print_type == "a":
            print(accelerometer_data)
        if print_type == "g":
            print(gps_data)
        if print_type == "b":
            print(accelerometer_data)
            print(gps_data)
    if choice == "e":
        base_filename = file.split("/")[-1].split(".")[0]
        export_type = input("[A]ccelerometer data only or [G]PS data only? ").lower()
        
        if export_type == "a":
            print("Exporting accelerometer data...")
            filename = base_filename + "_accel.csv"
            with open(filename, "w") as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "Interval", "ACCEL_X", "ACCEL_Y", "ACCEL_Z"])
                writer.writerows(accelerometer_data)
            print("Exported accelerometer data to " + filename)
            sys.exit()
        if export_type == "g":
            print("Exporting GPS data...")
            filename = base_filename + "_gps.csv"
            with open(filename, "w") as file:
                writer = csv.writer(file)
                writer.writerow(["Latitude", "Longitude", "Day", "Month", "Year", "Hour", "Minute", "Second"])
                writer.writerows(gps_data)
            print("Exported GPS data to " + filename)
            sys.exit()
    if choice == "r":
        run_cli()
    if choice == "x":
        sys.exit()


def run_cli():
    print("Welcome to the CLI interface for the Sheep Tracker project.")
    print("----------------------------------------")
    print("[D]irectory analysis")
    print("[F]ile analysis")
    print("[E]xit")
    print("----------------------------------------")
    choice = input("Choose an option: ").lower()
    
    if choice == "d":
        dir = input("Enter the directory to analyse: ").strip("'")
        load_data_dir(dir)
    if choice == "f":
        file = input("Enter the full path to the file for analysis: ").strip("'")
        load_data_file(file)
    if choice == "e":  
        sys.exit()
    else:
        print("\nInvalid option - please enter a valid value. Returning to menu.\n")
        run_cli()
    

if __name__ == "__main__":
    run_cli()