
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
    import sys
    from pathlib import Path
    from recipes.sof import check_files_exist
    import shutil
    print('==========>>>>> PROCESSING SCIENCE FRAMES IN OBS-NODDING MODE <<<<<==========')
    outpath = Path(outpath)

    soflist = Path(outpath/"obs_nodding/").glob("SCI_*.txt")
    for sofpath in soflist:
        i = str(sofpath).split('_')[-1].split('.')[0]
        print(f'==========>>>>> PROCESSING SOF {sofpath} IN OBS-STARING MODE <<<<<==========')
        check_files_exist(sofpath)
        if not cosmics:
            os.system('esorex '+' --output-dir='+str(outpath/'obs_nodding/output/')+' cr2res_obs_nodding '+str(sofpath))
        else:
            os.system('esorex '+' --output-dir='+str(outpath/'obs_nodding/output/')+' cr2res_obs_nodding --cosmics '+str(sofpath))

        shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_combinedA.fits',outpath/f'obs_nodding/output/cr2res_obs_nodding_combinedA_{i}.fits')
        shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_extractedA.fits',outpath/f'obs_nodding/output/cr2res_obs_nodding_extractedA_{i}.fits')
        shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_slitfuncA.fits',outpath/f'obs_nodding/output/cr2res_obs_nodding_slitfuncA_{i}.fits')
        shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_modelA.fits',outpath/f'obs_nodding/output/cr2res_obs_nodding_modelA_{i}.fits')
        shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_trace_wave_A.fits',outpath/f'obs_nodding/output/cr2res_obs_nodding_trace_wave_A_{i}.fits')
        shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_combinedB.fits',outpath/f'obs_nodding/output/cr2res_obs_nodding_combinedB_{i}.fits')
        shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_extractedB.fits',outpath/f'obs_nodding/output/cr2res_obs_nodding_extractedB_{i}.fits')
        shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_slitfuncB.fits',outpath/f'obs_nodding/output/cr2res_obs_nodding_slitfuncB_{i}.fits')
        shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_modelB.fits',outpath/f'obs_nodding/output/cr2res_obs_nodding_modelB_{i}.fits')
        shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_trace_wave_B.fits',outpath/f'obs_nodding/output/cr2res_obs_nodding_trace_wave_B_{i}.fits')
        shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_extracted_combined.fits',outpath/f'obs_nodding/output/cr2res_obs_nodding_extracted_combined_{i}.fits')
        sys.exit()
