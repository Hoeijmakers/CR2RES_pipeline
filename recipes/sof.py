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


def create_sof(inpath,outpath,dit=0,detlin='',pattern='A',remake_bg=True):
    """This script creates the file association lists (sof files) that are the main inputs
    to the pipeline recipes when called with esorex. The user provides the path of the raw data
    foe;s (inpath) as downloaded from the ESO archive. These must be sorted by instrument mode
    (i.e. use the same grating and nodding strategy). The user provides the output path, to which
    the sof files will be written (outpath).  This is also the location in which the pipeline
    reduction products will be stored. Finally, the user manually provides the exposure time they
    expect (in case of DARK and OBJECT frames with multiple exposures).


    Set the detlin parameter to a path where you have downloaded the detector linearity raw data
    for use with the cal_detlin recipe. This is optional though.

    Set the pattern keyword to determine whether (and what type of) nodding sequence this is, in
    preparation of using the obs_nodding recipe. This should be set to either 'A', 'AB', or 'ABBA'.
    """
    import os
    import numpy as np
    import astropy.io.fits as fitsio
    import pdb
    import sys
    from pathlib import Path
    import glob
    import copy

    outpath=Path(outpath)

    force = True
    if not outpath.exists():
        os.mkdir(outpath)
    else:
        if not force:
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
    sci_filename_list = []
    sci_A_list=[]
    sci_B_list=[]
    nodpos_list = []
    mjd_list = []


    #Sort out science types.
    #This may currently not work for STARING observations, if they dont get a NODPOS.
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
            with fitsio.open(fits_list[i]) as hdul:
                h = hdul[0].header
                catg = h['HIERARCH ESO DPR CATG']
                if catg == 'SCIENCE':
                    if pattern != 'A':
                        nodpos_list.append(h['HIERARCH ESO SEQ NODPOS'])
                    mjd_list.append(float(h['MJD-OBS']))
                    sci_list = np.append(sci_list,fits_list[i])

    mjd_list = np.array(mjd_list)
    sorting = np.argsort(mjd_list)

    sci_list_sorted,mjd_list_sorted = [],[]

    if pattern != 'A':
        nodding_positions,nodpos_list_sorted,sci_list_A,sci_list_B = [],[],[],[]

    for i in sorting:
        sci_list_sorted.append(sci_list[i])
        mjd_list_sorted.append(mjd_list[i])
        if pattern != 'A':
            nodpos_list_sorted.append(nodpos_list[i])
            print(sci_list[i].split('/')[-1],mjd_list[i],nodpos_list[i])





    # Here we identify the indices and filenames of continuous nodding sequences:
    if pattern != 'A':
        current_pos,current_sequence,nodding_indices = nodpos_list_sorted[0],[0],[]
        for i in range(1,len(nodpos_list_sorted)):
            if nodpos_list_sorted[i] == current_pos:
                current_sequence.append(i)
            else:
                nodding_indices.append(current_sequence)
                current_pos = nodpos_list_sorted[i]
                current_sequence = [i]
        nodding_indices.append(current_sequence)
        if pattern == 'ABBA':
            def split_list(lst):
                half = len(lst) // 2
                first_half = lst[:half]
                second_half = lst[half:]
                return first_half, second_half
            nodding_indices_split = [nodding_indices[0]]
            for i in range(1,len(nodding_indices)-1):
                for half in split_list(nodding_indices[i]):
                    nodding_indices_split.append(half)
            nodding_indices_split.append(nodding_indices[-1])
            nodding_indices = nodding_indices_split



        #THIS CURRENTLY ONLY WORKS FOR ABBA
        if not (outpath/"obs_nodding").exists(): os.mkdir(outpath/"obs_nodding")
        if not (outpath/"obs_nodding/median_bgs").exists(): os.mkdir(outpath/"obs_nodding/median_bgs")
        with open(outpath/"obs_nodding/nodpos.txt",'w') as npf:
            npf.write('')
        for i in range(len(nodpos_list_sorted)):
            with open(outpath/"obs_nodding/nodpos.txt",'a') as npf:
                npf.write(str(i)+'  '+str(nodpos_list_sorted[i])+'   '+sci_list_sorted[i]+'   '+str(mjd_list_sorted[i])+"\n")


        n_nods = len(nodding_indices)
        bg_nods = []
        z = 0
        for I in nodding_indices:
            bg_outpath = outpath/f"obs_nodding/median_bgs/{z}_{nodpos_list_sorted[I[0]]}x{len(I)}.fits"
            if remake_bg:
                stack1,stack2,stack3,hdrs,h1,h2,h3,hduls = [],[],[],[],[],[],[],[]
                for k,i in enumerate(I):
                    with fitsio.open(sci_list_sorted[i]) as hdul:
                        stack1.append(hdul[1].data)
                        stack2.append(hdul[2].data)
                        stack3.append(hdul[3].data)
                        hdrs.append(hdul[0].header)
                        h1.append(hdul[1].header)
                        h2.append(hdul[2].header)
                        h3.append(hdul[3].header)
                        if k == 0:
                            hdul_out = copy.deepcopy(hdul)

                M1 = np.nanmedian(stack1,axis=0)
                M2 = np.nanmedian(stack2,axis=0)
                M3 = np.nanmedian(stack3,axis=0)
                hdr_out = hdul_out[0].header
                for k,i in enumerate(I):
                    hdr_out.set(f'frame{k+1}',sci_list_sorted[i].split('/')[-1])

                hdul_out[1].data = M1
                hdul_out[2].data = M2
                hdul_out[3].data = M3
                # hdul_out = fitsio.HDUList([fitsio.PrimaryHDU(np.array(0),header=hdr_out),
                #                             fitsio.ImageHDU(M1,header=h1[0]),
                #                             fitsio.ImageHDU(M2,header=h2[0]),
                #                             fitsio.ImageHDU(M3,header=h3[0])])
                hdul_out.writeto(bg_outpath,overwrite=True)
            bg_nods.append(bg_outpath)
            print(f'Done frame {z+1} from {n_nods}')
            z+=1



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
    for i in range(len(sci_list_sorted)):
        outF = open(outpath/f"obs_staring/SCI_{i}.txt", "w")
        outF.write(sci_list_sorted[i]+'   OBS_STARING_JITTER')
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







    if pattern == 'ABBA':
        if not (outpath/"obs_nodding/output/").exists(): os.mkdir(outpath/"obs_nodding/output/")
        k=0
        for z,I in enumerate(nodding_indices):
            for i in I:
                outF = open(outpath/f"obs_nodding/SCI_{k}.txt", "w")
                outF.write(sci_list_sorted[i]+'   OBS_NODDING_JITTER')
                outF.write("\n")
                if z%2==0:
                    outF.write(str(bg_nods[z+1])+'   OBS_NODDING_JITTER')
                if z%2==1:
                    outF.write(str(bg_nods[z-1])+'   OBS_NODDING_JITTER')
                outF.write("\n")
                outF.write(str(outpath)+'/util_slit_curv/cr2res_util_calib_calibrated_collapsed_tw_tw.fits UTIL_SLIT_CURV_TW')
                outF.write("\n")
                if len(detlin) > 0:
                    outF.write(str(outpath)+"/detlin/cr2res_cal_detlin_coeffs.fits CAL_DETLIN_COEFFS")
                    outF.write("\n")
                outF.write(bpmfiles[0]+' CAL_DARK_BPM')
                outF.write("\n")
                # outF.write(darkfiles[0]+' CAL_DARK_MASTER') #Not needed because it self-subtracts?
                # outF.write("\n")
                outF.write(str(outpath)+"/util_normflat/cr2res_util_normflat_Open_master_flat.fits CAL_FLAT_MASTER")
                #I do not add the blaze function on purpose.
                outF.close()
                k+=1



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
