def print_raw_list(inpath):
    import os
    import astropy.io.fits as fitsio
    from pathlib import Path
    import numpy as np
    fits_list = os.listdir(inpath)
    fits_list = [str(i) for i in Path(inpath).glob('CRIRE*.fits')]
    static_list = [str(i) for i in Path(inpath).glob('M.CRIRE*.fits')]
    static_type_list=[]
    type_list=[]
    dits_list = []
    for file in fits_list:
        with fitsio.open(file) as fu:
            type_list.append(fu[0].header['HIERARCH ESO DPR TYPE'])
            dits_list=np.append(dits_list,fu[0].header['EXPTIME'])
    for file in static_list:
        with fitsio.open(file) as fu:
            static_type_list.append(fu[0].header['ESO PRO CATG'])

    for i in range(len(fits_list)):
        print(fits_list[i].split('/')[-1],type_list[i]+'\t\t\t',dits_list[i])
    print('')
    for i in range(len(static_list)):
        print(static_list[i].split('/')[-1],static_type_list[i]+'\t\t\t')


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
        # print(f'Creating detlin sof using files located in {detlin}')
        detlinpath = Path(detlin)

        detlin_list = os.listdir(detlinpath)
        detlin_list = [str(i) for i in Path(detlinpath).glob('CRIRE*.fits')]
        for d in detlin_list:
            with fitsio.open(d) as fu:
                detlin_type_list.append(fu[0].header['HIERARCH ESO DPR TYPE'])

        detlin_dark_list = []
        detlin_lamp_list = []
        for i in range(len(detlin_list)):
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
    une_list=[]
    emission_list=[]
    sci_list=[]
    sci_A_list=[]
    sci_B_list=[]

    for i in range(len(fits_list)):
        if type_list[i] == 'DARK':
            dark_list = np.append(dark_list,fits_list[i]+'   '+type_list[i])
        if type_list[i] == 'FLAT':
            flat_list = np.append(flat_list,fits_list[i]+'   '+type_list[i])
        if type_list[i] == 'WAVE,FPET':
            fpet_list = np.append(fpet_list,fits_list[i]+'   WAVE_FPET')
        if type_list[i] == 'WAVE,UNE':
            une_list = np.append(une_list,fits_list[i]+'   WAVE_UNE')
        if type_list[i] == 'OBJECT':
            sci_list = np.append(sci_list,fits_list[i]+'   OBS_STARING_JITTER')

    for i in range(len(static_list)):
        if static_type_list[i] == 'EMISSION_LINES':
            emission_list = np.append(emission_list,static_list[i]+'   EMISSION_LINES')


    # print('')
    # for i in range(len(static_list)):
    #     print(static_list[i].split('/')[-1],static_type_list[i])


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
    if len(une_list) == 0:
        print('ERROR: No UNE,WAVE frames detected. Check that you downloaded them properly.')
        print('UNE (Uranium-Neon) frames may not be found by the calselector so its possible '
        'that you have had to download it manually.')
        sys.exit()
    if len(emission_list) == 0:
        print('ERROR: No EMISSION_LINES frames detected. This is a static calibration file.')
        print("Check that you have downloaded it properly.")
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


    #Write the util_extract_calib sof. Extract the slit model?
    if not (outpath/"util_extract_calib").exists(): os.mkdir(outpath/"util_extract_calib")
    outF = open(outpath/"util_extract_calib/EXTRACT_CALIB.txt", "w")
    outF.write(str(outpath)+"/util_calib_flat/cr2res_util_calib_calibrated_collapsed.fits UTIL_CALIB")
    outF.write("\n")
    outF.write(str(outpath)+'/util_slit_curv/cr2res_util_calib_calibrated_collapsed_tw_tw.fits UTIL_SLIT_CURV_TW')
    outF.close()


    #Normflat
    if not (outpath/"util_normflat").exists(): os.mkdir(outpath/"util_normflat")
    outF = open(outpath/"util_normflat/NORMFLAT.txt", "w")
    outF.write(str(outpath)+"/util_calib_flat/cr2res_util_calib_calibrated_collapsed.fits UTIL_CALIB")
    outF.write("\n")
    outF.write(str(outpath)+'/util_extract_calib/cr2res_util_calib_calibrated_collapsed_extrModel.fits UTIL_SLIT_MODEL')
    outF.close()


    #Write the UNE sof.
    if not (outpath/"util_calib_une").exists(): os.mkdir(outpath/"util_calib_une")
    outF = open(outpath/"util_calib_une/CALIB.txt", "w")
    if len(detlin) > 0:
        outF.write(str(outpath)+"/detlin/cr2res_cal_detlin_coeffs.fits CAL_DETLIN_COEFFS")
        outF.write("\n")
    outF.write(une_list[0])
    outF.write("\n")
    darkfiles = glob.glob(str(outpath)+"/cal_dark/"+'cr2res_cal_dark_*_120*_master.fits')
    bpmfiles = glob.glob(str(outpath)+"/cal_dark/"+'cr2res_cal_dark_*_120*_bpm.fits')
    if len(darkfiles) < 1:
        raise Exception("No 120 second master dark found for FLAT reduction.")
    if len(bpmfiles) < 1:
        raise Exception("No 120 second master BPM found for FLAT reduction.")
    if len(darkfiles) > 1:
        raise Exception("More than 1 120 second master dark found for FLAT reduction??")
    if len(bpmfiles) > 1:
        raise Exception("More than 1 120 second master BPM found for FLAT reduction??")
    outF.write(bpmfiles[0]+' CAL_DARK_BPM')
    outF.write("\n")
    outF.write(darkfiles[0]+' CAL_DARK_MASTER')
    outF.write("\n")
    outF.write(str(outpath)+"/util_normflat/cr2res_util_normflat_Open_master_flat.fits CAL_FLAT_MASTER")
    outF.close()


    #Write the util_extract_calib sof. Extract wave UNE
    if not (outpath/"util_extract_une").exists(): os.mkdir(outpath/"util_extract_une")
    outF = open(outpath/"util_extract_une/EXTRACT_UNE.txt", "w")
    outF.write(str(outpath)+"/util_calib_une/cr2res_util_calib_calibrated_collapsed.fits UTIL_CALIB")
    outF.write("\n")
    outF.write(str(outpath)+'/util_slit_curv/cr2res_util_calib_calibrated_collapsed_tw_tw.fits UTIL_SLIT_CURV_TW')
    outF.close()


    if not (outpath/"util_wave").exists(): os.mkdir(outpath/"util_wave")
    outF = open(outpath/"util_wave/WAVE.txt", "w")
    outF.write(str(outpath)+'/util_extract_une/cr2res_util_calib_calibrated_collapsed_extr1D.fits UTIL_EXTRACT_1D')
    outF.write("\n")
    outF.write(str(outpath)+'/util_slit_curv/cr2res_util_calib_calibrated_collapsed_tw_tw.fits UTIL_SLIT_CURV_TW')
    outF.write("\n")
    outF.write(emission_list[0])
    outF.close()






    #Write the FPET sof.
    if not (outpath/"util_calib_fpet").exists(): os.mkdir(outpath/"util_calib_fpet")
    outF = open(outpath/"util_calib_fpet/CALIB.txt", "w")
    if len(detlin) > 0:
        outF.write(str(outpath)+"/detlin/cr2res_cal_detlin_coeffs.fits CAL_DETLIN_COEFFS")
        outF.write("\n")
    outF.write(fpet_list[0])
    outF.write("\n")
    darkfiles = glob.glob(str(outpath)+"/cal_dark/"+'cr2res_cal_dark_*_120*_master.fits')
    bpmfiles = glob.glob(str(outpath)+"/cal_dark/"+'cr2res_cal_dark_*_120*_bpm.fits')
    if len(darkfiles) < 1:
        raise Exception("No 120 second master dark found for FLAT reduction.")
    if len(bpmfiles) < 1:
        raise Exception("No 120 second master BPM found for FLAT reduction.")
    if len(darkfiles) > 1:
        raise Exception("More than 1 120 second master dark found for FLAT reduction??")
    if len(bpmfiles) > 1:
        raise Exception("More than 1 120 second master BPM found for FLAT reduction??")
    outF.write(bpmfiles[0]+' CAL_DARK_BPM')
    outF.write("\n")
    outF.write(darkfiles[0]+' CAL_DARK_MASTER')
    outF.write("\n")
    outF.write(str(outpath)+"/util_normflat/cr2res_util_normflat_Open_master_flat.fits CAL_FLAT_MASTER")
    outF.close()

    #Write the util_extract_calib sof. Extract wave FPET
    if not (outpath/"util_extract_fpet").exists(): os.mkdir(outpath/"util_extract_fpet")
    outF = open(outpath/"util_extract_fpet/EXTRACT_FPET.txt", "w")
    outF.write(str(outpath)+"/util_calib_fpet/cr2res_util_calib_calibrated_collapsed.fits UTIL_CALIB")
    outF.write("\n")
    outF.write(str(outpath)+'/util_slit_curv/cr2res_util_calib_calibrated_collapsed_tw_tw.fits UTIL_SLIT_CURV_TW')
    outF.close()

    if not (outpath/"util_wave_fpet").exists(): os.mkdir(outpath/"util_wave_fpet")
    outF = open(outpath/"util_wave_fpet/WAVE.txt", "w")
    outF.write(str(outpath)+'/util_extract_fpet/cr2res_util_calib_calibrated_collapsed_extr1D.fits UTIL_EXTRACT_1D')
    outF.write("\n")
    outF.write(str(outpath)+'/util_slit_curv/cr2res_util_calib_calibrated_collapsed_tw_tw.fits UTIL_SLIT_CURV_TW')
    outF.close()



    if not (outpath/"obs_staring").exists(): os.mkdir(outpath/"obs_staring")
    for i in range(len(sci_list)):
        outF = open(outpath/f"obs_staring/SCI_{i}.txt", "w")
        outF.write(sci_list[i])
        outF.write("\n")
        outF.write(str(outpath)+'/util_slit_curv/cr2res_util_calib_calibrated_collapsed_tw_tw.fits UTIL_SLIT_CURV_TW')
        outF.write("\n")
        if len(detlin) > 0:
            outF.write(str(outpath)+"/detlin/cr2res_cal_detlin_coeffs.fits CAL_DETLIN_COEFFS")
            outF.write("\n")
        outF.write(bpmfiles[0]+' CAL_DARK_BPM')
        outF.write("\n")
        outF.write(darkfiles[0]+' CAL_DARK_MASTER')
        outF.write("\n")
        outF.write(str(outpath)+"/util_normflat/cr2res_util_normflat_Open_master_flat.fits CAL_FLAT_MASTER")
        #I do not add the blaze function on purpose.
        outF.close()

    if not (outpath/"obs_nodding").exists(): os.mkdir(outpath/"obs_nodding")
    for i in range(len(sci_list_A)):
        outF = open(outpath/f"obs_nodding/SCI_{i}.txt", "w")
        outF.write(sci_A_list[i])
        outF.write(sci_B_list[i])
        outF.write("\n")
        outF.write(str(outpath)+'/util_slit_curv/cr2res_util_calib_calibrated_collapsed_tw_tw.fits UTIL_SLIT_CURV_TW')
        outF.write("\n")
        if len(detlin) > 0:
            outF.write(str(outpath)+"/detlin/cr2res_cal_detlin_coeffs.fits CAL_DETLIN_COEFFS")
            outF.write("\n")
        outF.write(bpmfiles[0]+' CAL_DARK_BPM')
        outF.write("\n")
        outF.write(darkfiles[0]+' CAL_DARK_MASTER')
        outF.write("\n")
        outF.write(str(outpath)+"/util_normflat/cr2res_util_normflat_Open_master_flat.fits CAL_FLAT_MASTER")
        #I do not add the blaze function on purpose.
        outF.close()



    #Write the FLAT sof. Requires DARK, BPM and DETLIN (optional)
    # if not (outpath/"cal_flat").exists(): os.mkdir(outpath/"cal_flat")
    # outF = open(outpath/"cal_flat/FLAT.txt", "w")
    # for line in flat_list:
    #     outF.write(line)
    #     outF.write("\n")
    # darkfiles = glob.glob(str(outpath)+"/cal_dark/"+'cr2res_cal_dark_*_1.*_master.fits')
    # bpmfiles = glob.glob(str(outpath)+"/cal_dark/"+'cr2res_cal_dark_*_1.*_bpm.fits')
    # if len(darkfiles) < 1:
    #     raise Exception("No ~1.5 second master dark found for FLAT reduction.")
    # if len(bpmfiles) < 1:
    #     raise Exception("No ~1.5 second master BPM found for FLAT reduction.")
    # if len(darkfiles) > 1:
    #     raise Exception("More than 1 ~1.5 second master dark found for FLAT reduction??")
    # if len(bpmfiles) > 1:
    #     raise Exception("More than 1 ~1.5 second master BPM found for FLAT reduction??")
    # outF.write(bpmfiles[0]+' CAL_DARK_BPM')
    # outF.write("\n")
    # outF.write(darkfiles[0]+' CAL_DARK_MASTER')
    #
    # if len(detlin) > 0:
    #     outF.write(str(outpath)+"/detlin/cr2res_cal_detlin_coeffs.fits CAL_DETLIN_COEFFS")
    # outF.close()

















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
