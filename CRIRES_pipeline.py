def create_sof(inpath,outpath,dit=0):
    """This script creates the file association lists (sof files) that are the main inputs
    to the pipeline recipes when called with esorex. The user provides the path of the raw data
    foe;s (inpath) as downloaded from the ESO archive. These must be sorted by instrument mode
    (i.e. use the same grating and nodding strategy). The user provides the output path, to which
    the sof files will be written (outpath).  This is also the location in which the pipeline
    reduction products will be stored. Finally, the user manually provides the exposure time they
    expect (in case of DARK and OBJECT frames with multiple exposures).

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
        "might happen [y/N]")
        if really.lower()=='y':
            pass
        else:
            sys.exit()

    fits_list = os.listdir(inpath)
    fits_list = [str(i) for i in Path(inpath).glob('CRIRE*.fits')]
    static_list = [str(i) for i in Path(inpath).glob('M.CRIRE*.fits')]


    type_list=[]
    static_type_list=[]
    dits_list = []

    for file in static_list:
        with fitsio.open(file) as fu:
            static_type_list.append(fu[0].header['ESO PRO CATG'])
    for file in fits_list:
        with fitsio.open(file) as fu:
            type_list.append(fu[0].header['HIERARCH ESO DPR TYPE'])
            dits_list=np.append(dits_list,fu[0].header['EXPTIME'])






    dark_list=[]
    sci_A_list=[]

    for i in range(len(fits_list)):
        print(fits_list[i].split('/')[-1],type_list[i]+'\t\t\t',dits_list[i])
        if type_list[i] == 'DARK' and (dit==0 or dit==dits_list[i]):
            dark_list = np.append(dark_list,fits_list[i]+'   '+type_list[i])#+'   %s' % dits_list[i])


    if len(dark_list) == 0:
        print('ERROR: No DARK frames detected. Check that you downloaded them properly and that.'
        'if you have set a DIT requirement, that DARKS were taken at that exposure time.')
        sys.exit()

    print('')
    print('---------')
    print('')
    print(dark_list)


    if not (outpath/"cal_dark").exists(): os.mkdir(outpath/"cal_dark")
    outF = open(outpath/"cal_dark/DARK.txt", "w")
    for line in dark_list:
        outF.write(line)
        outF.write("\n")
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


def master_dark(outpath):
    """This is a wrapper for the mdark recipe."""
    import os
    from pathlib import Path
    print('==========>>>>> CREATING MASTER DARK AND HOT PIXEL MAP<<<<<==========')
    outpath = Path(outpath)
    check_files_exist(outpath/"cal_dark/DARK.txt")
    os.system("cd "+str(outpath/'cal_dark/')+"; esorex cr2res_cal_dark DARK.txt")




inpath = '/data/jens/observations/55-cnc/dayside_crires_raw_night4'
outpath = 'test'

create_sof(inpath,outpath,dit=0)
master_dark(outpath)
