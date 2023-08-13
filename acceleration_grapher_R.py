""" A function used to graph acceleration from a cleaned sheep data text file, using R in python.
"""
# Requires the rpy2 library to be installed, you can use the following command:
```python
pip install rpy2
```

import rpy2.robjects as robjects

def acceleration_grapher(filename):
    'Returns an acceleration graph using R, given a file of sheep accelerometer data'
    r = robjects.r
    # Acceleration on y-axis
    y = robjects.FloatVector()
    read_csv = robjects.r('read.csv')
    sheep = read_csv(filename)
    euclid.dist <- function(x1, x2) sqrt(sum((x1 - x2) ^ 2))
    previous_point <- c(sheep[1])
    for (i in sheep) {
        y = append(y, euclid.dist(previous_point, i))
        previous_point <- i
    }
    # Time on x-axis
    x = robjects.IntVector(0:len(y))
    # Plotting using R
    r.plot(x, y, type="l", main="Acceleration of filename", xlab="Time", ylab="Acceleration", col="deeppink")