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

time_updated = []
#print(time[0:5])
for e in range(len(time)):
    time[e] = time[e].split(",")[0]
    time[e] = int(time[e].replace("*",""))


for e in range(len(data)):
    data[e] = data[e].split(",")[:3]
    for num in range(len(data[e])):
        data[e][num] = int(data[e][num])
    
time = np.linspace(time[0],time[-1],len(data))
time = pd.DataFrame(time)
data = pd.DataFrame(data)

time = time.rename(columns={0: "Time"})
data = data.rename(columns={0: "x", 1: "y", 2: "z"})

print(time.head(5))
print(time.tail(5))
print(data.tail(5))

# fig, axs = plt.subplots(3)
# fig.suptitle('Accelerometer movement in 3 axises')
# axs[0].plot(time,data["x"])
# axs[0].set_title('X-axis')
# axs[1].plot(time,data["y"])
# axs[1].set_title('Y-axis')
# axs[2].plot(time,data["z"])
# axs[2].set_title('Z-axis')

plt.plot(time,data["x"])
plt.plot(time,data["y"])
plt.plot(time,data["z"])        
plt.show()

#speed
dt = time[1]-time[0]
