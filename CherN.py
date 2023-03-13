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
    bands = [1,1] # band range (i_band,f_band) (i_band is must be => 1 ,f_band must be => to i_band)
    n_1 = 1 # discretization of brillouin zone by (n-1) in the 1 direction
    n_2 = 1 # discretization of brillouin zone by (n-1) in the 2 direction
    plane_dir = 3   # direction normal to the plane  (1 or 2 or 3)
    plane_height = 0.0 # value of the constant plane
    boundary = [0,1.0,0,1.0] #boundary selection: ex if plane_dir = 3 -> [1min,1max,2min,2max]
    parallel = False  # parallel option [-p] in BerryPI (needs a proper .machines file)
    spinpolar = False # spin polarized [-sp] in BerryPI
    orbital = False # additional orbital potential [-orb] in BerryPI
    name = "" #optional (if left as "" the name of the working directory by default)
    return bands,n_1,n_2,plane_dir,plane_height,parallel,spinpolar,boundary,name,orbital



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
(ex: plane_dir = '3', plane_height = 0.0)

plane_dir:
    This is a direction in k space for which a perpendicular plane is constructed and later discretized for the computing of C. 
plane_height:
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
    bands,n_1,n_2,plane_dir,plane_height,parallel,spinpolar,boundary,name,orbital = user_input()
    # Check input
    if type(bands[0]) != int:
        raise ValueError(f'i_band={bands[0]}, while expected an integer')
    elif type(bands[1]) != int:
        raise ValueError(f's_band={bands[1]}, while expected an integer')
    elif type(n_1) != int:
        raise ValueError(f'n_1={n_1}, while expected an integer')
    elif type(n_2) != int:
        raise ValueError(f'n_1={n_2}, while expected an integer')
    elif type(plane_dir) != int:
        raise ValueError(f'plane_dir={plane_dir}, while expected an integer')    
    if bands[0] > bands[1]:
        raise ValueError(f'i_band={bands[0]} > s_band{bands[1]}')
    if bands[0] < 0 or bands[1] < 0 or n_1 < 0 or n_2 < 0:
        raise ValueError(f'The values for i_band, s_band, n_1 and n_2 should be positive.')
    if n_1 < 1:
        raise ValueError(f'n_1={n_1}, while expected a value greater than 1')
    elif n_2 < 1:
        raise ValueError(f'n_2={n_2}, while expected a value greater than 1')
    elif bands[0] == 0 or bands[1] == 0:
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
    if orbital:
        orboption = '-orb'
    else:
        orboption = ''
    # print input
    prolog() # Information for user
    print("User input:")
    print(f'Band range is [{bands[0]}-{bands[1]}]')
    print(f'The selected plane is perpendicular to {plane_dir} with a constant value of {plane_height}')
    print(f'Brillouin zone discretization in {n_1-1}x{n_2-1}={(n_1-1)*(n_2-1)} loops')
    print(f'Parallel calculation option is set to {parallel}')
    print(f'Spin-polarized calculation option is set to {spinpolar}')
    print(f'Additional orbital calculation option is set to {orbital}')
    print('         ')
    WorkingDir, case, multiplier = preliminary()
    #Get kvectors
    proce = subprocess.Popen("grep -A 3 'G1' %s.outputkgen | tail -n 4 > kvectors"%case,shell=True)

    # Defining the meshgrid to perform the calculation
    nx , ny = (n_1,n_2)
    kx = np.linspace(boundary[0], boundary[1], nx)
    ky = np.linspace(boundary[2], boundary[3], ny)
    kxv , kyv = np.meshgrid(kx , ky, indexing = 'ij')
    
    # Function for getting the loop points
    full = [] 
    # List with the coordinates, a list with lists, each one is for a value of kx, inside there are lists of tuples with kx constant and varying ky
    for k in range(0,n_1):
        coordinate = np.c_[kxv[k],-kyv[k]]
        coordinate_list = coordinate.tolist()
        full.append(coordinate_list)
    
    berry_phases = [] # List of lists of berryphases per row
    count = 0
    #Iterating over very vertex
    for x in full[0:n_1-1]: #Iterates over the kx value lists
        col_phase = [] #Phases in column
        for y in x: #Iterates over the kx,ky tuple in each kx list
            if x.index(y) + 1 < n_1: #Not taking into account edge
                dn = full[full.index(x)][x.index(y)+1]
                dg = full[full.index(x)+1][x.index(y)+1]
                rt = full[full.index(x)+1][x.index(y)]
                sm = full[full.index(x)][x.index(y)]
                #Transform from 2D to 3D
                if plane_dir == 3:
                    dn = [ dn[0], dn[1], plane_height]
                    dg = [ dg[0], dg[1], plane_height]
                    rt = [ rt[0], rt[1], plane_height]
                    sm = [ sm[0], sm[1], plane_height]
                elif plane_dir == 1:
                    dn = [ plane_height , dn[0], dn[1]]
                    dg = [ plane_height , dg[0], dg[1]]
                    rt = [ plane_height , rt[0], rt[1]]
                    sm = [ plane_height , sm[0], sm[1]]
                elif plane_dir == 2:
                    dn = [ dn[0],plane_height , dn[1]]
                    dg = [ dg[0],plane_height , dg[1]]
                    rt = [ rt[0],plane_height , rt[1]]
                    sm = [ sm[0],plane_height , sm[1]]
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
                
                proc = subprocess.Popen("python $WIENROOT/SRC_BerryPI/BerryPI/berrypi -so -w -b %i %i %s %s %s"%(bands[0], bands[1],poption,spoption,orboption), shell=True, stdout=subprocess.PIPE, \
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
    
    
    

    if Check_diffh == True:
        print('The smoothness criteria is not achieved')
        print('Try increasing n_1 and n_2 value')
    elif Check_diff == True:
        print('The smoothness criteria is not achieved (alternative unwrapping)')
        print('Try increasing n _1 and n_2 value')
    else:
        if abs(boundary[0])+abs(boundary[1])==1 and abs(boundary[2])+abs(boundary[3])==1:
            print("---------------------------------------")
            print("The total Chern number is: ",round(CHERNNUMBERh,5))
            print("(for a different phase unwrapping scheme:(",round(CHERNNUMBER,5),")") 
        else:
            print("---------------------------------------")
            print("The total Berry curvature flux for the selected boundary: ",round(CHERNNUMBERh,5))
            print("(for a different phase unwrapping scheme:(",round(CHERNNUMBER,5),")") 
        


    
    #PLOTS PHASE
    try:
        import matplotlib
    except ImportError as error: # matplotlib is not installed
        print (error)
        print ("matplotlib is not installed, but it is not essential.")
        print ("You can plot the figure yourself by using the berryflux.dat file.")
        sys.exit(0)

    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    print ("Matplotlib found")

    #PLOT OF BERRY CURVATURE FLUX
    plt.rcParams.update({'font.size': 20, 'font.family': 'serif'})
    phases_flux = BPFinal.tolist()
    dataf = subprocess.run(["rm berryflux.dat"],shell=True)
    dataf = subprocess.run(["touch berryflux.dat"],shell=True)
    indexes = []
    for i in range(0,len(phases_flux)+1, n_1-1):
        indexes.append(i)
    flag = 1
    twoDmatrixp = []
    column = []
    for l in phases_flux:
        column.append(l)
        if flag in indexes and flag > 0:
            flag += 1
            #twoDmatrixp.append(column)
            twoDmatrixp.append(list(reversed(column)))
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
        BPFinalhst = "berryphaseslisth=["+ BPFinalhst +']'
        
        BPFinalvst = ','.join([str(item) for item in BPFinal])
        BPFinalvst = "berryphaseslistv=["+ BPFinalvst +']'     
        f.write(BPFinalhst)
        f.write('\n')
        f.write(BPFinalvst)
        f.write('\n')        
        f.write(f"Chern number: {CHERNNUMBER}")
    print("Data stored in berryflux.dat")


    #Normalization to units
    twoDmatrix = np.array(twoDmatrix)
    twoDmatrix = twoDmatrix/(((1)/(n_1-1))*(((1)/(n_2-1))))


    
    lines=[]
    path = os.path.dirname(__file__)
    filename = os.path.join(path, 'kvectors')
    with open (filename,"rt") as myfile:
        for myline in myfile:
            lines.append(myline.rstrip('\n'))
    linef = lines[1:3]
    L1 = linef[0].split()
    L2 = linef[1].split()

    G1x = float(L2[0])
    G1y = float(L1[0])
    G2x = float(L2[1])
    G2y = float(L1[1])


    #Non orthogonal graph
    nx, ny = n_1-1, n_2-1
    cell =  np.array([[G2x,G2y]
                     , [G1x,G1y ]
    ])
    
    x0, y0 = np.mgrid[0:1.0:1j*nx, 0:1.0:1j*ny]
    x1, y1 = np.tensordot(cell, [x0, y0], axes=(0, 0))
    
    
    plt.figure(figsize=(15, 15))
    plt.pcolormesh(x1, y1, twoDmatrix, shading='gouraud', cmap='seismic')
    ax = plt.gca()
    plt.axis('off')
    ax.axes.set_aspect('equal')
    plt.colorbar()
    plt.tight_layout()
    
    # Define two vectors as arrays
    v1 = np.array([G2x, G2y])
    v2 = np.array([G1x, G1y])

    # Plot the two vectors
    ax.quiver([0, 0], [0, 0], [v1[0], v2[0]], [v1[1], v2[1]],
              angles='xy', scale_units='xy', scale=1)

    # Add points along the first vector
    arrayg = np.array([0.2, 0.4, 0.6, 0.8, 1])
    v1_points = v1 * arrayg.reshape(-1, 1)
    for i, point in enumerate(v1_points):
        ax.scatter(point[0], point[1], color='black', s=1)
        ax.annotate(f'{round(arrayg[i],1)}', xy=(
            point[0], point[1]), xytext=(20, -5), textcoords='offset points')

    ax.annotate(r'$b_{2}$', xy=(v1[0]*0.5, v1[1]*0.5),
                xytext=(80, -40), textcoords='offset points')



    v2_points = v2 * arrayg.reshape(-1, 1)
    for i, point in enumerate(v2_points):
        ax.scatter(point[0], point[1], color='black', label='none', s=1)
        ax.annotate(f'{round(arrayg[i],1)}', xy=(
            point[0], point[1]), xytext=(-50, -25), textcoords='offset points')

    ax.annotate(r'$b_{1}$', xy=(v2[0]*0.5, v2[1]*0.5),
                xytext=(-80, -40), textcoords='offset points')
    ax.set_xlim([-0.2, v1[1]+0.7])
    ax.set_ylim([-0.1, v2[1]+0.7])
    plt.rcParams.update({'font.size': 20, 'font.family': 'serif'})
    
    if name != "":
        plt.title(r'Flux of Berry Curvature: %s' % name)
    else:
        plt.title(r'Flux of Berry Curvature: %s' % case)

    plt.savefig("berryflux.png", dpi=500)
    plt.savefig("berryflux.pdf", dpi=500)
    print("Output figure ""berryflux"" generated.")

    
    print("CherN.py is done!")
    end = time.time()
    total_time = end - start
    print("The time of running was: \n"+ str(total_time)," seconds")
    print(str(total_time/60)," minutes")
    epilog()
