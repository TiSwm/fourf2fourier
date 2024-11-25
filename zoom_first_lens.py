from rayoptics.environment import *

def get_model(shift_obj=0, shift_tube=0, NA=0.04):
    opm = OpticalModel()
    sm = opm['seq_model']
    osp = opm['optical_spec']

    beta = 5
    r_max_sensor = 3.1

    osp['pupil'] = PupilSpec(osp, key=['object', 'NA'], value=NA)
    osp['fov'] = FieldSpec(osp, key=['object', 'height'], value=0.6, flds=[0., 0.1 / beta, 1. / beta, r_max_sensor / beta], is_relative=True)
    osp['wvls'] = WvlSpec([(550.0, 1.0)], ref_wl=0)
    opm.radius_mode = True

    # sm.gaps[0].thi=28.17 + shift_obj
    # sm.add_surface([+20.89, 12.0, 'N-BAF10', 'Schott'])
    # sm.add_surface([-16.73, 2.00, 'N-SF6HT', 'Schott'])
    # sm.add_surface([-79.8, 22.9])

    sm.gaps[0].thi=21.175 + shift_obj
    sm.add_surface([+79.8, 2.00, 'N-SF6HT', 'Schott'])
    sm.add_surface([+16.73, 12.00, 'N-BAF10', 'Schott'])
    sm.add_surface([-20.89, 22.9, ])

    sm.set_stop()

    sm.add_surface([np.inf, 150.0 - shift_obj + shift_tube])
    sm.add_surface([+91.62, 5.7, 'N-BK7', 'Schott'])
    sm.add_surface([-66.68, 2.2, 'SF5', 'Schott'])
    sm.add_surface([-197.7, 172.071 - shift_tube])

    opm.update_model()

    return sm


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


shifts = np.linspace(-.1, .1, 60)
contrast_at_50um = np.zeros_like(shifts)

fig, ax = plt.subplots()
for i, shift in enumerate(shifts):
    sm = get_model(shift)
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
    sm = get_model(0., shift)
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
