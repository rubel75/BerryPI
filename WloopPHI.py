#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 11:13:26 2019

@author: enigma
"""

import subprocess
import os
import sys
#import FileFormat, ReadInput


def FileFormatMessage():
    print ("Error: Use proper formated file")
    print ("""Example for file format:
/home/enigma/WIEN2k/case                              # Path of your WIEN2k working directory.
51                                                    # Wilson loop Z-minimum and Z-maximum value.     
1:84                                                  # Number of division in Z direction for wilson loop.  
&WloopCoordinate                                      # Wilson loop start (it is case sensitive)
0.4565 0.2000 0.5000 ; -0.4565 0.2000 0.5000          # Starting point 1 ; End point 1
0.4565 0.3000 0.5000 ; -0.4565 0.3000 0.5000          # Starting point 2 ; End point 2          
0.4565 0.2500 1.0000 ; -0.4565 0.2500 1.0000          # Starting point 3 ; End point 3
END                                                   # End of file (It is case sensitive)""")
    sys.exit()
    

def ReadInputValues(content, WloopFileName):
    try:
        WorkingDir = str(content[0][:-1])
        KlistFileName = str("%s.klist" %(WorkingDir.split('/')[-1]))
        n = int(content[1].split()[0])
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
                
    StartBand = int(content[2].split(":")[0])
    EndBand = int(content[2].split(":")[1])
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



try:
    import numpy as np
    print ("[OK] Numpy found")
except ImportError as error:
    print (error.__class__.__name__+": "+error.message)
    sys.exit()

args = sys.argv
#print (args)
#print(len(args))
if len(args) > 4 or len(args) == 1:
    print ("Please use valid command line options!")
    print ("Usage: python WloopPHI.py Wloop.in -s -o")
    print ("Input file name (Wlooop.in) is mandatory and [-s] & [-o] options are optionals.")
    sys.exit()

options = ""
for i in range(2,len(args)):
    options += args[i] + " "
    
options = options[:-1]
#print (options)
#print (len(options))

if len(options) == 5:
    if (options.find('s') != -1 and options.find('o') != -1): 
        print ("Optios are OK!")
    else:
        print ("Please use valid command line options!")
        print ("Usage: python WloopPHI.py Wloop.in -s -o")
        print ("Input file name (Wlooop.in) is mandatory and [-s] & [-o] options are optionals.")
        sys.exit()
#print (len(options))
#sys.exit()

WloopFileName = str(args[1])
#WloopFileName = str("Wloop.in")    
f = open(WloopFileName, 'r')
content = f.readlines()
f.close()

if ("END" in content[-1]):
    #content = content[:-3]
    print ("Success")
    WorkingDir, KlistFileName, n, multiplier, S_Band, E_Band, K_Start, K_End = ReadInputValues(
            content, WloopFileName)
else:
    FileFormatMessage()
    
if not os.path.exists(WorkingDir):
    print ("Error: Working directory does not exist.")
    print ("Please check your working directory and try again. Good Bye :)")
    sys.exit()
    
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
    print ("Wilson Loop ---------------------  %i" %(i+1))
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
    subprocess.call("python $WIENROOT/SRC_BerryPI/BerryPI/berrypi -j -w -b %i:%i %s > Berrypi.out"%(S_Band, E_Band, options), shell=True)
    with open("Berrypi.out", 'r') as read_file:
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

######################### Unwrap ###########################################

BP = Data[:, 2]
BP_out = np.unwrap(BP, discont=3.141592653589793, axis=-1)

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
    print ("Output figure ""BW_PiWrapped.png"" has generated.")

    fig, ax = plt.subplots(figsize=(6,6), dpi=300)
    ax.plot(Data[:, 0], Data[:, 3], 'bo')
    ax.set(xlabel = 'Loop in %s direction' %direction, ylabel = 'Berry Phase (1/2pi)', title = 'Berry Phase Vs Wilson loop')
    fig.savefig("BW_PhaseChange.png")
    print ("Output figure ""BW_PhaseChange.png"" has generated")
    print ("Good Bye!!! :)")
except ImportError as error:
    print (error.__class__.__name__+": "+error.message)
    print ("You can plot your figure yourself by using ""PHI.dat"" file.")
    print ("Good bye!!! :)")
    sys.exit()
