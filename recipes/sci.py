
def obs_staring(outpath,cosmics=False):
    """This is a wrapper for the obs_staring recipe."""
    import os
    from pathlib import Path
    from recipes.sof import check_files_exist
    print('==========>>>>> PROCESSING SCIENCE FRAMES IN OBS-STARING MODE <<<<<==========')
    outpath = Path(outpath)

    soflist = Path(outpath/"obs_staring/").glob("SCI_*.txt")
    for sofpath in soflist:
        print(f'==========>>>>> PROCESSING SOF {sofpath} IN OBS-STARING MODE <<<<<==========')
        check_files_exist(sofpath)
        if not cosmics:
            os.system('esorex '+' --output-dir='+str(outpath/'obs_staring/')+' cr2res_obs_staring '+str(sofpath))
        else:
            os.system('esorex '+' --output-dir='+str(outpath/'obs_staring/')+' cr2res_obs_staring --cosmics '+str(sofpath))


def obs_nodding(outpath,cosmics=False):
    """This is a wrapper for the obs_nodding recipe."""
    import os
    from pathlib import Path
    from recipes.sof import check_files_exist
    print('==========>>>>> PROCESSING SCIENCE FRAMES IN OBS-NODDING MODE <<<<<==========')
    outpath = Path(outpath)

    soflist = Path(outpath/"obs_nodding/").glob("SCI_*.txt")
    for sofpath in soflist:
        print(f'==========>>>>> PROCESSING SOF {sofpath} IN OBS-STARING MODE <<<<<==========')
        check_files_exist(sofpath)
        if not cosmics:
            os.system('esorex '+' --output-dir='+str(outpath/'obs_nodding/')+' cr2res_obs_nodding '+str(sofpath))
        else:
            os.system('esorex '+' --output-dir='+str(outpath/'obs_nodding/')+' cr2res_obs_nodding --cosmics '+str(sofpath))
