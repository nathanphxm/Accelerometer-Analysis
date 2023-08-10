import sys, zlib, os

from datetime import datetime
startTime = datetime.now()

def read_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = f.readlines()
            return data
    except FileNotFoundError:
        print(f"File at {file_path} not found!")
        
def process_file(file_path):
    data = read_file(file_path)
    proc_data = []
    time_index = []
    time = None

    for index, line in enumerate(data):
        if line != "":
            if "*" in line:
                time_index.append(index)
                time = int(line.split(',')[0].strip("*"))
            if "*" not in line:
                line = f"{time},{line}"
        proc_data.append(line)
            
    time_index.reverse()
    
    for index in time_index:
        del proc_data[index]
    
    return proc_data

        
def main():
    if len(sys.argv) != 2:
        print("Usage: script.py <file.txt>")
        return
    
    file_path = sys.argv[1]
    file_name = file_path.split('/')[-1].split('.')[0]
    
    pd = process_file(file_path)
    
    with open(f'../resources/{file_name}_processed.txt', 'w') as pf:
        for line in pd:
            pf.write(line)

    print(datetime.now() - startTime)

if __name__ == "__main__":
    main()