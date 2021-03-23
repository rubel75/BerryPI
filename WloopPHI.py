#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 11:13:26 2019

@author: enigma
"""

import subprocess
import os
import sys
import argparse # parse line arguments

def printEpilog():
    print('''
Suggested references:
[1] H. Saini, M. Laurien, P. Blaha, and O. Rubel
    “WloopPHI: A tool for ab initio characterization of Weyl semimetals”,
    arXiv:2008.08124 [cond-mat.mtrl-sci] (2020)
    https://arxiv.org/abs/2008.08124
[2] S.J. Ahmed, J. Kivinen, B. Zaporzan, L. Curiel, S. Pichardo and O. Rubel
    "BerryPI: A software for studying polarization of crystalline solids with 
    WIEN2k density functional all-electron package"
    Comp. Phys. Commun. 184, 647 (2013)
    https://doi.org/10.1016/j.cpc.2012.10.028

Questions and comments are to be communicated via the WIEN2k mailing list
(see http://susi.theochem.tuwien.ac.at/reg_user/mailing_list)''')

def FileFormatMessage():
    print ("Error: Use proper formated file")
    print ("""Example for file format:
51                                                    # Number of Wilson loops along the trajectory
1:84                                                  # Band range  
&WloopCoordinate                                      # Wilson loop start (it is case sensitive)
0.4565 0.2000 0.5000 ; -0.4565 0.2000 0.5000          # Starting point 1 ; End point 1
0.4565 0.3000 0.5000 ; -0.4565 0.3000 0.5000          # Starting point 2 ; End point 2          
0.4565 0.2500 1.0000 ; -0.4565 0.2500 1.0000          # Starting point 3 ; End point 3
END                                                   # End of file (It is case sensitive)""")
    sys.exit()
    

def ReadInputValues(content, WloopFileName):
    try:
        WorkingDir = os.getcwd()
        print ("Working directory = %s" %(WorkingDir))
        KlistFileName = str("%s.klist" %(WorkingDir.split('/')[-1]))
        n = int(content[0].split()[0])
        #multiplier = int(content[2].split()[0]) # User dependent (make sure use proper array indexing)
        multiplier = 1000 # User independent
    except ValueError:
        print ("Error: Value Error")
        FileFormatMessage()
        
    K_Points = []
    wlcoordinate = 0
    with open(WloopFileName) as infile:
        copy = False
        for line in infile:
            if line.strip() == "&WloopCoordinate":
                wlcoordinate = "&WloopCoordinate"
                copy = True
                continue
            elif line.strip() == "END":
                copy = False
                continue
            elif copy:
                K_Points.append(line)
                
    StartBand = int(content[1].split(":")[0])
    EndBand = int(content[1].split(":")[1])
    S = [] # Staring Point
    E = [] # End Point
    for i in K_Points:
        temp = i.split(";")
        S.append(np.array(temp[0].split(), dtype="float"))
        E.append(np.array(temp[1].split(), dtype="float"))
        
    S = np.array(S)
    E = np.array(E)
    
        
    if(wlcoordinate == 0):
        print ("Error: ""&WloopCoordinate"" is not properly formatted. Notice it is case sensitive")
        FileFormatMessage()
        
    if (S.size == 0):
        print ("Error: Wilson loop points")
        FileFormatMessage()
        
    if (E.size == 0):
        print ("Error: Wilson loop points")
        FileFormatMessage()
        
    return (WorkingDir, KlistFileName, n, multiplier, StartBand, EndBand, S, E)

