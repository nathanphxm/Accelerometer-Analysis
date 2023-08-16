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

# fig, axs = plt.subplots(3)
# fig.suptitle('Accelerometer movement in 3 axises')
# axs[0].plot(time,x)
# axs[0].set_title('X-axis')
# axs[1].plot(time,y)
# axs[1].set_title('Y-axis')
# axs[2].plot(time,z)
# axs[2].set_title('Z-axis')

# plt.plot(time,x)
# plt.plot(time,y)
# plt.plot(time,z)
# plt.show()

# dt = time[1] - time[0]
# vx = [0]
# vy = [0]
# vz = [0]

# for i in np.arange(len(time)-1):
#     vx = vx + [vx[-1] + x[i]*dt]
#     vy = vy + [vy[-1] + y[i]*dt]
#     vz = vz + [vz[-1] + z[i]*dt]

# plt.plot(time,vx)
# plt.show()

#length of sample
sample_rate = len(time)

def plot_fft(time,axis,sample_rate,direction):
    # This returns the fourier transform coeficients as complex numbers
    transformed_axis = np.fft.fft(axis)

    # Take the absolute value of the complex numbers for magnitude spectrum
    freqs_magnitude = np.abs(transformed_axis)

    # Create frequency x-axis that will span up to sample_rate
    freq_axis = np.linspace(0, sample_rate, len(freqs_magnitude))

    # Plot frequency domain
    plt.plot(freq_axis, freqs_magnitude)
    plt.title("FFT of "+direction)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.xlim(0, 100)
    plt.show()

plot_fft(time,x,sample_rate,"x")
plot_fft(time,y,sample_rate,"y")
plot_fft(time,z,sample_rate,"z")
