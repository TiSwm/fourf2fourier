import numpy as np
import matplotlib.pyplot as plt

def slit(x, x0, w):
    return np.where(np.abs(x-x0) < w / 2, 1, 0)

def fft_on_grid(x, y, inverse=False):
    if inverse:
        fft_y = np.fft.ifft(y, norm="ortho")
    else:
        fft_y = np.fft.fft(y, norm="ortho")
    domain = np.max(x) - np.min(x)
    dx = domain/len(x)
    k = np.fft.fftfreq(len(x), d=dx)
    if inverse:
        k = np.fft.ifftshift(k)
    return k, fft_y

def filter_for_k_larger_cut(k, cut):
    slope = (np.max(k) - np.min(k)) / (len(k))
    filter = 1 - 1 / (1 + np.exp(-(k - cut) / slope)) - 1 / (1 + np.exp(-(-k - cut) / slope))
    return filter

def illumination(x, k):
    slope = np.tan(np.arcsin(k)) * 2 * np.pi / wl
    return np.exp(1.j * slope * x)

def calc_image(x, pupil, obj, na):
    image = np.zeros_like(obj, dtype="complex")
    for k_illu in pupil:
        il_obj = obj * illumination(x, k_illu)
        k, fft = fft_on_grid(x, il_obj)
        filter = filter_for_k_larger_cut(k, cut=na)
        cut_x, img = fft_on_grid(k, filter * fft, inverse=True)
        image += np.square(np.abs(img))
    return cut_x, image / 4

if __name__ == "__main__":
    wl = 550e-6 # mm
    x = np.linspace(-0.5, 0.5, int(2e5)) / wl
    w = 5 * wl
    d = 10 * wl
    single_slit = slit(x * wl, 0, w)
    double_slit = slit(x * wl, -d, w) + slit(x * wl, +d, w)
    pupil = [0.000001, -0.000001, 0.0000005, -0.0000005]
    # pupil = [0.0]

    obj = double_slit
    na = 0.02

    cut_x, img = calc_image(x, pupil, obj, na)

    k, fft = fft_on_grid(x, obj)
    filter = filter_for_k_larger_cut(k, cut=na)

    fig, ax = plt.subplots(2)
    ax[0].set_title("Real space")
    ax[0].plot(x, np.square(np.abs(obj)), label="mask")
    ax[0].plot(cut_x, img, "--", label="wafer")
    ax[0].set_xlabel(r"x / $\lambda$")
    ax[0].set_xlim(-40, 40)
    ax[0].set_title("Diffraction pattern")
    ax[1].plot(k, np.square(np.abs(fft)), label="mask")
    ax[1].plot(k, np.square(np.abs(fft * filter)), "--", label="wafer")
    ax[1].set_xlim(-0.5, 0.5)
    ax[1].set_xlabel(r"k $\lambda$")
    plt.tight_layout()
    plt.show()

    # pupil = [-0.00004, 0.00004, -0.000041, 0.000041]
    # cut_x, img = calc_image(x, pupil, obj, na)

    # k, fft = fft_on_grid(x, obj * illumination(x, 0.00004))
    # fig, ax = plt.subplots(2)
    # ax[0].plot(x, np.square(np.abs(obj)))
    # ax[0].plot(cut_x, img / np.max(img))
    # ax[0].set_xlabel(r"x / $\lambda$")
    # ax[1].plot(k, np.square(np.abs(fft)))
    # ax[1].plot(k, np.square(np.abs(fft * filter)))
    # ax[1].set_xlim(-0.5, 0.5)
    # # ax[1].set_xlabel(r"k $\lambda$")
    # plt.show()
