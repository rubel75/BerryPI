#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Calculation of Wannier charge centers evolution in a plane.
The plane and WCC direction are defined in the user_input() section below.
See prolog() for more details about the calculation setup.
Results are tabulated in the 'wcc.csv' file.

@author: Oleg Rubel
"""

import pandas as pd
import subprocess
import os
import numpy as np
import re
from pathlib import Path


def get_bands_from_file(file_path: Path) -> pd.DataFrame:
    """function to parse bands from the file
    
    pattern is defined as follows:
    ^band: Line starts with the word "band".
    \s+: One or more spaces after "band".
    \d+: An integer (band number).
    [-+]?\d*\.\d+: Matches a floating-point number (optionally with a sign).

    Parameters
    ----------
    file_path : Path
        path to file
    """

    pattern = r"^band\s+(\d+)\s+([-+]?\d*\.\d+)\s+([-+]?\d*\.\d+)\s+([-+]?\d*\.\d+)[Dd]([-+]?\d+)$"
    data = []
    with open(file_path, "r") as output_file:
        for line in output_file:
            # If the line matches the pattern, add it to the list.
            match = re.match(pattern, line.strip())
            if match:
                # Extract groups and convert them to appropriate types (int for band number, float for values).
                band_number = int(match.group(1))
                emin = float(match.group(2))
                emax = float(match.group(3))
                occupancy = float(match.group(4)) * (10 ** int(match.group(5)))
                data.append((band_number, emin, emax, occupancy))

    band_df = pd.DataFrame(data, columns=["Band Number", "emin", "emax", "occupancy"])
    band_df.to_csv(file_path.with_suffix(suffix=".csv"))
    
    return band_df

def find_edge_bands(band_df, band_gap_threshold = 0.01):
    """finds edge bands by 
    - identifying the twin bands and bands with no overlap in 
      energy with the subsequent band. 
    - then finding the bands that satisfy both conditions and 
      identifying them as a shell change
    - sorting these bands by their emax centered on 0 
    - picking the 2 closest bands to zero, in order of low 
    band number to high

    Parameters
    ----------
    band_df : pd.DataFrame
        dataframe with all parameters describing bands -
        Band number, emin, emax, occupancy

    band_gap_threshold : float
        threshold between bands to ensure that overlap is determined
        outside margin of error in band energy calculation
    Returns
    -------
    Tuple
        Band lower bound and upper bound
    """
    # check if band structure occupancies indicates metal
    metal_band_occupancy = not band_df['occupancy'].isin([0, 1]).all()
    if metal_band_occupancy:
        raise ValueError("band occupancies indicate metallic nature!\n Aborting Calculations")

    band_df["next_band_overlap"] = band_df["emax"] > (band_df["emin"].shift(-1) - band_gap_threshold)
    band_df["twin_band"] = band_df["emax"] == band_df["emax"].shift(-1)
    band_df["non_overlap_band"] = ~(band_df["next_band_overlap"] | band_df["twin_band"])

    upper_band = band_df[band_df["occupancy"] == 1].max()["Band Number"]
    non_overlap_band = band_df[band_df["non_overlap_band"] == True]
    lower_band = (
        non_overlap_band[
            non_overlap_band["occupancy"] == 1
            ]
            )["Band Number"].nlargest(2).iloc[-1] + 1
    
    return [lower_band, upper_band]

def get_bands_from_output(specified_bands, band_gap_threshold = 0.01):
    working_directory = Path.cwd()
    case_name = working_directory.stem
    output2_file = working_directory.joinpath(
                                        Path(case_name).with_suffix(".output2")
                                        )
    
    # Display the results
    if output2_file.exists():
        print("File ending with .output2 found:", output2_file)
        band_df = get_bands_from_file(file_path=output2_file)
        band_pair_from_output = find_edge_bands(band_df, band_gap_threshold) #change band overlap threshold here

        if band_pair_from_output != specified_bands and specified_bands is not None:
            print("WARNING: provided bands do not match output2 file")
            print(f"WARNING: provided range {specified_bands} does not match detected bands {band_pair_from_output}")
            print("WARNING: values in bands (user specified) will prevail")
        elif specified_bands is None:
            print(f"output2 file parsed, selected bands are {band_pair_from_output}")
            return band_pair_from_output

    else:
        print("WARNING: No .output2 files found in the working directory.")
        if specified_bands is None:
            raise ValueError("ERROR: output2 (band data) file not found")
        print("WARNING: Selecting bands provided by user")

    print(f"Selected bands are {band_pair_from_output}")
    return specified_bands


    
def user_input():
    """Editable section where users define their input"""
    kevoldir = 2 # Y
    kevol = [0, 0.5] # start and end in fraction of the corresponding reciprocal lattice vector G[kevoldir]
    nkevol = 20 # discretization intervals
    kwlsndir = 3 # Z, different from kevoldir
    nkwlsn = 10 # discretization intervals
    kfix = 0.0 # in fraction of reciprocal lattice vectors G[kfixdir]
    bands = None # can provide values explicitly here as [lower_band, upper_band]
    band_gap_threshold = 0.01 # specify band gap threshold (Ry) for two bands considered separated by the gap
    bands = get_bands_from_output(bands, band_gap_threshold)
    parallel = True # parallel option [-p] in BerryPI (needs a proper .machines file)
    spinpolar = False # [-sp] in BerryPI
    orbital = False # [-orb] in BerryPI

    return kevoldir, kevol, nkevol, kwlsndir, nkwlsn, kfix, bands, parallel, spinpolar, orbital

def preliminary():
    if os.environ.get('WIENROOT')==None:
        msg = "The environment variable WIENROOT is not set. "+\
                "It should be set and point to the WIEN2k installation "+\
                "directory for proper functioning of WIEN2k."
        raise RuntimeError(msg)
    try:
        WorkingDir = os.getcwd()
        print ("Working directory = %s" %(WorkingDir))
        KlistFileName = str("%s.klist" %(WorkingDir.split('/')[-1]))
        mult = 100000000 # User independent
    except ValueError:
        print ("Error: Value Error")
        
    return (WorkingDir, KlistFileName, mult)

def prolog():
    txt="""
