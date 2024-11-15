import numpy as np
import matplotlib.pyplot as plt

np.exp(-np.square(50 / 32.23) / 2)

x = np.linspace(-90, 90)
y = np.exp(-np.square(x / 32.23) / 2)

fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()

theta = x * (2 * np.pi) / 360

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.plot(theta, y)
ax.set_rmax(1.1)
ax.set_rticks([0.5, 1.])  # Less radial ticks
ax.set_rlabel_position(+45.)  # Move radial labels away from plotted line
ax.grid(True)

ax.set_title("A line plot on a polar axis", va='bottom')
plt.show()
