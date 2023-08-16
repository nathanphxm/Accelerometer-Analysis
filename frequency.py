import datetime

month = 2
day = 15
hour = 23

def read_file(filename):
    with open(filename,'r') as file:
        lines = file.readlines()
        formatted_data = [['Year','Month','Day','Hour','Minutes','Index','X','Y','Z']]
        for line in lines:
            col = line.strip().split(',')
            unix_timestamp = int(col[0])
            timestamp = datetime.datetime.fromtimestamp(unix_timestamp)
            
            year = timestamp.year
            month = timestamp.month
            day = timestamp.day
            hour = timestamp.hour
            minutes = timestamp.minute
            
            formatted_line = [year, month, day, hour, minutes] + col[1:]
            formatted_data.append(formatted_line)
        #print(formatted_data[0:25])
    return formatted_data

def get_month_data(month):
    this_month_data = [['Day','Hour','Minutes','Index','X','Y','Z']]
    data  = read_file('./resources/file007_clean.txt')
    for line in data[1:]:
        if line[1] == month:
            this_month_data.append(line[2:])
    #print(this_month_data[0:25])
    return this_month_data

def get_day_data(day):
    this_day_data = [['Hour','Minutes','Index','X','Y','Z']]
    data  = get_month_data(month)
    for line in data[1:]:
        if line[0] == day:
            this_day_data.append(line[1:])
    #print(this_day_data[0:25])
    return this_day_data

def get_hour_data(hour):
    this_hour_data = [['Minutes','Index','X','Y','Z']]
    data  = get_day_data(day)
    #print(data[0:10])
    for line in data[1:]:
        if line[0] == hour:
            this_hour_data.append(line[1:])
    #print(this_hour_data)
    return this_hour_data

def frequency_x_per_hour(hr):
    data = get_hour_data(hr)
    previous_x = None
    frequency = 0
    for line in data[1:]:
        if previous_x is None:
            previous_x = int(line[2])
        elif abs(int(line[2]) - int(previous_x)) >= 10:
            frequency += 1
        previous_x = line[2]
    #print(data[0:10])
    #print(previous_x)
    #print(hour,':00', "frequency of movement",frequency)
    return frequency

def frequency_x_per_day():
    x_frequency = [["Hour","Frequency of movement in x-axis"]]
    for hr in range(25):
        x_frequency.append([hr,frequency_x_per_hour(hr)])
    #print(x_frequency)
    return x_frequency

#frequency_x_per_day()
#read_file('./resources/file007_clean.txt')