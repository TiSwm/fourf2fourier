import numpy as np
import matplotlib.pyplot as plt

from projection_optics import get_rayoptics_model as get_pob
from raytrace_functions import calc_contrast, mtf_guess

shifts = np.linspace(-.1, .1, 60)
contrast_at_50um = np.zeros_like(shifts)

fig, ax = plt.subplots()
for i, shift in enumerate(shifts):
    sm = get_pob(shift)
    contrast_at_50um[i] = calc_contrast(sm, 1e-3)
    if i % 6 == 0:
        ax.plot(*mtf_guess(sm), label=f"shift 1st Lens: {np.around(shift * 1e3, 1)}um")
ax.set_xlabel("structure pitch / um")
ax.set_ylabel("ray optical contrast")
ax.legend()
plt.show()

fig, ax = plt.subplots()
ax.plot(1e3 * shifts, contrast_at_50um)
ax.set_xlabel("shift 1st Lens / um")
ax.set_ylabel("ray optical contrast @ pitch=1um")
ax.legend()
plt.show()


shifts = np.linspace(-2, 2, 60)
contrast_at_50um = np.zeros_like(shifts)

fig, ax = plt.subplots()
for i, shift in enumerate(shifts):
    sm = get_pob(0., shift)
    contrast_at_50um[i] = calc_contrast(sm, 1e-3)
    if i % 6 == 0:
        ax.plot(*mtf_guess(sm), label=f"shift 2nd Lens: {np.around(shift, 1)}mm")
ax.set_xlabel("structure pitch / um")
ax.set_ylabel("ray optical contrast")
ax.legend()
plt.show()

fig, ax = plt.subplots()
ax.plot(shifts, contrast_at_50um)
ax.set_xlabel("shift 2nd Lens / mm")
ax.set_ylabel("ray optical contrast @ pitch=1um")
plt.show()
