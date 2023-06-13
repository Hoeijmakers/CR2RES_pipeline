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
