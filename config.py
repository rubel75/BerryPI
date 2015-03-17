'''
This file includes configuration for the berry simulation automation
process.

1. I setup the automation to accept a special object, this object can
be created automatically.
'''

#######################################################
#### DEFAULT PATHS ####################################
#######################################################

#fix for location of python file locations when executing from the python commandline
DEFAULT_BIN_PATH='/home/rubel/BerryPI'

#Fix for python path to make sure it grabs the latest version
DEFAULT_PYTHON_PATH='/software/CentOS-6/tools/python-2.7.3/bin/python'

########################################################
####Some default values for the automation of each case
########################################################

#NUMBER OF K-POINTS IN WHOLE CELL: (0 allows to specify 3 divisions of G)
DEFAULT_NUMBER_OF_KPOINTS = 0 #Recommended not to change


#This value is used if one isn't provided in the configuration
#for key 'K-Mesh Divisions'
DEFAULT_KMESH_DIVISIONS = (10,10,10)

#Shift of k-mesh allowed. Do you want to shift: (0=no, 1=shift)
DEFAULT_KMESH_SHIFT = 0 #Always 0

#Enter minimal and maximal Bloch band,[n1 n2]:
DEFAULT_BLOCH_BAND = None


#Enter number of Wannier functions,[n1]:
DEFAULT_WANNIER_FUNCTIONS = 1

#Enter center atom and character[n1 s/p/d/f]:(e.g.: 2 d)
DEFAULT_CENTER_ATOM_AND_CHARACTER = '2 d' 
####


#Include LAPW1 (True, False)
DEFAULT_INCLUDE_LAPW1 = True

#Determines if lapw1 is performed in parallel
DEFAULT_INCLUDE_LAPW1_PARALLEL = False

####Configuration Options for entire automation process

#If True, the first error the automation comes upon will prevent the
#process from continuing
BERRY_EXIT_ON_ERROR = True

#prefix displayed in the terminal
BERRY_DEFAULT_CONSOLE_PREFIX = '[ BerryPI ] '

#extension used for the file to store the polarized value output
BERRY_FILE_EXTENSION = '.berrypi'

####

#insert objects like the exampleObject into the automation list before running
berryPyConfigAutomationList = []
#################################################################################
############################## Configuration For Each AUTOMATION ################
#################################################################################

#I get a segmentation fault when I run this (?????)
lattice0_config = {
    'Structure Name' : 'AlAs',
    'Structure Path' : '/home/stud2/AlAs',
    'Number of K-Points' : DEFAULT_NUMBER_OF_KPOINTS, #always use Default
    'K-Mesh Divisions' : (6,6,6), #X, Y, Z
    'K-Mesh Shift' : DEFAULT_KMESH_SHIFT, #always use Default
    'Bloch Band Range' : DEFAULT_BLOCH_BAND,
    'Number of Wannier Functions' : DEFAULT_WANNIER_FUNCTIONS, #always use Default
    'Center Atom and Character' : DEFAULT_CENTER_ATOM_AND_CHARACTER, #always use Default
    'Perform LAPW1' : DEFAULT_INCLUDE_LAPW1,
    'LAPW1 in Parallel' : DEFAULT_INCLUDE_LAPW1_PARALLEL,
}

ba_config = {
    'Structure Name' : 'BaTiO3-centrio',
    'Structure Path' : '/home/stud2/BaTiO3-berry/BaTiO3-tetra/experimentalBaTiO3/BaTiO3oldwien2k/BaTiO3min/BaTiO3min_vol__-2.0/BaTiO3-centrio',
    'Number of K-Points' : DEFAULT_NUMBER_OF_KPOINTS, #always use Default
    'K-Mesh Divisions' : (10,10,9), #X, Y, Z
    'K-Mesh Shift' : DEFAULT_KMESH_SHIFT, #always use Default
    'Bloch Band Range' : DEFAULT_BLOCH_BAND,
    'Number of Wannier Functions' : DEFAULT_WANNIER_FUNCTIONS, #always use Default
    'Center Atom and Character' : DEFAULT_CENTER_ATOM_AND_CHARACTER, #always use Default
    'Perform LAPW1' : DEFAULT_INCLUDE_LAPW1,
    'LAPW1 in Parallel' : DEFAULT_INCLUDE_LAPW1_PARALLEL,
}

ba_test = {
    'Structure Name' : 't-Se',
    'Structure Path' : '/home/stud2/Se-polarization/lambda0/t-Se',
    'Number of K-Points' : DEFAULT_NUMBER_OF_KPOINTS, #always use Default
    'K-Mesh Divisions' : (10,10,10), #X, Y, Z
    'K-Mesh Shift' : DEFAULT_KMESH_SHIFT, #always use Default
    'Bloch Band Range' : DEFAULT_BLOCH_BAND,
    'Number of Wannier Functions' : DEFAULT_WANNIER_FUNCTIONS, #always use Default
    'Center Atom and Character' : DEFAULT_CENTER_ATOM_AND_CHARACTER, #always use Default
    'Perform LAPW1' : DEFAULT_INCLUDE_LAPW1, #False, #True --> include lapw1, False --> don't include lapw1
    'LAPW1 in Parallel' : DEFAULT_INCLUDE_LAPW1_PARALLEL,

}

ba_test2 = {
    'Structure Name' : 'BaTiO3-centrio',
    'Structure Path' : '/home/stud2/BaTiO3-berry/BaTiO3-centrio',
    'Number of K-Points' : DEFAULT_NUMBER_OF_KPOINTS, #always use Default
    'K-Mesh Divisions' : (10,10,10), #X, Y, Z
    'K-Mesh Shift' : DEFAULT_KMESH_SHIFT, #always use Default
    'Bloch Band Range' : DEFAULT_BLOCH_BAND,
    'Number of Wannier Functions' : DEFAULT_WANNIER_FUNCTIONS, #always use Default
    'Center Atom and Character' : DEFAULT_CENTER_ATOM_AND_CHARACTER, #always use Default
    'Perform LAPW1' : DEFAULT_INCLUDE_LAPW1,
    'LAPW1 in Parallel' : DEFAULT_INCLUDE_LAPW1_PARALLEL,

}



##############################################
################## Run List ##################
##############################################


#berryPyConfigAutomationList.append(lattice0_config)
#berryPyConfigAutomationList.append(ba_config)
#berryPyConfigAutomationList.append(ba_test)
#berryPyConfigAutomationList.append(ba_test2)


################################################################################
##############################  END  ###########################################
################################################################################

