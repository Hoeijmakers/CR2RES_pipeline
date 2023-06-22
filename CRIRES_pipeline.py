from recipes import sof, cal, util, sci


inpath = '/data/jens/observations/55-cnc/dayside_crires_raw_night4'
outpath = 'test'


# sof.print_raw_list(inpath)
sof.create_sof(inpath,outpath,detlin='/data/jens/observations/55-cnc/detlin/',pattern='ABBA',remake_bg=False)
# cal.detlin(outpath)
# cal.master_dark(outpath)
# util.util_calib_flat(outpath)
# util.util_trace(outpath)
# util.util_slit_curv(outpath)
# util.util_extract_calib(outpath)
# util.util_normflat(outpath)
# util.util_calib_une(outpath)
# util.util_extract_une(outpath)
# util.util_wave(outpath,deg=0,err=0.1)
# util.util_wave(outpath,deg=2,err=0.03)
# util.util_calib_fpet(outpath)
# util.util_extract_fpet(outpath)
# util.util_wave_fpet(outpath,deg=4)
# sci.obs_staring(outpath) #ADD TO THIS THAT OUTPUT GETS RENAMED TO AVOID OVERWRITING.
