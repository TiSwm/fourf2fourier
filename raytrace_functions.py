import numpy as np

from rayoptics.environment import trace
from projection_optics import get_rayoptics_model as get_pob


def trace_rays_in_system(start_points, start_directions):
    pob_model = get_pob()
    dists = np.array([0., 28.17, 12., 2., 22.0, 150., 5.7, 2.2, 172.071])
    z_for_drawing = np.cumsum(dists)
    wavelength_nm = 550

    n_rays = len(start_points)
    r_of_z = np.zeros((n_rays, len(z_for_drawing), 3))
    for ray_idx in range(n_rays):
        raytrace_data = trace(pob_model, start_points[ray_idx], start_directions[ray_idx], wavelength_nm)
        n_steps = len(raytrace_data.ray)
        assert n_steps == len(z_for_drawing)

        for i, ray in enumerate(raytrace_data.ray):
            r = ray[0]
            k = ray[1]
            r_of_z[ray_idx, i] = r

        r_of_z[ray_idx,:,2] = z_for_drawing + r_of_z[ray_idx,:,2]

    return r_of_z



def calc_contrast(sm, pitch, x0=0, na=0.04):
    n_rays = 13
    angles = np.linspace(-na, na, n_rays)
    x_bright = x0 + pitch

    data = np.zeros((n_rays, 2))
    for i, angle in enumerate(angles):
        ray = trace(sm, np.array([x0, 0., 0.]), np.array([angle, 0., 1]), 550)
        data[i,0] = ray[0][-1][0][0]
        ray = trace(sm, np.array([x_bright, 0., 0.]), np.array([angle, 0., 1]), 550)
        data[i,1] = ray[0][-1][0][0]

    center = np.mean(data)
    center_int = 0
    for i in range(2):
        center_int += np.exp(-np.square((center - np.mean(data[:,i])) / np.std(data[:,i])) / 2)

    return 1 - center_int

def mtf_guess(sm):
    pitches = np.linspace(5, 100, 30) * 1e-4
    contrast = np.zeros_like(pitches)
    for i, p in enumerate(pitches):
        contrast[i] = calc_contrast(sm, p, 0.6 / 5, 0.04)
    return 1e3 * pitches, contrast


if __name__ == "__main__":
    start_points = np.zeros((10, 3))
    start_directions = np.zeros((10, 3))
    start_directions[:,2] = 1.
    # # pupil raytrace
    # object_dirs[:,0] = np.linspace(0., 0.1, 10)
    # field raytrace
    start_points[:,0] = np.linspace(0., 0.1, 10)
