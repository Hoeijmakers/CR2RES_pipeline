def detlin(outpath):
    import os
    from pathlib import Path
    from recipes.sof import check_files_exist
    print('==========>>>>> CREATING DETLIN COEFFICIENTS <<<<<==========')
    outpath = Path(outpath)
    sofpath = outpath/"detlin/DETLIN.txt"
    check_files_exist(sofpath)
    os.system('esorex '+' --output-dir='+str(outpath/'detlin/')+' cr2res_cal_detlin '+str(sofpath))



def master_dark(outpath):
    """This is a wrapper for the cal_dark recipe."""
    import os
    from pathlib import Path
    from recipes.sof import check_files_exist
    print('==========>>>>> CREATING MASTER DARK AND BAD PIXEL MAP <<<<<==========')
    outpath = Path(outpath)
    sofpath = outpath/"cal_dark/DARK.txt"
    check_files_exist(sofpath)
    os.system('esorex '+' --output-dir='+str(outpath/'cal_dark/')+' cr2res_cal_dark '+str(sofpath))




def master_flat(outpath):
    """This is a wrapper for the cal_flat recipe."""
    import os
    from pathlib import Path
    from recipes.sof import check_files_exist
    print('==========>>>>> CREATING MASTER FLAT <<<<<==========')
    outpath = Path(outpath)
    sofpath = outpath/"cal_flat/FLAT.txt"
    check_files_exist(sofpath)
    os.system('esorex '+' --output-dir='+str(outpath/'cal_flat/')+' cr2res_cal_flat '+str(sofpath))
