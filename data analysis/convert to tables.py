import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file = pd.read_table("file007.txt",header=None)
df = pd.DataFrame(file)
time = []
data = []

print(df[0][2])
for i in df[0]:
    if("*" in i):
        time.append(i)
    else:
        data.append(i)

for e in range(len(time)):
    time[e] = time[e].split(",")[0]
    time[e] = int(time[e].replace("*",""))


for e in range(len(data)):
    data[e] = data[e].split(",")[:3]
    for num in range(len(data[e])):
        data[e][num] = int(data[e][num])
    
time = np.linspace(time[0],time[-1],len(data))

x = []
y = []
z = []
for element in data:
    x.append(element[0])
    y.append(element[1])
    z.append(element[2])

time = pd.DataFrame(time)
x = pd.DataFrame(x)
y = pd.DataFrame(y)
z = pd.DataFrame(z)

joined = pd.concat([x,y],axis=1)
joined = pd.concat([joined,z],axis=1)
joined = pd.concat([joined,time],axis=1)

joined = joined.rename(columns={0: "x", 1: "y", 2: "z", 3:"Time"})
x.to_csv("x-axis.csv")
y.to_csv("y-axis.csv")
z.to_csv("z-axis.csv")
time.to_csv("time.csv")
joined.to_csv("data007.csv")
