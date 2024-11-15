from rayoptics.environment import *
isdark = False

opm = OpticalModel()
sm = opm['seq_model']
osp = opm['optical_spec']
pm = opm['parax_model']
em = opm['ele_model']
pt = opm['part_tree']
ar = opm['analysis_results']

f1 = 30
f2 = 150

FieldSpec()
osp['pupil'] = PupilSpec(osp, key=['object', 'NA'], value=0.25)
osp['fov'] = FieldSpec(osp, key=['object', 'height'], value=25.0, flds=[0., 0.5, 1.], is_relative=True)
osp['wvls'] = WvlSpec([('F', 0.5), (550.0, 1.0), ('C', 0.5)], ref_wl=1)

opm.radius_mode = True

sm.gaps[0].thi=f1
help(sm.add_surface)
