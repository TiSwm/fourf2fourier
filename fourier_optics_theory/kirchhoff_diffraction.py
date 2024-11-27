import numpy as np
import matplotlib.pyplot as plt
from fourier_optics import slit, fft_on_grid
from tqdm import tqdm

nx = 6000

z_s = -100
z_i = +0.004
w_o = 1
w_i = 1
wl = 500e-6

x_o = np.linspace(-w_o / 2, w_o / 2, nx)
x_i = np.linspace(-w_i / 2, w_i / 2, nx)

r_s = np.array([3, z_s])
r_s = np.array([0, z_s])

width_slit = 5 * wl
dist_slits = 10 * wl

def grid(cd, pitch, n_elements=20, offset=0):
    width = n_elements * pitch - 2 * (pitch - cd)
    x0 = width / 2 + offset
    def object_function(x_o):
        transmission = np.zeros_like(x_o, dtype="complex")
        for i in range(n_elements):
            transmission += slit(x_o, -x0 + i * pitch, cd)
        return transmission
    return object_function, 1.1 * n_elements * pitch / 2


def double_slit(width_slit, dist_slits):
    def object_function(x_o):
        return slit(x_o, -dist_slits / 2, width_slit) + slit(x_o, +dist_slits / 2, width_slit)
    return object_function

# object_function = double_slit(width_slit, dist_slits)
object_function, window = grid(width_slit * 2, dist_slits * 5, n_elements=4)
object_function, window = grid(cd=5 * wl, pitch=10 * wl, n_elements=2)
# object_function, window = grid(cd=50 * wl, pitch=100 * wl, n_elements=2)

def kirchhoff_integral(z_i, wl, x_o, x_i, r_s, obj_function):
    obj = obj_function(x_o)
    nx = len(x_o)
    dx_o = (np.max(x_o) - np.min(x_o)) / nx
    rr_o = np.array([x_o, np.zeros_like(x_o)]).T
    rr_s = np.tile(r_s, (nx, 1))
    d_s = np.linalg.norm(rr_s - rr_o, axis=1)

    img = np.zeros_like(x_i)
    for idx, x in enumerate(x_i):
        r_i = np.array([x, z_i])
        rr_i = np.tile(r_i, (nx, 1))
        d_i = np.linalg.norm(rr_i - rr_o, axis=1)

        E_img = dx_o / wl * np.sum(obj * np.exp(2.j * np.pi * (d_s + d_i) / wl) / (d_s * d_i))
        img[idx] = np.square(np.abs(E_img))
    return img

def plot_nearfield():
    x_o = np.linspace(-w_o / 2, w_o / 2, nx * 20)
    x_i = np.linspace(-w_o / 2, w_o / 2, 2000)
    z_nf = 2 * wl
    img = kirchhoff_integral(z_i=z_nf, wl=wl, x_o=x_o, x_i=x_i, r_s=r_s, obj_function=object_function)

    fig, ax = plt.subplots(2)
    ax[0].plot(x_o, object_function(x_o))
    ax[0].set_xlim(-window, window)
    ax[1].plot(x_i, img * np.square(z_s + z_nf))
    ax[1].set_xlim(-window, window)
    plt.show()


def plot_farfield():
    x_o = np.linspace(-w_o / 2, w_o / 2, nx * 20)
    z_ff = 50 * w_o / wl
    x_i = np.linspace(-w_o / 2, w_o / 2, 2000) * z_ff
    print(z_ff)
    img = kirchhoff_integral(z_i=z_ff, wl=wl, x_o=x_o, x_i=x_i, r_s=r_s, obj_function=object_function)

    fig, ax = plt.subplots(2)
    ax[0].plot(x_o, object_function(x_o))
    ax[0].set_xlim(-window, window)
    ax[1].plot(x_i, img * np.square(z_s + z_ff))
    plt.show()

plot_nearfield()
plot_farfield()

# aerial image
aerial = []
z_cuts = np.linspace(0.001, 1, 100)
for z in tqdm(z_cuts):
    aerial.append(kirchhoff_integral(z_i=z, wl=wl, x_o=x_o, x_i=x_i, r_s=r_s, obj_function=object_function))
aerial = np.array(aerial)

fig, ax = plt.subplots()
ax.imshow(aerial.T * np.tile(z_cuts, (aerial.shape[1], 1)), extent=(np.min(z_cuts), np.max(z_cuts), np.min(x_i), np.max(x_i)))
plt.show()
fig, ax = plt.subplots(1, 5)
# ax[0].imshow(np.log(aerial).T, extent=(np.min(z_cuts), np.max(z_cuts), np.min(x_i), np.max(x_i)))
for ax_idx, z_idx in enumerate([0, 2, 4, 10, -1]):
    ax[ax_idx].plot(aerial[z_idx] * z_cuts[z_idx], x_i)
    ax[ax_idx].set_title(r"z / $\lambda=$" + f"{np.around(z_cuts[z_idx] / wl, 2)}")
plt.tight_layout()
plt.show()

z = 1e3
x_i = z * np.linspace(-w_i / 2, w_i / 2, nx * 10)
x_o = np.linspace(-w_o * 10, w_o * 10, nx * 10)
kirchhoff = kirchhoff_integral(z_i=z, wl=wl, x_o=x_o, x_i=x_i, r_s=r_s, obj_function=object_function)

illu_phase = np.exp(+2.j * np.pi * x_o * r_s[0] / r_s[1] / wl)
k, fft = fft_on_grid(x_o / wl, object_function(x_o) * illu_phase)
fourier = np.square(np.abs(fft))
x_fourier = z * np.tan(np.arcsin(k))

kirchhoff /= np.max(kirchhoff)
fourier /= np.max(fourier)
fig, ax = plt.subplots()
ax.plot(x_i, kirchhoff, label="Exact Kirchhoff")
ax.plot(x_fourier, fourier, "--", label="Fourier approximation")
ax.legend()
ax.set_xlim(np.min(x_i), np.max(x_i))
plt.show()
