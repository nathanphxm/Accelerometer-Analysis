import datetime

month = 2
day = 15
hour = 23
minute = 1
second = 1

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
            seconds = timestamp.second
            
            formatted_line = [year, month, day, hour, minutes,seconds] + col[1:]
            formatted_data.append(formatted_line)
        #print(formatted_data[0:25])
    return formatted_data

file_data  = read_file('./resources/file007_clean.txt')

def get_month_data(month):
    this_month_data = [['Day','Hour','Minutes','Seconds','Index','X','Y','Z']]
    for line in file_data[1:]:
        if line[1] == month:
            this_month_data.append(line[2:])
    #print(this_month_data[0:25])
    return this_month_data

def get_day_data(month, day):
    this_day_data = [['Hour','Minutes','Seconds','Index','X','Y','Z']]
    data  = get_month_data(month)
    for line in data[1:]:
        if line[0] == day:
            this_day_data.append(line[1:])
    #print(this_day_data[0:25])
    return this_day_data

def get_hour_data(month, day, hour):
    this_hour_data = [['Minutes','Seconds','Index','X','Y','Z']]
    data  = get_day_data(month, day)
    #print(data[0:10])
    for line in data[1:]:
        if line[0] == hour:
            this_hour_data.append(line[1:])
    #print(this_hour_data)
    return this_hour_data

def get_minute_data(month, day, hour, minute):
    this_minute_data = [['Seconds','Index','X','Y','Z']]
    data  = get_hour_data(month, day, hour)
    #print(data[0:10])
    for line in data[1:]:
        if line[0] == minute:
            this_minute_data.append(line[1:])
    #print(this_minute_data)
    return this_minute_data

def get_second_data(month, day, hour, minute, second):
    this_second_data = [['Index','X','Y','Z']]
    data  = get_minute_data(month, day, hour, minute)
    #print(data[0:10])
    for line in data[1:]:
        if line[0] == second:
            this_second_data.append(line[1:])
    #print(this_second_data)
    return this_second_data


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

def frequency_x_per_second(month, day, hour, minute, second):
    data = get_second_data(month, day, hour, minute, second)
    previous_x = None
    frequency = 0
    for line in data[1:]:
        x = line[1]
        if previous_x is None:
            previous_x = int(x)
        elif abs(int(x) - int(previous_x)) >= 10:
            frequency += 1
        previous_x = x
    #print(data[0:10])
    #print(previous_x)
    print(month, day, hour, minute, second)
    #print(hour,':00', "frequency of movement",frequency)
    return frequency

def frequency_x_per_hour_by_second(month, day):
    x_frequency = [["Time","Frequency of movement in x-axis"]]
    for min in range (60):
        for sc in range(60):
            x_frequency.append([str(month)+'/'+str(day)+' '+str(hour)+':'+str(min)+':'+str(sc),frequency_x_per_second(month, day, hour, min, sc)])
    print(x_frequency)
    return x_frequency
frequency_x_per_hour_by_second(month, day)


def frequency_x_per_day():
    x_frequency = [["Hour","Frequency of movement in x-axis"]]
    for hr in range(24):
        x_frequency.append([hr,frequency_x_per_hour(hr)])
    #print(x_frequency)
    return x_frequency

#frequency_x_per_day()
#read_file('./resources/file007_clean.txt')

def frequency_y_per_hour(hr):
    data = get_hour_data(hr)
    previous_y = None
    frequency = 0
    for line in data[1:]:
        if previous_y is None:
            previous_y = int(line[3])
        elif abs(int(line[3]) - int(previous_y)) >= 10:
            frequency += 1
        previous_y = line[3]
    return frequency

def frequency_y_per_day():
    y_frequency = [["Hour","Frequency of movement in y-axis"]]
    for hr in range(25):
        y_frequency.append([hr,frequency_y_per_hour(hr)])
    return y_frequency

def frequency_z_per_hour(hr):
    data = get_hour_data(hr)
    previous_z = None
    frequency = 0
    for line in data[1:]:
        if previous_z is None:
            previous_z = int(line[4])
        elif abs(int(line[4]) - int(previous_z)) >= 10:
            frequency += 1
        previous_z = line[4]
    return frequency

def frequency_z_per_day():
    z_frequency = [["Hour","Frequency of movement in z-axis"]]
    for hr in range(25):
        z_frequency.append([hr,frequency_z_per_hour(hr)])
    return z_frequency