import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

xy = (np.random.random((1000, 2)) - 0.5).cumsum(axis=0)
print(xy)
# Reshape things so that we have a sequence of:
# [[(x0,y0),(x1,y1)],[(x0,y0),(x1,y1)],...]
xy = xy.reshape(-1, 1, 2)
segments = np.hstack([xy[:-1], xy[1:]])
print(segments)

fig, ax = plt.subplots()
coll = LineCollection(segments, cmap=plt.cm.gist_ncar)
coll.set_array(np.random.random(xy.shape[0]))

ax.add_collection(coll)
ax.autoscale_view()

plt.show()