def Solve (*args):
    K_Points = []
    for i,j in zip(K_Start, K_End):
        xmin = i[0]
        xmax = j[0]
        ymin = i[1]
        ymax = j[1]
        zmin = i[2]
        zmax = j[2]
        
        var_x = np.linspace(xmin, xmax, num=n)
        var_y = np.linspace(ymin, ymax, num=n)
        var_z = np.linspace(zmin, zmax, num=n)
        
        for x, y, z in zip(var_x, var_y, var_z):
            Klist = np.array([[x, y, z]])
            #print (Klist)
            K_Points.append(Klist)
            
        #break
    K_Points = np.concatenate(K_Points, axis=0)
    
    if ((var_x[1] - var_x[0]) == 0 and (var_y[1] - var_y[0]) == 0):
        x_axis = var_z
        direction = 'z'
    elif ((var_y[1] - var_y[0]) == 0 and (var_z[1] - var_z[0]) == 0):
        x_axis = var_x
        direction = 'x'
    else:
        x_axis = var_y
        direction = 'y'
    
    Data = []
    loop = 0
    
    for i in range(0, n):
        print ("Wilson Loop ---------------------  %i of %i" %(i+1, n))
        temp = i
        Klist = []
        for k in range(0, len(K_Start)):
            #print (temp)
            Klist.append(K_Points[temp])
            temp = temp + n    
        #temp = np.concatenate(Klist, axis=0)
        #break
        Klist = np.array(Klist)
        size = np.size(Klist, 0)
        #break
        Klist = Klist * multiplier
        Klist = np.c_[Klist, multiplier*np.ones(size), 2.00*np.ones(size)]
        Klist = np.int_(Klist)
        #break
        filename = str("Wilson.klist")
        np.savetxt(filename, Klist, fmt="          %5i%5i%5i%5i%5.1f", delimiter='', footer='END', comments='')
        #print(Klist)
        pwd = os.getcwd()
        os.chdir(WorkingDir)
        subprocess.call("mv %s/%s %s/%s" %(pwd, filename, WorkingDir, KlistFileName), shell = True)
        subprocess.call("python $WIENROOT/SRC_BerryPI/BerryPI/berrypi -so -w -b %i %i %s"%(S_Band, E_Band, options), shell=True)
        berrypiOutFileName = str("%s.outputberry" %(str(WorkingDir.split('/')[-1])))
        with open(berrypiOutFileName, 'r') as read_file:
            for line in read_file:
                if "Berry phase sum (rad) =" in line:
                    #return line
                    content = line
                    #print (content)
    
        os.chdir(pwd)
        #sys.exit()
        
        temp = float(content.split()[-1])
        #print (temp)
        #sys.exit()
    
        temp1 = ((temp + np.pi) % (2 * np.pi) - np.pi)  # 2 pi wraping
        #temp = np.array([i, temp])    
        temp = np.array([x_axis[loop], temp, temp1])
        loop += 1
        
        Data.append(temp)
        
    Data = np.array(Data)
    
    return (direction, Data)

def Unwrap(Data):
    BP = Data[:, 2]
    BP_out = np.unwrap(BP, discont=float(1*np.pi), axis=-1)
    diff = 0
    Check_Diff = False
    for i in BP_out:
        diff = i-diff
        if (diff > np.divide(np.pi, 2)):
            Check_Diff = True
        diff = i
    
    BP_out = np.divide(BP_out, np.multiply(2, np.pi))
    shape = BP_out.shape
    BP_out.shape = (shape[0], 1)
    
    Data = np.append(Data, BP_out, axis=1)
    
    return (Check_Diff, Data)
    
    
