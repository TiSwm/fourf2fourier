import numpy as np
import matplotlib.pyplot as plt

wl = 550e-6 # mm

def slit(x, x0, w):
    return np.where(np.abs(x-x0) < w / 2, 1, 0)

def fft_on_grid(x, y, inverse=False):
    domain = np.max(x) - np.min(x)
    dx = domain/len(x)
    if inverse:
        fft_y = np.fft.ifft(y, norm="ortho")
    else:
        fft_y = np.fft.fft(y, norm="ortho")
    k = np.fft.fftfreq(len(x), d=dx)
    if inverse:
        k = np.fft.ifftshift(k)
    return k, fft_y

def filter_for_k_larger_cut(k, cut):
    slope = (np.max(k) - np.min(k)) / (len(k))
    filter = 1 - 1 / (1 + np.exp(-(k - cut) / slope)) - 1 / (1 + np.exp(-(-k - cut) / slope))
    return filter


x = np.linspace(-2, 2, 1000) / wl
w = 0.2

single_slit = slit(x * wl, 0, .2)
double_slit = slit(x * wl, 0, .2)

obj = single_slit
k, fft = fft_on_grid(x, obj)

filter = filter_for_k_larger_cut(k, cut=0.0027)
# filter = filter_for_k_larger_cut(k, cut=0.0027 * 2)
cut_x, img = fft_on_grid(k, filter * fft, inverse=True)

fig, ax = plt.subplots(3)
ax[0].plot(x, obj)
ax[1].plot(k, np.square(np.abs(fft)))
ax[1].plot(k, np.square(np.abs(fft * filter)))
ax[2].plot(x, obj)
ax[2].plot(cut_x, img)
# ax[2].set_xlim(-2, 2)
plt.show()
