from recipes import sof
from recipes import cal, util


inpath = '/data/jens/observations/55-cnc/dayside_crires_raw_night4'
outpath = 'test'

sof.create_sof(inpath,outpath,detlin='/data/jens/observations/55-cnc/detlin/')
# cal.detlin(outpath)
# cal.master_dark(outpath)
# util.util_calib_flat(outpath)
# util.util_trace(outpath)
# util.util_slit_curv(outpath)
# util.util_extract_calib(outpath)
util.util_normflat(outpath)
