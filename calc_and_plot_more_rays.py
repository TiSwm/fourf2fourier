import numpy as np
import matplotlib.pyplot as plt

from rayoptics.environment import trace
from projection_optics import get_rayoptics_model as get_pob


pob_model = get_pob()
dists = np.array([0., 28.17, 12., 2., 22.0, 150., 5.7, 2.2, 172.071])
z_for_drawing = np.cumsum(dists)

object_points = np.zeros((10, 3))
object_dirs = np.zeros((10, 3))
object_dirs[:,2] = 1.
# # pupil raytrace
# object_dirs[:,0] = np.linspace(0., 0.1, 10)
# field raytrace
object_points[:,0] = np.linspace(0., 0.1, 10)

wavelength_nm = 550
n_rays = len(object_points)

r_of_z = np.zeros((n_rays, len(z_for_drawing), 3))
for ray_idx in range(n_rays):
    raytrace_data = trace(pob_model, object_points[ray_idx], object_dirs[ray_idx], wavelength_nm)
    n_steps = len(raytrace_data.ray)
    assert n_steps == len(z_for_drawing)

    for i, ray in enumerate(raytrace_data.ray):
        r = ray[0]
        k = ray[1]
        r_of_z[ray_idx, i] = r


fig, ax = plt.subplots()
for ray in range(n_rays):
    ax.plot(z_for_drawing + r_of_z[ray,:,2], r_of_z[ray,:,0])

ax.set_xlabel("z / mm")
ax.set_ylabel("x / mm")
ax.set_title("Raytrace of a bundle of rays in the 4f system")
plt.show()