if __name__=="__main__":
    import time
    StartTime = time.time() # Calculation start time.
    try:
        import numpy as np
        print ("[OK] Numpy found")
    except ImportError as error:
        print ("It seems that numpy is not installed. Exiting")
        sys.exit(1)
    
    # Set up parser for line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("infile",\
            help="input file name",\
            type=str)
    parser.add_argument("-sp",\
            help="spin polarized calculation",\
            action="store_true")
    parser.add_argument("-orb",\
            help="calculation with an additional orbit potential (e.g., LSDA+U)",\
            action="store_true")
    args = parser.parse_args()
    
    # Assign line arguments parsed by "argparse"
    WloopFileName = args.infile # input file name
    print("Input file name: %s" %WloopFileName)
    options = "" # start with empty options and fill it up
    if args.sp: # enable spin polarization
        options = options + '-sp'
    if args.orb: # enable orbital potential
        options = options + '-orb'
    print("Additional options: %s" %options)
    
    # Read input file
    print("Checking existance of %s" %WloopFileName)
    if not(os.path.isfile(WloopFileName)):
        print("{} does not exist, cannot finish calculation.".format(WloopFileName))
        exit(2)
    else:
        print('-- OK')
    f = open(WloopFileName, 'r')
    content = f.readlines()
    f.close()
    
    if ("END" in content[-1]):
        #content = content[:-3]
        print ("Success")
        WorkingDir, KlistFileName, n, multiplier, \
            S_Band, E_Band, K_Start, K_End = \
                ReadInputValues(content, WloopFileName)
    else:
        FileFormatMessage()
        
    if not os.path.exists(WorkingDir):
        print ("Error: Working directory does not exist.")
        print ("Please check your working directory and try again. Thank you!")
        sys.exit()
        
    ######################## Solver ############################################
    direction, Data = Solve(WorkingDir, KlistFileName, n, multiplier, S_Band, E_Band, K_Start, K_End)

    ######################### Unwrap ###########################################
    Check_Diff, Data = Unwrap(Data) 

    #################### Save data to file #####################################
    outfile = str("PHI.dat")
    np.savetxt(outfile, Data, fmt='%5.5f', delimiter='          ', 
               header='Loop (%s)       BerryPhase(BP)   BP(-/+pi wrap)   BP(unwrap)' %direction)
    print ("Calculation done!!!")
    if (Check_Diff == True):
        print("WARNING -----> Phase Difference: The jump in phase difference is greter than pi/2 which is not good.")
        print("To avoid this warning please increase the number of Wilson loops.")
    print ("Output data file ""PHI.dat"" has generated.")
    
    #################### PLOT ##################################################
    try:
        import matplotlib
    except ImportError as error: # matplotlib is not installed
        print ("It seems that matplotlib is not installed, but it is not essential.")
        print ("You can plot the figure yourself by using ""PHI.dat"" file.")
        EndTime = time.time() # Calculation end time.
        print ("Total time = %s" %time.strftime('%H:%M:%S', time.gmtime(float(EndTime - StartTime))))
        printEpilog()
        sys.exit(0)
    
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    print ("[OK] Matplotlib found")
    fig, ax = plt.subplots(figsize=(6,6), dpi=300)
    ax.plot(Data[:, 0], Data[:, 1], 'bo')
    ax.set(xlabel = 'Loop in %s direction' %direction, ylabel = 'Berry Phase (radians)', title = 'Berry Phase Vs Wilson loop')
    #ax.grid()
    fig.savefig("BW_RawData.png")
    #plt.show()
    print ("Output figure ""BW_RawData.png"" has generated.")
    
    fig, ax = plt.subplots(figsize=(6,6), dpi=300)    
    ax.plot(Data[:, 0], Data[:, 2], 'bo')
    ax.set(xlabel = 'Loop in %s direction' %direction, ylabel = 'Berry Phase (radians)', title = 'Berry Phase Vs Wilson loop')
    fig.savefig("BW_PiWrapped.png")
    print ("Output figure ""BW_PiWrapped.png"" has been generated.")
    
    fig, ax = plt.subplots(figsize=(6,6), dpi=300)
    ax.plot(Data[:, 0], Data[:, 3], 'bo')
    ax.set(xlabel = 'Loop in %s direction' %direction, ylabel = 'Berry Phase (1/2pi)', title = 'Berry Phase Vs Wilson loop')
    fig.savefig("BW_PhaseChange.png")
    print ("Output figure ""BW_PhaseChange.png"" has been generated")
    EndTime = time.time() # Calculation end time.
    print ("Total time = %s" %time.strftime('%H:%M:%S', time.gmtime(float(EndTime - StartTime))))
    printEpilog()
