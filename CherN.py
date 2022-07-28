#!/usr/bin/env python
import os, os.path
import subprocess
import sys


"""
Calculation of Chern topological invariant for a given material system. 
The inferior and top limit bands are defined in the user_input below.
See prolog() for more details about the calculation setup.
Results are stored in the 'berryflux.dat' file. 

@author: Andrés F Gómez B
"""


 
def user_input():
    """User input section"""
    i_band = 1    # Inferior band (starts from 1)
    s_band = 130   # Superior band (must be => to i_band)
    n = 15 # Discretization of brillouin zone by (n-1)x(n-1) loops. 
    plane_dir = 3   # Direction normal to the plane  (1 or 2 or 3)
    plane_value = 0.0 # Value of the constant plane 
    boundary = [-0.5,0.5,-0.5,0.5] #Boundary selection: ex if plane_dir = 3 -> [1min,1max,2min,2max]
    parallel = True  # parallel option [-p] in BerryPI (needs a proper .machines file)
    spinpolar = True # spin polarized [-sp] in BerryPI
    name = "" #Optional (if left as "" the name of the working directory by default)
    return i_band,s_band,n,plane_dir,plane_value,parallel,spinpolar,boundary,name


def preliminary():
    if os.environ.get('WIENROOT')==None:
        msg = "The environment variable WIENROOT is not set. "+\
                "It should be set and point to the WIEN2k installation "+\
                "directory for proper functioning of WIEN2k."
        raise RuntimeError(msg)
    try:
        WorkingDir = os.getcwd()
        print ("Working directory = %s" %(WorkingDir))
        case = str(WorkingDir.split('/')[-1]) #Obtains the case
        multiplier = 100000000 # Multiplier later used for the formating of klist (user independent)
    except ValueError:
        print ("Error: Value Error")
    return (WorkingDir, case, multiplier)

def prolog():
    txt="""
Calculate the Chern topological invariant (C) for a plane perpendicular to one of the axis in k space defined at a certain value 
(ex: plane_dir = '3', plane_value = 0.0)

plane_dir:
    This is a direction in k space for which a perpendicular plane is constructed and later discretized for the computing of C. 
plane_value:
    This is the value along 'plane_dir' in which the plane is selected.

The calculation is done by discretizing the selected portion of the BZ in(n-1)x(n-1) loops for which the Berry phase is calculated. 


"""
    print(txt)

def epilog():
    txt="""
Results (Chern number and Berryflux values) are stored in the 'berryflux.dat' file. Berry curvature flux is displayed in 
'berryflux.png' file. Please check headings for more explanation about the content.

Suggested references:
[1] S.J.Ahmed, J.Kivinen, B.Zaporzan, L.Curiel, S.Pichardo and O.Rubel
    "BerryPI: A software for studying polarization of crystalline solids with 
    WIEN2k density functional all-electron package"
    Comp. Phys. Commun. 184, 647 (2013)
    https://doi.org/10.1016/j.cpc.2012.10.028
    (our implementation for Berry phase calculation in WIEN2k)
[2] D. Gresch, G. Autès, O. V. Yazyev, M. Troyer, D. Vanderbilt, B. A. Bernevig, and A. A. Soluyanov
    "Z2Pack: Numerical implementation of hybrid Wannier centers for identifying topological materials"
    Phys. Rev. B 95, 075146 (2017)
    https://doi.org/10.1103/PhysRevB.95.075146

[3] QuanSheng Wu, ShengNan Zhang, Hai-Feng Song, Matthias Troyer,and Alexey A. Soluyanov. Wanniertools:
    An open-source software package for novel topological materials. Computer Physics Communications,
    224,2018. ISSN 0010-4655. doi: https://doi.org/10.1016/j.cpc.2017.09.033

Questions and comments are to be communicated via the WIEN2k mailing list
(see http://susi.theochem.tuwien.ac.at/reg_user/mailing_list)"""
    print(txt)

