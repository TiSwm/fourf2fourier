from rayoptics.environment import OpticalModel, PupilSpec, FieldSpec, WvlSpec
import numpy as np

def get_rayoptics_model(shift_obj=0, shift_tube=0, NA=0.04, flip_first_lens=False):
    opm = OpticalModel()
    sm = opm['seq_model']
    osp = opm['optical_spec']

    beta = 5
    r_max_sensor = 3.1

    osp['pupil'] = PupilSpec(osp, key=['object', 'NA'], value=NA)
    osp['fov'] = FieldSpec(
        osp, key=['object', 'height'],
        value=r_max_sensor / beta,
        flds=[0., 0.1, 0.5, 1.], is_relative=True)
    osp['wvls'] = WvlSpec([(550.0, 1.0)], ref_wl=0)
    opm.radius_mode = True

    if flip_first_lens:
        sm.gaps[0].thi=28.17 + shift_obj
        sm.add_surface([+20.89, 12.0, 'N-BAF10', 'Schott'])
        sm.add_surface([-16.73, 2.00, 'N-SF6HT', 'Schott'])
        sm.add_surface([-79.8, 22.9])
    else:
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
