#!/usr/bin/env python
import numpy as np
import numpy as np
import os, os.path
import subprocess
import time
import matplotlib #Graphs
import matplotlib.pyplot as plt
np.set_printoptions(threshold=np.inf)
start = time.time()

print("Running Chern.PY welcome!")

#Later to be input
i_band = 1
s_band = 143
n = 14 #Discretization of brillouin zone
plane_dir = 'z' #Plane perpendicular to which axis
plane_value = 0.0 #Value of the constant plane

#From dir
WorkingDir = os.getcwd() #Obtain the working directory
print ("Working directory = %s" %(WorkingDir)) 
case = str(WorkingDir.split('/')[-1]) #Obtains the case
multiplier = 100000000 #Multiplier later used for the formating of klist

#Defining the meshgrid to perform the calculation
nx , ny = (n,n)
kx = np.linspace(-0.5, 0.5, nx)
ky = np.linspace(-0.5, 0.5, ny)
kxv , kyv = np.meshgrid(kx , ky, indexing = 'ij')

#Function for getting the loop points
full = [] 
#List with the coordinates, A list with lists, each one is for a value of kx, inside there are lists of tuples with kx constant and ky changing
for k in range(0,n):
    coordinate = np.c_[kxv[k],-kyv[k]]
    coordinate_list = coordinate.tolist()
    full.append(coordinate_list)
#print(full)

berry_phases = [] #List of lists of berryphases per row
#chern_numbers = [] ##List of lists of Chern numbers per row
count = 0
#Iterating over very vertex
for x in full[0:n-1]: #Iterates over the kx value lists
    col_phase = [] #Phases in column
    #col_chern = [] 
    for y in x: #Iterates over the kx,ky tuple in each kx list
        if x.index(y) + 1 < n: #Not taking into account edge
            #print(full.index(x))
            #print(x.index(y))
            #print(full[full.index(x)][x.index(y)])
            #print('---')
            dn = full[full.index(x)][x.index(y)+1]
            dg = full[full.index(x)+1][x.index(y)+1]
            rt = full[full.index(x)+1][x.index(y)]
            sm = full[full.index(x)][x.index(y)]

            #Transform from 2D to 3D
            if plane_dir == 'z':
                dn = [ dn[0], dn[1], plane_value]
                dg = [ dg[0], dg[1], plane_value]
                rt = [ rt[0], rt[1], plane_value]
                sm = [ sm[0], sm[1], plane_value]
            elif plane_dir == 'x':
                dn = [ plane_value , dn[0], dn[1]]
                dg = [ plane_value , dg[0], dg[1]]
                rt = [ plane_value , rt[0], rt[1]]
                sm = [ plane_value , sm[0], sm[1]]
            elif plane_dir == 'y':
                dn = [ dn[0],plane_value , dn[1]]
                dg = [ dg[0],plane_value , dg[1]]
                rt = [ rt[0],plane_value , rt[1]]
                sm = [ sm[0],plane_value , sm[1]]
            #print(dn,dg,rt,sm)
            loop = [sm,dn,dg,rt]
            #print(loop)
            loop = np.array(loop)
            #print(loop)
            size = np.size(loop, 0)
            loop = loop*multiplier
            loop = np.c_[loop, multiplier*np.ones(size), 2.00*np.ones(size)]
            loop = np.int_(loop)
            filename = str("%s.klist"%case)
            np.savetxt(filename, loop, fmt="          %10i%10i%10i%10i%5.1f", 
                   delimiter='', footer='END', comments='')
            
            run_berrypi = subprocess.run(["python $WIENROOT/SRC_BerryPI/BerryPI/berrypi -so -w -p -sp -b %i %i"%(i_band, s_band)],shell=True) 
            
            berrypiOutFileName = str("%s.outputberry" %(str(WorkingDir.split('/')[-1]))) #Reads output.berry
            with open(berrypiOutFileName, 'r') as read_file:  #Searches for line with berry phase
                for line in read_file:
                    if "Berry phase sum (rad) =" in line:
                        content = line
            temp = float(content.split()[-1]) #Phase value
            temp1 = ((temp + np.pi) % (2 * np.pi) - np.pi) #2pi wrapping
            #chern = temp1 / 2*np.pi #Chern number
            col_phase.append(temp1)
            #col_chern.append(chern)
    berry_phases.append(col_phase) #Appends the list for each row to the total one
    #chern_numbers.append(col_chern)        



berry_phases_array = np.array(berry_phases)
#chern_numbers_array = np.array(chern_numbers)

def totalsum(array):
    summed_row = np.array([])
    for r in array:
        row_sum = np.sum(r)
        np.append(summed_row,row_sum)
    return np.sum(summed_row) 





all_phases = [] #List of wrapped 2pi phases in zigzag
for i in berry_phases:
    if berry_phases.index(i) % 2 == 0:
        all_phases.extend(i)
    else:
        rever_list = list(reversed(i))
        all_phases.extend(rever_list)