Calculate Wannier charge centers (WCCs) for a plane in k space defined as 
(kfix, kevol=var, kwcc=var)

kwlsn:
    This is a direction in k space along which we construct a closed Wilson loop
    and later evaluate WCCs on that loop. It can be 1 for X, 2 for Y, or 3 for Z.
kevol:
    This direction is perpendicular to kwcc. The Wilson loop will advance in this
    direction. Later we will plot WCCs vs the k coordinate in this direction.
kfix:
    This is a k value for the fixed dimension of the plane

Schematic Wilson loop of n k-points in kwlsn direction:

* k(1) + G[dir. kwlsn]
|
* k(n)
|
* ...
|
* k(2)
|
* k(1)

Here G[dir. kwlsn] is the reciprocal lattice vector in the direction of Wilson
loop. We evaluate WCCs for the loop and store in a temporary file wcc_i.csv
There will be as many WCCs as many bands are considered in BerryPI (-b option).

Next, we advance the Wislon loop in the kevol direction and compute WCCs again.
Multiple Wilson loops form a plane.

*--*--*--*--*--*--*
|  |  |  |  |  |  |
*  *  *  *  *  *  *
|  |  |  |  |  |  |
*  *  *  *  *  *  *
|  |  |  |  |  |  |
*  *  *  *  *  *  *   ^
|  |  |  |  |  |  |   |
*--*--*--*--*--*--*   kwlsn dir.

kevol dir. ->
(kfix is perpendicular to the screen)

After each step along kevol, data from wcc_i.csv are accumulated in the wcc.csv 
file."""
    print(txt)

def epilog():
    txt="""
Results (evolution of Wannier charge centers) are stored in the 'wcc.csv' 
file. Please check headings for more explanation about the content.
Use your favorite software to plot evolution of WCCs vs k.

Suggested references:
[1] C. Sgiarovello, M. Peressi, and R. Resta
    "Electron localization in the insulating state: Application to crystalline semiconductors"
    Phys. Rev. B 64, 115202 (2001)
    https://doi.org/10.1103/PhysRevB.64.115202
    (this paper first introduced hybrid WCCs)
[2] S.J.Ahmed, J.Kivinen, B.Zaporzan, L.Curiel, S.Pichardo and O.Rubel
    "BerryPI: A software for studying polarization of crystalline solids with 
    WIEN2k density functional all-electron package"
    Comp. Phys. Commun. 184, 647 (2013)
    https://doi.org/10.1016/j.cpc.2012.10.028
    (our implementation for Berry phase calculation in WIEN2k)
