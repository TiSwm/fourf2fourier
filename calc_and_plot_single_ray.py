import numpy as np
import matplotlib.pyplot as plt

from rayoptics.environment import trace
from projection_optics import get_rayoptics_model as get_pob


pob_model = get_pob()
dists = np.array([0., 28.17, 12., 2., 22.0, 150., 5.7, 2.2, 172.071])
z_for_drawing = np.cumsum(dists)

object_point = np.array([0.0, 0., 0.])
object_dir = np.array([0.01, 0., 1.])
wavelength_nm = 550

raytrace_data = trace(pob_model, object_point, object_dir, wavelength_nm)
raytrace_data.op
raytrace_data.wvl

n_steps = len(raytrace_data.ray)
assert n_steps == len(z_for_drawing)

r_of_z = np.zeros((len(z_for_drawing), 3))
for i, ray in enumerate(raytrace_data.ray):
    r = ray[0]
    k = ray[1]
    r_of_z[i] = r

fig, ax = plt.subplots()
ax.plot(z_for_drawing + r_of_z[:,2], r_of_z[:,0])
# ax.set_aspect("equal")
ax.set_xlabel("z / mm")
ax.set_ylabel("x / mm")
ax.set_title("Raytrace of a single ray through the 4f system")
plt.show()
