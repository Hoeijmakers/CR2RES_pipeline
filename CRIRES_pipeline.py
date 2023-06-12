def create_sof(inpath,outpath,dit=0,detlin=''):
    """This script creates the file association lists (sof files) that are the main inputs
    to the pipeline recipes when called with esorex. The user provides the path of the raw data
    foe;s (inpath) as downloaded from the ESO archive. These must be sorted by instrument mode
    (i.e. use the same grating and nodding strategy). The user provides the output path, to which
    the sof files will be written (outpath).  This is also the location in which the pipeline
    reduction products will be stored. Finally, the user manually provides the exposure time they
    expect (in case of DARK and OBJECT frames with multiple exposures).


    Set the detlin parameter to a path where you have downloaded the detector linearity raw data
    for use with the cal_detlin recipe. This is optional though.
    """
    import os
    import numpy as np
    import astropy.io.fits as fitsio
    import pdb
    import sys
    from pathlib import Path
    import glob

    outpath=Path(outpath)

    if not outpath.exists():
        os.mkdir(outpath)
    else:
        really = input(f"{str(outpath)} already exists. Do you want to continue? A lot of "
        "overwriting might happen [y/N]")
        if really.lower()=='y':
            pass
        else:
            sys.exit()

    fits_list = os.listdir(inpath)
    fits_list = [str(i) for i in Path(inpath).glob('CRIRE*.fits')]
    static_list = [str(i) for i in Path(inpath).glob('M.CRIRE*.fits')]
    detlin_list = []

    type_list=[]
    static_type_list=[]
    detlin_type_list=[]
    dits_list = []

    for file in static_list:
        with fitsio.open(file) as fu:
            static_type_list.append(fu[0].header['ESO PRO CATG'])
    for file in fits_list:
        with fitsio.open(file) as fu:
            type_list.append(fu[0].header['HIERARCH ESO DPR TYPE'])
            dits_list=np.append(dits_list,fu[0].header['EXPTIME'])


    if len(detlin)>0:
        print(f'Loading detlin files from {detlin}')
        detlinpath = Path(detlin)

        detlin_list = os.listdir(detlinpath)
        detlin_list = [str(i) for i in Path(detlinpath).glob('CRIRE*.fits')]
        for d in detlin_list:
            with fitsio.open(d) as fu:
                detlin_type_list.append(fu[0].header['HIERARCH ESO DPR TYPE'])

        detlin_dark_list = []
        detlin_lamp_list = []
        for i in range(len(detlin_list)):
            # print(detlin_list[i].split('/')[-1],detlin_type_list[i])
            if detlin_type_list[i] == 'FLAT,LAMP,DETCHECK':
                detlin_lamp_list = np.append(detlin_lamp_list,detlin_list[i]+'   DETLIN_LAMP')
            if detlin_type_list[i] == 'DARK,DETCHECK':
                detlin_dark_list = np.append(detlin_dark_list,detlin_list[i]+'   DETLIN_DARK')
        if len(detlin_dark_list) == 0:
            print('ERROR: No DARK frames detected. Check that you downloaded them properly and that.'
            'if you have set a DIT requirement, that DARKS were taken at that exposure time.')
            sys.exit()
        if len(detlin_lamp_list) == 0:
            print('ERROR: No FLAT frames detected. Check that you downloaded them properly.')
            sys.exit()

        if not (outpath/"detlin").exists(): os.mkdir(outpath/"detlin")
        outF = open(outpath/"detlin/DETLIN.txt", "w")
        for line in detlin_dark_list:
            outF.write(line)
            outF.write("\n")
        for line in detlin_lamp_list:
            outF.write(line)
            outF.write("\n")
        outF.close()






    dark_list=[]
    flat_list=[]
    fpet_list=[]
    sci_A_list=[]

    for i in range(len(fits_list)):
        # print(fits_list[i].split('/')[-1],type_list[i]+'\t\t\t',dits_list[i])
        if type_list[i] == 'DARK':
            dark_list = np.append(dark_list,fits_list[i]+'   '+type_list[i])
        if type_list[i] == 'FLAT':
            flat_list = np.append(flat_list,fits_list[i]+'   '+type_list[i])
        if type_list[i] == 'WAVE,FPET':
            fpet_list = np.append(fpet_list,fits_list[i]+'   WAVE_FPET')

    # print('')
    # for i in range(len(static_list)):
    #     print(static_list[i].split('/')[-1],static_type_list[i])

    print(fpet_list)

    if len(dark_list) == 0:
        print('ERROR: No DARK frames detected. Check that you downloaded them properly and that.'
        'if you have set a DIT requirement, that DARKS were taken at that exposure time.')
        sys.exit()
    if len(flat_list) == 0:
        print('ERROR: No FLAT frames detected. Check that you downloaded them properly.')
        sys.exit()
    if len(fpet_list) == 0:
        print('ERROR: No FPET,WAVE frames detected. Check that you downloaded them properly.')
        sys.exit()

    print('')
    print('---------')
    print('')


    #Write the DARK sof
    if not (outpath/"cal_dark").exists(): os.mkdir(outpath/"cal_dark")
    outF = open(outpath/"cal_dark/DARK.txt", "w")
    for line in dark_list:
        outF.write(line)
        outF.write("\n")
    outF.close()

    #Write the UTIL CALIB (FLAT) sof. Requires DARK, BPM and DETLIN (optional)
    if not (outpath/"util_calib_flat").exists(): os.mkdir(outpath/"util_calib_flat")
    outF = open(outpath/"util_calib_flat/CALIB.txt", "w")
    for line in flat_list:
        outF.write(line)
        outF.write("\n")
    darkfiles = glob.glob(str(outpath)+"/cal_dark/"+'cr2res_cal_dark_*_1.*_master.fits')
    bpmfiles = glob.glob(str(outpath)+"/cal_dark/"+'cr2res_cal_dark_*_1.*_bpm.fits')
    if len(darkfiles) < 1:
        raise Exception("No ~1.5 second master dark found for FLAT reduction.")
    if len(bpmfiles) < 1:
        raise Exception("No ~1.5 second master BPM found for FLAT reduction.")
    if len(darkfiles) > 1:
        raise Exception("More than 1 ~1.5 second master dark found for FLAT reduction??")
    if len(bpmfiles) > 1:
        raise Exception("More than 1 ~1.5 second master BPM found for FLAT reduction??")
    outF.write(bpmfiles[0]+' CAL_DARK_BPM')
    outF.write("\n")
    outF.write(darkfiles[0]+' CAL_DARK_MASTER')

    if len(detlin) > 0:
        outF.write(str(outpath)+"/detlin/cr2res_cal_detlin_coeffs.fits CAL_DETLIN_COEFFS")
        outF.write("\n")
    outF.close()

    #Write the UTIL_TRACE sof.
    if not (outpath/"util_trace").exists(): os.mkdir(outpath/"util_trace")
    outF = open(outpath/"util_trace/TRACE.txt", "w")
    outF.write(str(outpath)+"/util_calib_flat/cr2res_util_calib_calibrated_collapsed.fits UTIL_CALIB")
    outF.close()

    #Write the util_slit_curv sof.
    if not (outpath/"util_slit_curv").exists(): os.mkdir(outpath/"util_slit_curv")
    outF = open(outpath/"util_slit_curv/SLITCURV.txt", "w")
    outF.write(fpet_list[0])
    outF.write("\n")
    outF.write(str(outpath)+'/util_trace/cr2res_util_calib_calibrated_collapsed_tw.fits CAL_FLAT_TW')
    outF.close()





    #Write the FLAT sof. Requires DARK, BPM and DETLIN (optional)
    if not (outpath/"cal_flat").exists(): os.mkdir(outpath/"cal_flat")
    outF = open(outpath/"cal_flat/FLAT.txt", "w")
    for line in flat_list:
        outF.write(line)
        outF.write("\n")
    darkfiles = glob.glob(str(outpath)+"/cal_dark/"+'cr2res_cal_dark_*_1.*_master.fits')
    bpmfiles = glob.glob(str(outpath)+"/cal_dark/"+'cr2res_cal_dark_*_1.*_bpm.fits')
    if len(darkfiles) < 1:
        raise Exception("No ~1.5 second master dark found for FLAT reduction.")
    if len(bpmfiles) < 1:
        raise Exception("No ~1.5 second master BPM found for FLAT reduction.")
    if len(darkfiles) > 1:
        raise Exception("More than 1 ~1.5 second master dark found for FLAT reduction??")
    if len(bpmfiles) > 1:
        raise Exception("More than 1 ~1.5 second master BPM found for FLAT reduction??")
    outF.write(bpmfiles[0]+' CAL_DARK_BPM')
    outF.write("\n")
    outF.write(darkfiles[0]+' CAL_DARK_MASTER')

    if len(detlin) > 0:
        outF.write(str(outpath)+"/detlin/cr2res_cal_detlin_coeffs.fits CAL_DETLIN_COEFFS")
    outF.close()



