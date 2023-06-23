
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
    ids,nodpos = [],[]
    with open(outpath/"obs_nodding/nodpos.txt", 'r') as f:
        for line in f:
            fields = ' '.join(line.split()).split(' ')
            ids.append(fields[0])
            nodpos.append(fields[1])


    for sofpath in soflist:
        i = str(sofpath).split('_')[-1].split('.')[0]
        for k,ii in enumerate(ids):
            if ii == i:
                nod = nodpos[k]
        print('\n')
        print(f'==========>>>>> PROCESSING SOF {sofpath} (position {nod}) IN OBS-NODDING MODE <<<<<==========')
        check_files_exist(sofpath)
        if not cosmics:
            os.system('esorex '+' --output-dir='+str(outpath/'obs_nodding/output/')+' cr2res_obs_nodding '+str(sofpath))
        else:
            os.system('esorex '+' --output-dir='+str(outpath/'obs_nodding/output/')+' cr2res_obs_nodding --cosmics '+str(sofpath))


        if not Path(outpath/'obs_nodding/output/bg_frames').exists():
            os.mkdir(outpath/'obs_nodding/output/bg_frames')

        if nod == 'A':
            # if True:
            # shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_combinedA.fits',outpath/f'obs_nodding/output/cr2res_obs_nodding_combinedA_{i}.fits')
            shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_extractedA.fits',outpath/f'obs_nodding/output/cr2res_obs_nodding_extractedA_{i}.fits')
            shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_slitfuncA.fits',outpath/f'obs_nodding/output/cr2res_obs_nodding_slitfuncA_{i}.fits')
            shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_modelA.fits',outpath/f'obs_nodding/output/cr2res_obs_nodding_modelA_{i}.fits')
            shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_trace_wave_A.fits',outpath/f'obs_nodding/output/cr2res_obs_nodding_trace_wave_A_{i}.fits')
            # os.remove(outpath/'obs_nodding/output/cr2res_obs_nodding_combinedA.fits')
            # os.remove(outpath/'obs_nodding/output/cr2res_obs_nodding_combinedB.fits')
            # os.remove(outpath/'obs_nodding/output/cr2res_obs_nodding_extractedB.fits')
            # os.remove(outpath/'obs_nodding/output/cr2res_obs_nodding_slitfuncB.fits')
            # os.remove(outpath/'obs_nodding/output/cr2res_obs_nodding_modelB.fits')
            # os.remove(outpath/'obs_nodding/output/cr2res_obs_nodding_trace_wave_B.fits')
            # os.remove(outpath/'obs_nodding/output/cr2res_obs_nodding_extracted_combined.fits')
            shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_extractedB.fits',outpath/f'obs_nodding/output/bg_frames/cr2res_obs_nodding_extractedB_{i}.fits')
            shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_slitfuncB.fits',outpath/f'obs_nodding/output/bg_frames/cr2res_obs_nodding_slitfuncB_{i}.fits')
            shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_modelB.fits',outpath/f'obs_nodding/output/bg_frames/cr2res_obs_nodding_modelB_{i}.fits')
            shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_trace_wave_B.fits',outpath/f'obs_nodding/output/bg_frames/cr2res_obs_nodding_trace_wave_B_{i}.fits')

        if nod == 'B':
            # if True:
            # shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_combinedB.fits',outpath/f'obs_nodding/output/cr2res_obs_nodding_combinedB_{i}.fits')
            shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_extractedB.fits',outpath/f'obs_nodding/output/cr2res_obs_nodding_extractedB_{i}.fits')
            shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_slitfuncB.fits',outpath/f'obs_nodding/output/cr2res_obs_nodding_slitfuncB_{i}.fits')
            shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_modelB.fits',outpath/f'obs_nodding/output/cr2res_obs_nodding_modelB_{i}.fits')
            shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_trace_wave_B.fits',outpath/f'obs_nodding/output/cr2res_obs_nodding_trace_wave_B_{i}.fits')
            # shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_extracted_combined.fits',outpath/f'obs_nodding/output/cr2res_obs_nodding_extracted_combined_{i}.fits')
            # os.remove(outpath/'obs_nodding/output/cr2res_obs_nodding_combinedB.fits')
            # os.remove(outpath/'obs_nodding/output/cr2res_obs_nodding_combinedA.fits')
            # os.remove(outpath/'obs_nodding/output/cr2res_obs_nodding_extractedA.fits')
            # os.remove(outpath/'obs_nodding/output/cr2res_obs_nodding_slitfuncA.fits')
            # os.remove(outpath/'obs_nodding/output/cr2res_obs_nodding_modelA.fits')
            # os.remove(outpath/'obs_nodding/output/cr2res_obs_nodding_trace_wave_A.fits')
            # os.remove(outpath/'obs_nodding/output/cr2res_obs_nodding_extracted_combined.fits')
            shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_extractedA.fits',outpath/f'obs_nodding/output/bg_frames/cr2res_obs_nodding_extractedA_{i}.fits')
            shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_slitfuncA.fits',outpath/f'obs_nodding/output/bg_frames/cr2res_obs_nodding_slitfuncA_{i}.fits')
            shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_modelA.fits',outpath/f'obs_nodding/output/bg_frames/cr2res_obs_nodding_modelA_{i}.fits')
            shutil.move(outpath/'obs_nodding/output/cr2res_obs_nodding_trace_wave_A.fits',outpath/f'obs_nodding/output/bg_frames/cr2res_obs_nodding_trace_wave_A_{i}.fits')