all_phases_array = np.array(all_phases)
#print(all_phases)



phases_horizontal = [] #List of lists by rows
for L in range(0,len(berry_phases)):
    ph_hori = []
    for cx in berry_phases:
        for cy in cx:
            if cx.index(cy) == L:
                ph_hori.append(cy)
    phases_horizontal.append(ph_hori)
#print(phases_horizontal)



all_phasesh = [] #List of wrapped 2pi phases in zigzag horizontally
for l in phases_horizontal:
    if phases_horizontal.index(l) % 2 == 0:
        all_phasesh.extend(l)
    else:
        rever_listh = list(reversed(l))
        all_phasesh.extend(rever_listh)
all_phasesh_array = np.array(all_phasesh)
#print(all_phasesh)




def Unwrap(Data):
    BP = Data
    BP_out = np.unwrap(BP, discont=float(1*np.pi), axis=-1)
    #print(BP_out)
    diff = 0
    Check_Diff = False
    for i in BP_out:
        diff = i-diff
        if (diff > np.divide(np.pi, 2)):
            Check_Diff = True
        diff = i       
    CHERN_out = np.divide(BP_out, np.multiply(2, np.pi))
    result = [BP_out,CHERN_out]
    #print(Data)
    return (Check_Diff, result)



#Results Unwrap Vertically
Check_diff,results = Unwrap(all_phases_array)
BPFinal = results[0]
SUMBPF = np.sum(results[0])
CHERNNUMBER = np.sum(results[1])

#Unwrap Horizontally
Check_diffh,resultsh = Unwrap(all_phasesh_array)
BPFinalh = resultsh[0]
SUMBPFh = np.sum(resultsh[0])
CHERNNUMBERh = np.sum(resultsh[1])


print("---------------------------------------")
print("The total Chern number is: ",CHERNNUMBER)
print("Phases:",BPFinal.tolist())
print("Chern numbers:",results[1].tolist())
if Check_diff == True:
    print('No smooth !!!!!!!!!!!!!!!!!!!!!!!!!')

print("---------------------------------------")
print("The total Chern number HORIZONTAL is: ",CHERNNUMBERh)
print("Phases:",BPFinalh.tolist())
print("Chern numbers:",resultsh[1].tolist())
if Check_diffh == True:
    print('No smooth horizontally !!!!!!!!!!!!!!!!!!!!!!!!!')

#PLOTS PHASE
plt.rcParams.update({'font.size': 20, 'font.family': 'serif'})
plt.figure(1, figsize=(15, 15))
plt.subplot(211)
plt.plot(range(0,len(BPFinal)), BPFinal ,label=('Chern number:%f Plane %s : %f bands:%i-%i grid:%iX%i'%(CHERNNUMBER,plane_dir,plane_value,i_band,s_band,n-1,n-1)),color='navy',linewidth=1.5 )
plt.ylabel(r'$\gamma_{Berry}$')
plt.title('Vertical unwrapping of the Berry Phase of %s'%case)
plt.legend()

plt.subplot(212)
plt.plot(range(0,len(BPFinalh)), BPFinalh ,label=('Chern number:%f Plane %s : %f bands:%i-%i grid:%iX%i'%(CHERNNUMBERh,plane_dir,plane_value,i_band,s_band,n-1,n-1)), color='crimson',linewidth=1.5 ) 
plt.ylabel(r'$\gamma_{Berry}$')
plt.title('Horizontal unwrapping of the Berry Phase of %s'%case)
plt.legend()
plt.savefig("unwrapping%i.png"%n,dpi=500)
#PLOT OF BERRY CURVATURE FLUX
phases_flux = BPFinal.tolist()
twoDmatrix = []
d = 0
for i in range(0,len(phases_flux)+1, n-1):
    if i > 0:      
        flag = 0
        if flag % 2 == 0:
            list_temp = phases_flux[d:i]
            twoDmatrix.append(list_temp)
        else:
            list_temp = list(reversed(phases_flux[d:i]))
            twoDmatrix.append(list_temp)
        flag += 1
        d = i
twoDmatrix = np.array(twoDmatrix).T

plt.figure(2, figsize=(15, 15))
plt.imshow(twoDmatrix,cmap='viridis',extent=(-0.5,0.5,-0.5,0.5),interpolation='spline36')
plt.xlim(-0.5,0.5)
plt.ylim(-0.5,0.5)
plt.colorbar()
plt.ylabel(r'$k_{y}$')
plt.xlabel(r'$k_{x}$')
#plt.rcParams["figure.figsize"] = (20,20)
plt.title(r'Flux of Berry Curvature: FeBr3')
plt.savefig("berryflux%i.png"%n,dpi=500)



print("ChernPy is done!!!")
end = time.time()
total_time = end - start
print("\n"+ str(total_time)," Seconds")
print(str(total_time/60)," Minutes")