def check_files_exist(sof_file):
    "This program reads the sof file prior to execution of the recipe, to make sure that all the dependent files actually exist. This is to prevent the recipe running for 3 hours and then crashing due to a missing file or a wrongly spelled filename somewhere. If the tag is spelled wrongly, well then hopefully the recipe itself will crash at the start."""
    import csv
    import os
    import sys

    f=open(sof_file,'r').read().splitlines()
    for line in f:
        if len(line.split()) > 2:#If there are spaces in the main path (DONT DO THIS) then we split on the .fits extension instead.
            filename = line.split('.fits')[0]+'.fits'
        else:
            filename=line.split()[0]
        exists=os.path.isfile(filename)
        if exists != True:
            print(f"ERROR IN RECIPE PATH FILE: {filename} is required for {str(sof_file)} but it doesn't exist. Check:")
            print("  1. Whether this is a static calibration file in your esorex installation that is named wrongly. (Could happen if those building the pipeline have changed the name of their static calibration files in a new version).")
            print("  2. That all required previous recipes were executed.")
            print("  3. That previous recipes produced the right output files, and that these were moved to the right (outpath) folder.")
            print("  4. That the recipe path file file was created correctly by create_sof (i.e. without typos).")
            sys.exit()

def move_to(filename,outpath,newname=None):
    import pdb
    """This short script moves a file at location filename to the folder outpath.
    If the newname keyword is set to a string, the file will also be renamed in the process.
    This moving overwrites existing files."""
    #I was lazy to type shutil.move all the time...
    import shutil
    from pathlib import Path
    outpath=Path(outpath)
    if newname == None:
        shutil.move(filename,outpath/filename)
    else:
        shutil.move(filename,outpath/newname)

    #==============================================================================================#
    #==============================================================================================#
    #What follows are the wrappers for the esorex recipes. These are executed one by one when
    #calling this script, all the way at the end of this file.
    #==============================================================================================#
    #==============================================================================================#


