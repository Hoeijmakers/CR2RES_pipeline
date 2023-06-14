def util_calib_flat(outpath):
    """This is a wrapper for the util_calib recipe."""
    import os
    from pathlib import Path
    from recipes.sof import check_files_exist
    print('==========>>>>> CREATING MASTER FLAT <<<<<==========')
    outpath = Path(outpath)
    sofpath = outpath/"util_calib_flat/CALIB.txt"
    check_files_exist(sofpath)
    os.system('esorex '+' --output-dir='+str(outpath/'util_calib_flat/')+' cr2res_util_calib --collapse="MEAN" '+str(sofpath))

def util_trace(outpath):
    """This is a wrapper for the util_trace recipe."""
    import os
    from pathlib import Path
    from recipes.sof import check_files_exist
    print('==========>>>>> CREATING TRACE <<<<<==========')
    outpath = Path(outpath)
    sofpath = outpath/"util_trace/TRACE.txt"
    check_files_exist(sofpath)
    os.system('esorex '+' --output-dir='+str(outpath/'util_trace/')+' cr2res_util_trace '+str(sofpath))

def util_slit_curv(outpath):
    """This is a wrapper for the util_slit_curv recipe."""
    import os
    from pathlib import Path
    from recipes.sof import check_files_exist
    print('==========>>>>> CREATING SLIT MAP <<<<<==========')
    outpath = Path(outpath)
    sofpath = outpath/"util_slit_curv/SLITCURV.txt"
    check_files_exist(sofpath)
    os.system('esorex '+' --output-dir='+str(outpath/'util_slit_curv/')+' cr2res_util_slit_curv '+str(sofpath))


def util_extract_calib(outpath):
    """This is a wrapper for the util_extract recipe applied on the calibration frame"""
    import os
    from pathlib import Path
    from recipes.sof import check_files_exist
    print('==========>>>>> EXTRACTING CALIB <<<<<==========')
    outpath = Path(outpath)
    sofpath = outpath/"util_extract_calib/EXTRACT_CALIB.txt"
    check_files_exist(sofpath)
    os.system('esorex '+' --output-dir='+str(outpath/'util_extract_calib/')+' cr2res_util_extract  --smooth_slit=3 -smooth_spec=2 '+str(sofpath))


def util_normflat(outpath):
    """This is a wrapper for the util_normflat recipe applied on the calibration frame"""
    import os
    from pathlib import Path
    from recipes.sof import check_files_exist
    print('==========>>>>> CREATING NORMFLAT <<<<<==========')
    outpath = Path(outpath)
    sofpath = outpath/"util_normflat/NORMFLAT.txt"
    check_files_exist(sofpath)
    os.system('esorex '+' --output-dir='+str(outpath/'util_normflat/')+' cr2res_util_normflat '+str(sofpath))


def util_calib_une(outpath):
    """This is a wrapper for the util_calib recipe."""
    import os
    from pathlib import Path
    from recipes.sof import check_files_exist
    print('==========>>>>> CALIBRATING WAVE UNE <<<<<==========')
    outpath = Path(outpath)
    sofpath = outpath/"util_calib_une/CALIB.txt"
    check_files_exist(sofpath)
    os.system('esorex '+' --output-dir='+str(outpath/'util_calib_une/')+' cr2res_util_calib --collapse="MEAN" --subtract_nolight_rows=TRUE '+str(sofpath))

def util_extract_une(outpath):
    """This is a wrapper for the util_extract recipe applied on the UNE frame"""
    import os
    from pathlib import Path
    from recipes.sof import check_files_exist
    print('==========>>>>> EXTRACTING UNE <<<<<==========')
    outpath = Path(outpath)
    sofpath = outpath/"util_extract_une/EXTRACT_UNE.txt"
    check_files_exist(sofpath)
    os.system('esorex '+' --output-dir='+str(outpath/'util_extract_une/')+' cr2res_util_extract --smooth_slit=3 '+str(sofpath))

def util_wave_une(outpath,deg=2,err=0.03):
    """This is a wrapper for the util_wave recipe applied on the extracted UNE frame"""
    import os
    from pathlib import Path
    from recipes.sof import check_files_exist
    print('==========>>>>> EXTRACTING WAVELENGTH SOLUTION UNE <<<<<==========')
    outpath = Path(outpath)
    sofpath = outpath/"util_wave/WAVE.txt"
    check_files_exist(sofpath)
    os.system('esorex '+' --output-dir='+str(outpath/'util_wave/')+f' cr2res_util_wave  --wl_method=XCORR --wl_degree={deg} --keep --wl_err={err} --fallback '+str(sofpath))


def util_calib_fpet(outpath):
    """This is a wrapper for the util_calib recipe."""
    import os
    from pathlib import Path
    from recipes.sof import check_files_exist
    print('==========>>>>> CALIBRATING WAVE FPET <<<<<==========')
    outpath = Path(outpath)
    sofpath = outpath/"util_calib_fpet/CALIB.txt"
    check_files_exist(sofpath)
    os.system('esorex '+' --output-dir='+str(outpath/'util_calib_fpet/')+' cr2res_util_calib --collapse="MEAN" '+str(sofpath))

def util_extract_fpet(outpath):
    """This is a wrapper for the util_extract recipe applied on the FPET frame"""
    import os
    from pathlib import Path
    from recipes.sof import check_files_exist
    print('==========>>>>> EXTRACTING FPET <<<<<==========')
    outpath = Path(outpath)
    sofpath = outpath/"util_extract_fpet/EXTRACT_FPET.txt"
    check_files_exist(sofpath)
    os.system('esorex '+' --output-dir='+str(outpath/'util_extract_fpet/')+' cr2res_util_extract --smooth_slit=3 '+str(sofpath))


def util_wave_fpet(outpath,deg=4):
    """This is a wrapper for the util_wave recipe applied on the extracted UNE frame"""
    import os
    from pathlib import Path
    from recipes.sof import check_files_exist
    print('==========>>>>> EXTRACTING WAVELENGTH SOLUTION FPET <<<<<==========')
    outpath = Path(outpath)
    sofpath = outpath/"util_wave_fpet/WAVE.txt"
    check_files_exist(sofpath)
    os.system('esorex '+' --output-dir='+str(outpath/'util_wave_fpet/')+f' cr2res_util_wave  --wl_method=ETALON --wl_degree={deg} --fallback '+str(sofpath))
