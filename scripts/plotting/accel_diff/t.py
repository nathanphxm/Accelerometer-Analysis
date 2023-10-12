import matplotlib.pyplot as plt

x = [0,1,2,3,4]
y = [0,1,2,3,4]

opacity = 0.5
colors = {
    'blue':   [55,  126, 184],  #377eb8 
    'orange': [255, 127, 0],    #ff7f00
    'green':  [77,  175, 74],   #4daf4a
    'pink':   [247, 129, 191],  #f781bf
    'brown':  [166, 86,  40],   #a65628
    'purple': [152, 78,  163],  #984ea3
    'gray':   [153, 153, 153],  #999999
    'red':    [228, 26,  28],   #e41a1c
    'yellow': [222, 222, 0]     #dede00
} 

c_str = {k:f'rgba({v[0]},{v[1]},{v[2]},{opacity})'
         for (k, v) in colors.items()}

print(c_str['blue'])
plt.plot(x,y)
plt.fill_between(x,0,4, color = "#FFB000", alpha = 0.2)

plt.show()