# MAIN
if __name__=="__main__":
    import time
    start = time.time()
    
    try:
        import numpy as np
        print ("Numpy found")
    except ImportError as error:
        print(error)
        print("Numpy not installed. Exiting")
        sys.exit(1)
    
    np.set_printoptions(threshold=np.inf)
    # Set user parameters
    i_band,s_band,n,plane_dir,plane_value,parallel,spinpolar,boundary,name = user_input()
    # Check input
    if type(i_band) != int:
        raise ValueError(f'i_band={i_band}, while expected an integer')
    elif type(s_band) != int:
        raise ValueError(f's_band={s_band}, while expected an integer')
    elif type(n) != int:
        raise ValueError(f's_band={n}, while expected an integer')
    elif type(plane_dir) != int:
        raise ValueError(f'plane_dir={plane_dir}, while expected an integer')    
    if i_band > s_band:
        raise ValueError(f'i_band={i_band} > s_band{s_band}')
    if i_band < 0 or s_band < 0 or n < 0:
        raise ValueError(f'The values for i_band, s_band and n should be positive.')
    if n < 1:
        raise ValueError(f'n={n}, while expected a value greater than 1')
    elif i_band == 0 or s_band == 0:
        raise ValueError(f'i_band and s_band must be different from zero')
    if not(plane_dir in [1 , 2 , 3]):
        raise ValueError(f'plane_dir={plane_dir}, while expected one of [1,2,3]')
    
    if parallel:
        poption = '-p'
    else:
        poption = ''
    if spinpolar:
        spoption= '-sp'
    else:
        spoption= ''

    # print input
    prolog() # Information for user
    print("User input:")
    print(f'Band range is [{i_band}-{s_band}]')
    print(f'The selected plane is perpendicular to {plane_dir} with a constant value of {plane_value}')
    print(f'Brillouin zone discretization in {n-1}x{n-1}={(n-1)*(n-1)} loops')
    print(f'Parallel calculation option is set to {parallel}')
    print(f'Spin-polarized calculation option is set to {spinpolar}')
    print('         ')
    WorkingDir, case, multiplier = preliminary()

    # Defining the meshgrid to perform the calculation
    nx , ny = (n,n)
    kx = np.linspace(boundary[0], boundary[1], nx)
    ky = np.linspace(boundary[2], boundary[3], ny)
    kxv , kyv = np.meshgrid(kx , ky, indexing = 'ij')
    
    # Function for getting the loop points
    full = [] 
    # List with the coordinates, a list with lists, each one is for a value of kx, inside there are lists of tuples with kx constant and varying ky
    for k in range(0,n):
        coordinate = np.c_[kxv[k],-kyv[k]]
        coordinate_list = coordinate.tolist()
        full.append(coordinate_list)
    
    berry_phases = [] # List of lists of berryphases per row
    count = 0
    #Iterating over very vertex
    for x in full[0:n-1]: #Iterates over the kx value lists
        col_phase = [] #Phases in column
        for y in x: #Iterates over the kx,ky tuple in each kx list
            if x.index(y) + 1 < n: #Not taking into account edge
                dn = full[full.index(x)][x.index(y)+1]
                dg = full[full.index(x)+1][x.index(y)+1]
                rt = full[full.index(x)+1][x.index(y)]
                sm = full[full.index(x)][x.index(y)]
                #Transform from 2D to 3D
                if plane_dir == 3:
                    dn = [ dn[0], dn[1], plane_value]
                    dg = [ dg[0], dg[1], plane_value]
                    rt = [ rt[0], rt[1], plane_value]
                    sm = [ sm[0], sm[1], plane_value]
                elif plane_dir == 1:
                    dn = [ plane_value , dn[0], dn[1]]
                    dg = [ plane_value , dg[0], dg[1]]
                    rt = [ plane_value , rt[0], rt[1]]
                    sm = [ plane_value , sm[0], sm[1]]
                elif plane_dir == 2:
                    dn = [ dn[0],plane_value , dn[1]]
                    dg = [ dg[0],plane_value , dg[1]]
                    rt = [ rt[0],plane_value , rt[1]]
                    sm = [ sm[0],plane_value , sm[1]]
                loop = [sm,dn,dg,rt]
                loop = np.array(loop)
                size = np.size(loop, 0)
                loop = loop*multiplier
                loop = np.c_[loop, multiplier*np.ones(size), 2.00*np.ones(size)]
                loop = np.int_(loop)
                filename = str("%s.klist"%case)
                # save case.k_list 
                np.savetxt(filename, loop, fmt="          %10i%10i%10i%10i%5.1f", 
                       delimiter='', footer='END', comments='')
                # run BerryPI
                
                proc = subprocess.Popen("python $WIENROOT/SRC_BerryPI/BerryPI/berrypi -so -w -b %i %i %s %s"%(i_band, s_band,poption,spoption), shell=True, stdout=subprocess.PIPE, \
                    stderr=subprocess.PIPE)
                proc.wait()
                (stdout, stderr) = proc.communicate()
                if proc.returncode != 0:
                    print(stderr.decode()) # need decode to deal with b'...' string
                    msg = "Error while executing BerryPI, exiting (Check Input)"
                    raise RuntimeError(msg)
                else:
                    if (count == 0): # print BerryPI stdout once
                        print(stdout.decode())
                        print('Future BerryPI output will be supressed')
                    print(f"Iteration {count+1} status: success")
                
                berrypiOutFileName = str("%s.outputberry" %(str(WorkingDir.split('/')[-1]))) #Reads output.berry
                with open(berrypiOutFileName, 'r') as read_file:  #Searches for line with berry phase
                    for line in read_file:
                        if "Berry phase sum (rad) =" in line:
                            content = line
                temp = float(content.split()[-1]) #Phase value
                temp1 = ((temp + np.pi) % (2 * np.pi) - np.pi) #2pi wrapping
                col_phase.append(temp1)
                count += 1
        berry_phases.append(col_phase) #Appends the list for each row to the total one        
    
    berry_phases_array = np.array(berry_phases)
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
    
    
    phases_horizontal = [] #List of lists by rows
    for L in range(0,len(berry_phases)):
        ph_hori = []
        for cx in berry_phases:
            for cy in cx:
                if cx.index(cy) == L:
                    ph_hori.append(cy)
        phases_horizontal.append(ph_hori)
    
    
    all_phasesh = [] #List of wrapped 2pi phases in zigzag horizontally
    for l in phases_horizontal:
        if phases_horizontal.index(l) % 2 == 0:
            all_phasesh.extend(l)
        else:
            rever_listh = list(reversed(l))
            all_phasesh.extend(rever_listh)
    all_phasesh_array = np.array(all_phasesh)
    
    
    def Unwrap(Data):
        BP = Data
        BP_out = np.unwrap(BP, discont=float(1*np.pi), axis=-1)
        diff = 0
        Check_Diff = False
        for i in BP_out:
            diff = i-diff
            if (diff > np.divide(np.pi, 2)):
                Check_Diff = True
            diff = i       
        CHERN_out = np.divide(BP_out, np.multiply(2, np.pi))
        result = [BP_out,CHERN_out]
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
    print("The total Chern number is: ",CHERNNUMBERh)
    print("(for a different phase unwrapping scheme:(",CHERNNUMBER,")") 

    if Check_diffh == True:
        print('The smoothness criteria is not achieved')
        print('Try increasing n value')
    if Check_diff == True:
        print('The smoothness criteria is not achieved (alternative unwrapping)')
        print('Try increasing n value')
    print("---------------------------------------")


    
    #PLOTS PHASE
    try:
        import matplotlib
    except ImportError as error: # matplotlib is not installed
        print (error)
        print ("matplotlib is not installed, but it is not essential.")
        print ("You can plot the figure yourself by using the berryflux.dat file.")
        print("ChernPy is done!")
        end = time.time()
        total_time = end - start
        print("The time of running was: \n"+ str(total_time)," Seconds")
        print(str(total_time/60)," Minutes")
        epilog()
        sys.exit(0)

    import matplotlib.pyplot as plt
    print ("Matplotlib found")

    #PLOT OF BERRY CURVATURE FLUX
    plt.rcParams.update({'font.size': 20, 'font.family': 'serif'})
    phases_flux = BPFinalh.tolist()
    dataf = subprocess.run(["rm berryflux.dat"],shell=True)
    dataf = subprocess.run(["touch berryflux.dat"],shell=True)
    indexes = []
    for i in range(0,len(phases_flux)+1, n-1):
        indexes.append(i)
    flag = 1
    twoDmatrixp = []
    column = []
    for l in phases_flux:
        column.append(l)
        if flag in indexes and flag > 0:
            flag += 1
            twoDmatrixp.append(column)
            stringcolumn = ','.join([str(item) for item in column])
            with open('berryflux.dat', 'a') as f:
                f.write(stringcolumn)
                f.write('\n')
            column =[]
            continue
        flag += 1
    twoDmatrix = []
    for lis in twoDmatrixp:
        if twoDmatrixp.index(lis) % 2 == 0:
            twoDmatrix.append(lis)
        else:
            tempo = list(reversed(lis))
            twoDmatrix.append(tempo)
    
    with open('berryflux.dat', 'a') as f:
        f.write('\n')
        BPFinalhst = ','.join([str(item) for item in BPFinalh])
        BPFinalhst = "berryphaseslist=["+ BPFinalhst +']'
        f.write(BPFinalhst)
        f.write('\n')
        f.write(f"Chern number: {CHERNNUMBERh}")
    print("Data stored in berryflux.dat")
    twoDmatrix = np.array(twoDmatrix)
    plt.figure(1, figsize=(15, 25))
    plt.imshow(twoDmatrix,cmap='viridis',extent=(-0.5,0.5,-0.5,0.5),interpolation='spline36',origin='lower')
    plt.xlim(-0.5,0.5)
    plt.ylim(-0.5,0.5)
    plt.xticks(np.arange(-0.5, 0.5, 0.1))
    plt.yticks(np.arange(-0.5, 0.5, 0.1))
    plt.colorbar()
    plt.ylabel(r'$k_{y}$')
    plt.xlabel(r'$k_{x}$')
    if name != "":
        plt.title(r'Flux of Berry Curvature: %s'%name)
    else:
        plt.title(r'Flux of Berry Curvature: %s'%case)

    plt.savefig("berryflux.png",dpi=500)
    print ("Output figure ""berryflux.png"" generated.")
    

    

     
    


    
    
    



































































