def detlin(outpath):
    import os
    from pathlib import Path
    print('==========>>>>> CREATING DETLIN COEFFICIENTS <<<<<==========')
    outpath = Path(outpath)
    sofpath = outpath/"detlin/DETLIN.txt"
    check_files_exist(sofpath)
    os.system('esorex '+' --output-dir='+str(outpath/'detlin/')+' cr2res_cal_detlin '+str(sofpath))

def master_dark(outpath):
    """This is a wrapper for the cal_dark recipe."""
    import os
    from pathlib import Path
    print('==========>>>>> CREATING MASTER DARK AND BAD PIXEL MAP <<<<<==========')
    outpath = Path(outpath)
    sofpath = outpath/"cal_dark/DARK.txt"
    check_files_exist(sofpath)
    os.system('esorex '+' --output-dir='+str(outpath/'cal_dark/')+' cr2res_cal_dark '+str(sofpath))

def util_calib_flat(outpath):
    """This is a wrapper for the util_calib recipe."""
    import os
    from pathlib import Path
    print('==========>>>>> CREATING MASTER FLAT <<<<<==========')
    outpath = Path(outpath)
    sofpath = outpath/"util_calib_flat/CALIB.txt"
    check_files_exist(sofpath)
    os.system('esorex '+' --output-dir='+str(outpath/'util_calib_flat/')+' cr2res_util_calib --collapse="MEAN" '+str(sofpath))

def util_trace(outpath):
    """This is a wrapper for the util_trace recipe."""
    import os
    from pathlib import Path
    print('==========>>>>> CREATING TRACE <<<<<==========')
    outpath = Path(outpath)
    sofpath = outpath/"util_trace/TRACE.txt"
    check_files_exist(sofpath)
    os.system('esorex '+' --output-dir='+str(outpath/'util_trace/')+' cr2res_util_trace '+str(sofpath))

def util_slit_curv(outpath):
    """This is a wrapper for the util_slit_curv recipe."""
    import os
    from pathlib import Path
    print('==========>>>>> CREATING SLIT MAP <<<<<==========')
    outpath = Path(outpath)
    sofpath = outpath/"util_slit_curv/SLITCURV.txt"
    check_files_exist(sofpath)
    os.system('esorex '+' --output-dir='+str(outpath/'util_slit_curv/')+' cr2res_util_slit_curv '+str(sofpath))



def master_flat(outpath):
    """This is a wrapper for the cal_flat recipe."""
    import os
    from pathlib import Path
    print(os.getcwd())
    print('==========>>>>> CREATING MASTER FLAT <<<<<==========')
    outpath = Path(outpath)
    sofpath = outpath/"cal_flat/FLAT.txt"
    check_files_exist(sofpath)
    os.system('esorex '+' --output-dir='+str(outpath/'cal_flat/')+' cr2res_cal_flat '+str(sofpath))



inpath = '/data/jens/observations/55-cnc/dayside_crires_raw_night4'
outpath = 'test'

create_sof(inpath,outpath,detlin='/data/jens/observations/55-cnc/detlin/')
# detlin(outpath)
# master_dark(outpath)
# util_calib_flat(outpath)
# util_trace(outpath)
util_slit_curv(outpath)
