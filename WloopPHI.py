#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 11:13:26 2019

@author: enigma
"""

import subprocess
import os
import sys
import FileFormat, ReadInput

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
    WorkingDir, KlistFileName, n, multiplier, S_Band, E_Band, K_Start, K_End = ReadInput.Values(
            content, WloopFileName)
else:
    FileFormat.Message()
    
if not os.path.exists(WorkingDir):
    print ("Error: Working directory does not exist.")
    print ("Please check your working directory and try again. Good Bye :)")
    sys.exit()
    
#print (len(K_Start))
#print (len(K_End))
#print (np.linalg.norm(K_Start[0] - K_End[0]))
#print (np.linalg.norm(K_Start[1] - K_End[1]))
#print (np.linalg.norm(K_Start[2] - K_End[2]))
#sys.exit()
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
    
    pwd = os.getcwd()
    os.chdir(WorkingDir)
    subprocess.call("mv %s/%s %s/%s" %(pwd, filename, WorkingDir, KlistFileName), shell = True)
    #print ("python $WIENROOT/SRC_BerryPI/BerryPI/berrypi -j -w -b %i:%i %s >> Berrypi.out"%(S_Band, E_Band, options))
    #sys.exit()
    subprocess.call("python $WIENROOT/SRC_BerryPI/BerryPI/berrypi -j -w -b %i:%i %s >> Berrypi.out"%(S_Band, E_Band, options), shell=True)
    f = open("Berrypi.out", "r")
    content = f.readlines()
    f.close()
    os.chdir(pwd)
    
    temp = float(content[-1].split()[-1][1:-2])
    temp1 = ((temp + np.pi) % (2 * np.pi) - np.pi)  # 2 pi wraping
    #temp = np.array([i, temp])    
    temp = np.array([x_axis[loop], temp, temp1])
    loop += 1
    
    Data.append(temp)
    
Data = np.array(Data)

#outfile = str("Data.dat")
#np.savetxt(outfile, Data, fmt='%5.5f', delimiter='          ', 
#           header='Loop (%s)      BerryPhase(BP)       BP(pi wrap)' %direction)

############################################################################
######################### Unwrap ###########################################
############################################################################

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

"""
k = 0
i = 1
#print (np.size(u))
temp = []
threshold = np.pi/2
#threshold = 0.1
#BP_out = np.zeros((np.size(u), np.size(u)))
BP_out = np.zeros(np.size(BP))
for i in range(1, np.size(BP) - 1):
    BP_out[i] = BP[i] + (2*np.pi*k)
    if (np.abs(BP[i+1]-BP[i]) > np.abs(threshold)):
        if (np.abs(BP_out[i] - BP_out[i-1]) < np.abs(threshold)):
            if BP[i+1] < BP[i]:
                k = k+1
            else:
                k = k-1
    temp.append(k)
            
BP_out[(i+1)] = BP[i+1] + (2*np.pi*k)
    
BP_out[0] = BP[0] 
BP_out.shape = BP_out.size,1
"""
Data = np.append(Data, BP_out, axis=1)

"""
#################### Chern Number ##########################################

ChernNumber  = ((BP_out[BP_out.size-1] - BP_out[(BP_out.size-1)/2]) / 
                (2*np.pi) + (BP_out[(BP_out.size-1)/2] - BP_out[0]) / (2*np.pi))

if (ChernNumber != -1.0 and ChernNumber != 1.0):
    print ("Wilson loop found two weyl points.")
    ChernNumber_1 = (BP_out[(BP_out.size-1)/2] - BP_out[0]) / (2*np.pi)
    ChernNumber_2 = (BP_out[BP_out.size-1] - BP_out[(BP_out.size-1)/2]) / (2*np.pi)
    print ("Chern Number for first weyl point = %2.1f" %ChernNumber_1)
    print ("Chern Number for second weyl point = %2.1f" %ChernNumber_2)
    
else:
    print ("Wilson loop found one weyl points.")
    print ("Chern Number = %2.1f" %ChernNumber)
"""

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
    print ("Do not WORRY!!! You can plot your figure yourself by using ""PHI.dat"" file.")
    print ("Good bye!!! :)")
    sys.exit()