[3] D. Gresch, G. Autès, O. V. Yazyev, M. Troyer, D. Vanderbilt, B. A. Bernevig, and A. A. Soluyanov
    "Z2Pack: Numerical implementation of hybrid Wannier centers for identifying topological materials"
    Phys. Rev. B 95, 075146 (2017)
    https://doi.org/10.1103/PhysRevB.95.075146
    (this work inspired our WCC implementation)

Questions and comments are to be communicated via the WIEN2k mailing list
(see http://susi.theochem.tuwien.ac.at/reg_user/mailing_list)"""
    print(txt)

# MAIN
if __name__=="__main__":
    # Set user parameters
    kevoldir, kevol, nkevol, kwlsndir, nkwlsn, kfix,\
            bands, parallel, spinpolar, orbital = user_input()
    # Check input
    if not(kevoldir in [1, 2, 3]):
        raise ValueError(f'kevoldir={kevoldir}, while expected one of [1,2,3]')
    elif not(kwlsndir in [1, 2, 3]):
        raise ValueError(f'kwlsndir={kwlsndir}, while expected one of [1,2,3]')
    elif kevoldir == kwlsndir:
        raise ValueError(f'kwlsndir={kwlsndir} is the same as kwlsndir={kwlsndir}, while expected to be different')
    if not(type(kevol) == list):
        raise ValueError(f'kevol should be type list, while you have {type(kevol)}')
    elif not(len(kevol) == 2):
        raise ValueError(f'kevol list should have length = 2, while you have {len(kevol)}')
    if not(type(nkevol) == int):
        raise ValueError(f'nkevol should be type int, while you have {type(nkevol)}')
    elif not(nkevol >= 1):
        raise ValueError(f'nkevol should be at lest 1, while you have {nkevol}')
    if not(type(nkwlsn) == int):
        raise ValueError(f'nkwlsn should be type int, while you have {type(nkwlsn)}')
    elif not(nkwlsn >= 1):
        raise ValueError(f'nkwlsn should be at lest 1, while you have {nkwlsn}')
    # Evaluate missing inport
    kfixdir = set([1,2,3])-set([kevoldir,kwlsndir])
    kfixdir = list(kfixdir)
    kfixdir = kfixdir[0]
    if parallel:
        poption = '-p'
    else:
        poption = ''
    if spinpolar:
        spoption = '-sp'
    else:
        spoption = ''
    if orbital:
        orboption = '-orb'
    else:
        orboption = ''
    # Print input
    prolog() # print some info for the user
    print("User input:")
    print(f'kevoldir={kevoldir}, kwlsndir={kwlsndir}, kfixdir={kfixdir}')
    print(f'kevol range={kevol} with {nkevol} intervals')
    print(f'Wilson loop will use {nkwlsn} intervals')
    print(f'Band range from {bands[0]} to {bands[1]}')
    if parallel:
        print(f'Parallel option [{poption}] will be used in BerryPI call')
    if spinpolar:
        print(f'Spin-polarization option [{spoption}] will be used in BerryPI call')
    if orbital:
        print(f'Orbital potential option [{orboption}] will be used in BerryPI call')
    k = [0,0,0] # init k plane list
    k[kfixdir-1] = kfix
    k[kevoldir-1] = 'var evol'
    k[kwlsndir-1] = 'var Wloop'
    print(f'Plane is fixed at k={k}')
    WorkingDir, KlistFileName, mult = preliminary()
    # remove the result file to get a fresh start
    subprocess.call("rm -f %s"%("wcc.csv"), shell=True)
    subprocess.call("rm -f %s"%("wcc_prior_kvar.dat"), shell=True)
    # populate the result file with heading
    reslt_file = open("wcc.csv", "w")
    heading = f'#k values are fractional coordinates in direction of the reciprocal lattice vector G[{kevoldir}]\n'
    reslt_file.write(heading)
    heading = f'#WCC are evaluated on a closed Wilson loop in direction of the reciprocal lattice vector G[{kwlsndir}]\n'
    reslt_file.write(heading)
    heading = '#k'
    for i in range(bands[1]-bands[0]+1):
        heading += f',WCC {i+1}' # create ,wcc 1, wcc 2, ...
    heading += '\n' # new line
    reslt_file.write(heading)
    reslt_file.close()
    # MAIN LOOP
    klistsize = (nkwlsn,3) # klist array dimension
    Data = [] # to store Berry phase on each loop
    ikevol = -1 # init. counter
    for kevoli in np.linspace(start=kevol[0], stop=kevol[1], num=nkevol):
        ikevol += 1
        print(f'kevoli = {kevoli:.3f} ({ikevol+1} of {nkevol})')
        klist = np.zeros(klistsize)
        ikwlsn = -1 # init. counter
        for kwlsni in np.linspace(start=0, stop=1-1/nkwlsn, num=nkwlsn):
            ikwlsn += 1
            # k points [kfix, kevol, kwlsn] set in proper columns
            klist[ikwlsn,kfixdir-1] = kfix
            klist[ikwlsn,kevoldir-1] = kevoli
            klist[ikwlsn,kwlsndir-1] = kwlsni
        #print(klist)
        klist = klist * mult
        klist = np.c_[klist, mult*np.ones(nkwlsn), 1.00*np.ones(nkwlsn)]
        klist = np.int_(klist)
        # save case.klist file
        os.chdir(WorkingDir)
        np.savetxt(KlistFileName, klist, fmt="          %10i%10i%10i%10i%5.1f", 
                delimiter='', footer='END', comments='')
        # run BerryPI
        proc = subprocess.Popen("python $WIENROOT/SRC_BerryPI/BerryPI/berrypi -so %s %s -b %i %i %s -w %i"\
                %(spoption, orboption, bands[0], bands[1], poption, kwlsndir), shell=True, \
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()
        (stdout, stderr) = proc.communicate()
        if proc.returncode != 0:
            print(stdout.decode()) # need decode to deal with b'...' string
            print(stderr.decode())
            msg = "Error while executing BerryPI, exiting"
            raise RuntimeError(msg)
        else:
            if (ikevol == 0): # print BerryPI stdout once
                print(stdout.decode())
                print('Future BerryPI output will be supressed')

            print("success")

        # append iteration results to a global result file
        proc = subprocess.Popen("cat %s | sed 's/^/%f,/' >> %s"\
                %("wcc_i.csv", kevoli, "wcc.csv"), shell=True, stdout=subprocess.PIPE, \
                stderr=subprocess.PIPE)
        proc.wait()
        (stdout, stderr) = proc.communicate()
        if proc.returncode != 0:
            print(stderr.decode()) # need decode to deal with b'...' string
            msg = "Error while executing concatenate and sed command, exiting"
            raise RuntimeError(msg)
        # get output Berry phase for each Wilson loop
        berrypiOutFileName = str("%s.outputberry" %(str(WorkingDir.split('/')[-1])))
        with open(berrypiOutFileName, 'r') as read_file:
            for line in read_file:
                if "Berry phase sum (rad) =" in line:
                    #return line
                    content = line
                    break

        temp1 = float(content.split()[-1])
        temp2 = temp1 % (2 * np.pi)  # 2 pi wraping  
        temp = np.array([kevoli, temp1, temp2])
        Data.append(temp)
    # END MAIN LOOP

    Data = np.array(Data)
    phases = Data[:,2]
    phases = np.unwrap(phases)
    Data[:,2] = phases
    print(f'Total Berry phase on each Wilson loop for bands {bands[0]}-{bands[1]}:')
    print('-'*54)
    print(' i           k            Phase wrap.    Phase unwrap.')
    print('                            (rad)           (rad)')
    print('-'*54)
    rows, columns = Data.shape
    leni = len(str(rows)) # dind number of characters
    ki = [0, 0, 0]
    for i in range(rows):
        ki[kfixdir-1] = f'{kfix:.3f}'
        ki[kevoldir-1] = f'{Data[i,0]:.3f}'
        ki[kwlsndir-1] = '***'
        kitext = f'[{ki[0]}, {ki[1]}, {ki[2]}]'
        warn = ''
        if (i > 0) and (abs(Data[i,2]-Data[i-1,2]) > np.pi/4):
            warn = '  WARNING: cannot obtain smooth phase evolution'
        print(f'{i+1:{leni}d}  {kitext}     {Data[i,1]:.3f}        {Data[i,2]:8.3f}{warn}')
    print('-'*54)
    print('Here "***" refer to the direction of the Wilson loop.')

    subprocess.call("rm -f %s"%("wcc_i.csv"), shell=True) # clean temp file
    epilog() # print concluding remarks
