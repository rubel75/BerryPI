'''
This file includes default variables/configurations for the Berry phase
calculations.
'''

########################################################
####Some default values for the automation of each case
########################################################

#NUMBER OF K-POINTS IN WHOLE CELL: (0 allows to specify 3 divisions of G)
DEFAULT_NUMBER_OF_KPOINTS = 0 #Recommended not to change

#This value is used if one isn't provided in the configuration
#for key 'K-Mesh Divisions'
DEFAULT_KMESH_DIVISIONS = (10,10,10)

#Shift of k-mesh allowed. Do you want to shift: (0=no, 1=shift)
DEFAULT_KMESH_SHIFT = 0

#Enter number of Wannier functions,[n1]:
DEFAULT_WANNIER_FUNCTIONS = 1

#Enter center atom and character[n1 s/p/d/f]:(e.g.: 2 d)
DEFAULT_CENTER_ATOM_AND_CHARACTER = '2 d' 

#If True, the first error the automation comes upon will prevent the
#process from continuing
BERRY_EXIT_ON_ERROR = True

#prefix displayed in the terminal
BERRY_DEFAULT_CONSOLE_PREFIX = '[ BerryPI ] '
