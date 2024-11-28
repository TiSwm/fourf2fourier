import numpy as np
import matplotlib.pyplot as plt

from rayoptics.environment import trace
from projection_optics import get_rayoptics_model as get_pob

NA = 0.12
pob_model = get_pob(NA=NA)

n_rays = 50
x_range = np.linspace(0., 0.62)
k_range = np.linspace(-NA, NA, n_rays)
fig, ax = plt.subplots()
for x0 in np.linspace(0., 0.62, 32):
    target = np.zeros((n_rays, 3))
    for i, k in enumerate(k_range):
        data = trace(pob_model, np.array([x0, 0., 0.]), np.array([k, 0., 1]), 550)
        target[i] = data[0][-1][0]
    if np.isclose(x0 % 0.1, 0.):
        ax.plot(k_range, target[:,0], label=f"x0={x0}")
    else:
        ax.plot(k_range, target[:,0])
ax.legend()
ax.set_xlabel("sin(start ray angle)")
ax.set_ylabel("intersection in image plane")
plt.show()
