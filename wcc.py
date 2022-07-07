#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Calculation of Wannier charge centers evolution in a plane.
The plane and WCC direction are defined in the user_input() section below.
See prolog() for more details about the calculation setup.
Results are tabulated in the 'wcc.csv' file.

@author: Oleg Rubel
"""

import subprocess
import os
import numpy as np

def user_input():
    """Editable section where users define their input"""
    kscandir = 2 # Y
    kscan = [0, 0.5] # start and end in fraction of the correcponging reciprocal lattice vector G[kscandir]
    nkscan = 20 # descretization intervals
    kwlsndir = 3 # Z, different from kscandir
    nkwlsn = 10 # descretization intervals
    kfix = 0.0 # in fraction of reciprocal lattice vectors G[kfixdir]
    bands = [61, 78]
    parallel = True # parallel option [-p] in BerryPI (needs a proper .machines file)
    spinpolar = False # [-sp] in BerryPI

    return kscandir, kscan, nkscan, kwlsndir, nkwlsn, kfix, bands, parallel, spinpolar

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
(kfix, kscan=var, kwcc=var)

kwlsn:
    This is a direction in k space along which we construct a closed Wilson loop
    and later evaluate WCCs on that loop. It can be 1 for X, 2 for Y, or 3 for Z.
kscan:
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

Next, we advance the Wislon loop in the kscan direction and WCCs again.
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

kscan dir. ->
(kfix is perpendicular to the screen)

After each step along kscan, data from wcc_i.csv are accumulated in the wcc.csv 
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
    (this paper first introduced WCCs)
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
    kscandir, kscan, nkscan, kwlsndir, nkwlsn, kfix,\
            bands, parallel, spinpolar = user_input()
    # Check input
    if not(kscandir in [1, 2, 3]):
        raise ValueError(f'kscandir={kscandir}, while expected one of [1,2,3]')
    elif not(kwlsndir in [1, 2, 3]):
        raise ValueError(f'kwlsndir={kwlsndir}, while expected one of [1,2,3]')
    elif kscandir == kwlsndir:
        raise ValueError(f'kwlsndir={kwlsndir} is the same as kwlsndir={kwlsndir}, while expected to be different')
    if not(type(kscan) == list):
        raise ValueError(f'kscan should be type list, while you have {type(kscan)}')
    elif not(len(kscan) == 2):
        raise ValueError(f'kscan list should have length = 2, while you have {len(kscan)}')
    if not(type(nkscan) == int):
        raise ValueError(f'nkscan should be type int, while you have {type(nkscan)}')
    elif not(nkscan >= 1):
        raise ValueError(f'nkscan should be at lest 1, while you have {nkscan}')
    if not(type(nkwlsn) == int):
        raise ValueError(f'nkwlsn should be type int, while you have {type(nkwlsn)}')
    elif not(nkwlsn >= 1):
        raise ValueError(f'nkwlsn should be at lest 1, while you have {nkwlsn}')
    # Evaluate missing inport
    kfixdir = set([1,2,3])-set([kscandir,kwlsndir])
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
    # Print input
    prolog() # print some info for the user
    print("User input:")
    print(f'kscandir={kscandir}, kwlsndir={kwlsndir}, kfixdir={kfixdir}')
    print(f'kscan range={kscan} with {nkscan} intervals')
    print(f'Wilson loop will use {nkwlsn} intervals')
    print(f'Band range from {bands[0]} to {bands[1]}')
    if parallel:
        print('Parallel option [-p] will be used in BerryPI call')
    else:
        print('Parallel option [-p] will not be used in BerryPI call')
    k = [0,0,0] # init k plane list
    k[kfixdir-1] = kfix
    k[kscandir-1] = 'var scan'
    k[kwlsndir-1] = 'var Wloop'
    print(f'Plane is fixed at k={k}')
    WorkingDir, KlistFileName, mult = preliminary()
    # remove the result file to get a fresh start
    subprocess.call("rm -f %s"%("wcc.csv"), shell=True)
    # populate the result file with heading
    reslt_file = open("wcc.csv", "w")
    heading = f'#k values are fractional coordinates in direction of the reciprocal lattice vector G[{kscandir}]\n'
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
    ikscan = -1 # init. counter
    for kscani in np.linspace(start=kscan[0], stop=kscan[1], num=nkscan):
        ikscan += 1
        print(f'kscani = {kscani:.3f} ({ikscan+1} of {nkscan})')
        klist = np.zeros(klistsize)
        ikwlsn = -1 # init. counter
        for kwlsni in np.linspace(start=0, stop=1-1/nkwlsn, num=nkwlsn):
            ikwlsn += 1
            # k points [kfix, kscan, kwlsn] set in proper columns
            klist[ikwlsn,kfixdir-1] = kfix
            klist[ikwlsn,kscandir-1] = kscani
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
        proc = subprocess.Popen("python $WIENROOT/SRC_BerryPI/BerryPI/berrypi -so %s -b %i %i %s -w %i"\
                %(spoption, bands[0], bands[1], poption, kwlsndir), shell=True, stdout=subprocess.PIPE, \
                stderr=subprocess.PIPE)
        proc.wait()
        (stdout, stderr) = proc.communicate()
        if proc.returncode != 0:
            print(stdout.decode()) # need decode to deal with b'...' string
            print(stderr.decode())
            msg = "Error while executing BerryPI, exiting"
            raise RuntimeError(msg)
        else:
            if (ikscan == 0): # print BerryPI stdout once
                print(stdout.decode())
                print('Future BerryPI output will be supressed')
            print("success")
        # append iteration results to a global result file
        proc = subprocess.Popen("cat %s | sed 's/^/%f,/' >> %s"\
                %("wcc_i.csv", kscani, "wcc.csv"), shell=True, stdout=subprocess.PIPE, \
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
        temp = np.array([kscani, temp1, temp2])
        Data.append(temp)
    # END MAIN LOOP

    Data = np.array(Data)
    phases = Data[:,2]
    phases = np.unwrap(phases)
    Data[:,2] = phases
    print(f'Total Berry phase on each Wislon loop for bands {bands[0]}-{bands[1]}:')
    print('-'*54)
    print(' i           k            Phase wrap.    Phase unwrap.')
    print('                            (rad)           (rad)')
    print('-'*54)
    rows, columns = Data.shape
    leni = len(str(rows)) # dind number of characters
    ki = [0, 0, 0]
    for i in range(rows):
        ki[kfixdir-1] = f'{kfix:.3f}'
        ki[kscandir-1] = f'{Data[i,0]:.3f}'
        ki[kwlsndir-1] = '***'
        kitext = f'[{ki[0]}, {ki[1]}, {ki[2]}]'
        warn = ''
        if (i > 0) and (abs(Data[i,2]-Data[i-1,2]) > np.pi/4):
            warn = '  WARNING: cannot obtain smooth pase evolution'
        print(f'{i+1:{leni}d}  {kitext}     {Data[i,1]:.3f}        {Data[i,2]:8.3f}{warn}')
    print('-'*54)
    print('Here "***" refer to the direction of the Wilson loop.')

    subprocess.call("rm -f %s"%("wcc_i.csv"), shell=True) # clean temp file
    epilog() # print concluding remarks