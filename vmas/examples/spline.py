import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import splprep, splev

# Data
data_points = [(-5.0, 4.0), (-5.0, 3.0), (-5.0, 2.0), (-5.0, 1.0), (-5.0, 0.0), 
               (-5.0, -1.0), (-5.0, -2.0), (-4.0, -2.0), (-3.0, -2.0), 
               (-2.0, -2.0), (-1.0, -2.0)]

x, y = zip(*data_points)

# Parametric spline
tck, u = splprep([x, y], s=0.05)
u_fine = np.linspace(0, 1, 1000)
x_smooth, y_smooth = splev(u_fine, tck)


# Plot
plt.plot(x, y, 'o', label='Data')
plt.plot(x_smooth, y_smooth, '-', label='Spline')
plt.legend()
plt.axis("equal")
plt.show()