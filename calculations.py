'''
File includes all of the necessary code to perform calculations and
return necessary values for each step in the automation process

The classes are setup to accept dictionary argument passing read the
help() on each class to understand what you need to pass in order to
ensure correct operation

upon calling the class, it returns the appropriate values upon which
it has been asked to return.

*Essentially it is a function*
'''
import math, pprint

import errorCheck as b_PyError
import parsing as b_PyParse
import numpy

from collections import OrderedDict as orderedDict
from config import BERRY_DEFAULT_CONSOLE_PREFIX as DEFAULT_PREFIX

DEBUG = True


##################
# default values #
##################

ELECTRON_CHARGE = 1.60217646e-19
#bohr to meters
BOHR_CONSTANT = 5.29e-11

#value which determines the bounds 
#of zeroing our 2pi values
GAMMA_ZEROING_VALUE = 0.000001

COORDINATE_CORRECTION_UPPER_BOUND = 1.0
COORDINATE_CORRECTION_LOWER_BOUND = 0.8

class PathphaseCalculation:
    '''
    -- arguments --

    values(list) : list of berry phase values which you wish to pass
    to the calculation

    
    '''
    def __init__(self, **arguments):
        self.topDomain = math.pi * 2
        self.values = arguments['values']
        self.correctDomain() #produces correct domain in self.correctedValues
        self.meanValue = (sum(self.correctedValues) / len(self.correctedValues)) / (self.topDomain/2)
	#print self.meanValue
    def correctDomain(self):
        '''
        Correct the domain of the pathphase values so that they lie
        within the [0, 2PI] domain -- [0. 6.28]
        '''
        topDomain = self.topDomain

        self.correctedValues = self.values[:]

        #use modulo 2PI to maintain a consistent domain
        self.correctedValues = [ (i + (2 *numpy.pi)) % topDomain for i in self.correctedValues ]

#	self.correctedValues = [ numpy.unwrap(i) for i in self.correctedValues ]
        #function to add topDomain when value is less than zero
        def correctNegation(x):
            if x < 0: return x + topDomain
            else: return x
        self.correctedValues = map(
                                   correctNegation,
                                   self.correctedValues
                                   )

        #correct for 2*pi values which should be
        #zero
        def correctToZero(x):
            if x > (self.topDomain - GAMMA_ZEROING_VALUE):
                return 0.
            else:
                return x
        self.correctedValues = map(
                                   correctToZero,
                                   self.correctedValues
                                  )
        #print self.correctedValues
        return self.correctedValues
        
    def getValues(self):
        return self.values

    def getCorrectedValues(self):
        return self.correctedValues

    def getMeanValue(self):
        return self.meanValue

class CalculateNumberOfBands:
    '''
    Used to calculate the number of bands within the *.scf file to
    determine the input for the write_w2win function.

    You pass a file path to the *.scf in order to carry out this
    calculation
    '''
    def __init__(self, filePath):
        self.text = open(filePath, 'r').readlines()
        self.parser = b_PyParse.MainSCFParser(self.text)
        self.parser.parse()

    def getNumberOfBands(self):
        bandList = self.parser['Band List']
        #produce list from dictionary values with only the occupancy
        #and band range where occupancy is not 0
        theList = [ (i['band range'], i['occupancy']) for i in bandList if i['occupancy'] ]
        # return the last occupancy
        return theList[-1][0]

    
        

class MainCalculationContainer:
    '''
    This class contains every calculation and spits out the final result

    -- arguments --
    file_pathphase_x(file path) - to x-coordinate .pathphase file
    
    file_pathphase_y(file path) - to y-coordinate .pathphase file

    file_pathphase_y(file path) - to z-coordinate .pathphase file

    file_struct(file path) - to structure .struct file

    file_scf(file path) - to .scf file

    file_outputd(file path) - to .outputd file

    file_outputst(file path) - to .outputst file
    '''
    def __init__(self, **arguments):
        ############################
        ######### PARSING ##########
        ############################

        ###Rest of the Files###
        #parse all the things!
        #### *.struct file parser
        parser_struct_handle = open(arguments['file_struct'], 'r').readlines()
        parser_struct_handle = b_PyParse.MainStructParser(parser_struct_handle)
        parser_struct_handle.parse()


        #### *.scf file parser
        parser_scf_handle = open(arguments['file_scf'], 'r').readlines()
        parser_scf_handle = b_PyParse.MainSCFParser(parser_scf_handle)
        parser_scf_handle.parse()


        #### *.outputd parser
        parser_outputd_handle = open(arguments['file_outputd'], 'r').readlines()
        parser_outputd_handle = b_PyParse.MainOutputDParser(parser_outputd_handle)
        parser_outputd_handle.parse()

        
        #### *.outputst parser
        parser_outputst_handle = open(arguments['file_outputst'], 'r').readlines()
        parser_outputst_handle = b_PyParse.MainOutputstParser(parser_outputst_handle)
        parser_outputst_handle.parse()


        #####################################
        ############ END Parsing ############
        #####################################


        #############################
        ###### Getting Values #######
        #############################
        self._calculationValues = orderedDict();
        
        #### *.struct handle
        # - determine name of atoms
        # - determine MULT for each atom
        self._calculationValues['Atom Listing'] = parser_struct_handle['Atom Listing']
        
        #### *.scf handle
        # - Cell Volume
        self._calculationValues['Cell Volume in bohr^3'] = parser_scf_handle['Cell Volume']
        self._calculationValues['Cell Volume in m^3'] = bohrToMeters(self._calculationValues['Cell Volume in bohr^3'],3)
        #### *.outputd handle
        # - BR2_DIR matrix (v_x, v_y, v_z)
        # - number of atoms in cell
        # - Lattice Constants (x,y,z)
	laticematrix=parser_outputd_handle['BR2_DIR Matrix']
	latticematrixa1=laticematrix[0]
	self._calculationValues['Lattice Matrix a1 in bohr']=latticematrixa1
	latticematrixa2=laticematrix[1]
	self._calculationValues['Lattice Matrix a2 in bohr']=latticematrixa2
	latticematrixa3=laticematrix[2]
	self._calculationValues['Lattice Matrix a3 in bohr']=latticematrixa3
        self._calculationValues['Lattice Matrix in bohr'] = parser_outputd_handle['BR2_DIR Matrix']
        self._calculationValues['Lattice Matrix in m'] = [[ bohrToMeters(i) for i in j ] for j in self._calculationValues['Lattice Matrix in bohr']]
        self._calculationValues['Number of Atoms in Unit Cell'] = parser_outputd_handle['Number of Atoms in Unit Cell']
        self._calculationValues['Lattice Constants in bohr'] = parser_outputd_handle['Lattice Constants']
        self._calculationValues['Lattice Constants in m'] = [ bohrToMeters(i) for i in self._calculationValues['Lattice Constants in bohr']]

        #### *.outputst handle
        # for each element:
        # - Core Value
        # - Spin Value 1
        # - Spin Value 2
        self._calculationValues['Element Listing'] = parser_outputst_handle['Element List']

        ####
        
        #### PATHPHASE ####
        #*.pathphases parsers
        #get text strings from each file
        phaseFilesList = [
            arguments['file_pathphase_x'],
            arguments['file_pathphase_y'],
            arguments['file_pathphase_z'],
            ]
        #read from files
        phaseTextStringsList = [ open(i,'r').readlines() for i in phaseFilesList ]
        #parse the values
        phaseValues = [ b_PyParse.MainPathphaseParser(i) for i in phaseTextStringsList ]
        for i in phaseValues: 
            i.parse()
        #send to pathphasecalculation for correction
        phaseObjects = [ PathphaseCalculation(values=i['values']) for i in phaseValues ]
        #receive mean values
        value_phaseCorrectedValues = [ i.getCorrectedValues() for i in phaseObjects ]

        self.value_phaseMeanValues = value_phaseMeanValues = [ i.getMeanValue() for i in phaseObjects ]
	#print self.value_phaseMeanValues

        #constants
        #electron charge / unit volume
        self.ELEC_BY_VOL_CONST = ELECTRON_CHARGE / bohrToMeters(self._calculationValues['Cell Volume in bohr^3'], dimension = 3.)
        #perform necessary calculations
        self.determineElectronPolarization()
        self.determineIonPolarization()
        self.calculateNetPolarizationEnergy()

    def valuephaseMeanValues(self):
	return self.value_phaseMeanValues

    def __call__(self):
        return self.netPolarizationEnergy()

    def calculationValues(self):
        return self._calculationValues

    def prettyPrintCalculationValues(self):
        pprint.pprint(self._calculationValues)
    
    def determineElectronPolarization(self):
        '''
        Calculate the flux capacitance of the electron fermion fields
        TODO write an actual good description later

        Calculation:

        Pel_x = electron charge / unit volume (m) * berry phase mean value *
          lattice_matrices (diagonal x)
        '''
        self._electronPolarization = []
	self._ebyVandlatticeconstant = []
        calcValues = self.calculationValues()
	berryphase = self.valuephaseMeanValues()
        ELEC_BY_VOL_CONST = self.ELEC_BY_VOL_CONST
	latticeConstants = calcValues['Lattice Constants in bohr']
        latticeMatrix_x = calcValues['Lattice Matrix in bohr'][0]
        latticeMatrix_y = calcValues['Lattice Matrix in bohr'][1]
        latticeMatrix_z = calcValues['Lattice Matrix in bohr'][2]
        # split up lattice matrix into respective form
        #latticeMatrix_x = [ i[0] for i in calcValues['Lattice Matrix'] ]
        #latticeMatrix_y = [ i[1] for i in calcValues['Lattice Matrix'] ]
        #latticeMatrix_z = [ i[2] for i in calcValues['Lattice Matrix'] ]
        # take the absolute value of the vector sqrt(x^2 + y^2 + z^2)
        absVector = lambda vec: math.sqrt(sum([i**2 for i in vec]))
        #absolute matrices values (look oddly similar to lattice constants......)
        lattice_x = absVector(latticeMatrix_x)
        lattice_y = absVector(latticeMatrix_y)
        lattice_z = absVector(latticeMatrix_z)
	### e/V*latticeconstant
	self._ebyVandlatticeconstant.append(ELEC_BY_VOL_CONST * bohrToMeters(latticeConstants[0]))
 	self._ebyVandlatticeconstant.append(ELEC_BY_VOL_CONST * bohrToMeters(latticeConstants[1]))
 	self._ebyVandlatticeconstant.append(ELEC_BY_VOL_CONST * bohrToMeters(latticeConstants[2]))
       

	print  DEFAULT_PREFIX + "e/V*lattice constant\n           "+str(self._ebyVandlatticeconstant)+"\n"
	

	###Electronic/Berry Phase Remapping in between -pi to +pi to calculate electronic Polrization	
	remappedberryx=self.correctPhaseDomain( berryphase[0])
	remappedberryy=self.correctPhaseDomain( berryphase[1])
	remappedberryz=self.correctPhaseDomain( berryphase[2])
	self._berryremapped=[ remappedberryx, remappedberryy, remappedberryz ]


        #### CALCULATION ####
        self._electronPolarization.append(
            ELEC_BY_VOL_CONST * remappedberryx* bohrToMeters(latticeConstants[0])
            )
        self._electronPolarization.append(
            ELEC_BY_VOL_CONST * remappedberryy* bohrToMeters(latticeConstants[1]))
        self._electronPolarization.append(
            ELEC_BY_VOL_CONST * remappedberryz * bohrToMeters(latticeConstants[2])
            )
        #### DONE ####
        return self._electronPolarization
    
    def remappedberryphase(self):	
	return self._berryremapped
	print self.remappedberryphase	

    def ebyVlatticeconstant(self):		
	return self._ebyVandlatticeconstant	

    def electronPolarization(self):
        return self._electronPolarization

    def determineIonPolarization(self):
        '''
        Calculation:

        Pion_x = electron charge / unit volume (m) * lattice_x * (
        
          sum of (
            atom valence charge * position(x)
            )
          )

          where atom valence charge = ( core value - spin val 1 - spin val 2 )
        '''
        self._ionPolarization = []
        calcValues = self.calculationValues()

        ELEC_BY_VOL_CONST = self.ELEC_BY_VOL_CONST

        latticeConstants = calcValues['Lattice Constants in bohr']

        atomListing = calcValues['Atom Listing']

        #produce a tuple pair which includes the valence electrons and
        #the coordinates for each element
        calcIonValues = [] # (coordinates(x,y,z), valence value)
        
        #TODO: include good exception handling for this stage
        #construct the calcIonValues for the calculation
        for atom in atomListing:
            for i in range(atom['MULT']):
                theElementName = atom['Element Name']
		
                if calcValues['Element Listing'].has_key(theElementName):
                    theElement = calcValues['Element Listing'][theElementName]
                    theValence = -theElement['Core Value'] + theElement['Spin Value 1'] + theElement['Spin Value 2']
                    xCoordinate = atom['X-Coord'][i]
                    yCoordinate = atom['Y-Coord'][i]
                    zCoordinate = atom['Z-Coord'][i]
		 

                    #produce tuple from coordinates
                    coordinates = (xCoordinate, yCoordinate, zCoordinate)
		    
                    allinfo = [theElementName,theValence,coordinates]
                    print str(allinfo)

                    #correct coordinates which are close to 1.0 between 
                    #(COORDINATE_CORRECTION_LOWER_BOUND,COORDINATE_CORRECTION_UPPER_BOUND)
                   # def correctCoordinates(x):
                    #    if x > COORDINATE_CORRECTION_LOWER_BOUND:
                     #      print DEFAULT_PREFIX + "WARNING:Coordinate {} has been corrected to {} to account for periodic boundary condition".format(x, x-1)
                      #     return x - 1.
                       # else: return x
                  #  coordinates = map(correctCoordinates, coordinates)
                  #  append to calcIonValues list
                    calcIonValues.append((coordinates, theValence))
                else:
                    print DEFAULT_PREFIX + 'ERROR: Missing element in element list'
                    print DEFAULT_PREFIX + theElementName
                    print DEFAULT_PREFIX + calcValues['Element List']
                    print DEFAULT_PREFIX + 'Exiting....'
                    sys.exit(1)
                    
        #### CALCULATION ####
        xPolarIon, yPolarIon, zPolarIon = (0., 0., 0.)

        #coordinates were converted from bohr
        for iCoord, iValence in calcIonValues:
            xPolarIon += iCoord[0] * iValence
            yPolarIon += iCoord[1] * iValence
            zPolarIon += iCoord[2] * iValence
        #    print DEFAULT_PREFIX + " Coord (x,y,z) - Valence - " + str(((iCoord[0],iCoord[1],iCoord[2]),(iValence)))
        #    print DEFAULT_PREFIX + " Coord * Valence (x,y,z) - " + str((xPolarIon,yPolarIon,zPolarIon))
	#Correction of Polarion to 2pi domain As it should not be negetive so no negetive correction function was added
	topPi=2
	xPolarionCorrected=xPolarIon%topPi
	yPolarionCorrected=yPolarIon%topPi
        zPolarionCorrected=zPolarIon%topPi
	self._ionicphase=[ xPolarionCorrected, yPolarionCorrected, zPolarionCorrected ]
	
	# Remapping of Ionic Phase in -pi to +pi for Ionic Polarization 
	xPolrionmapped= self.correctPhaseDomain(xPolarionCorrected)
	yPolrionmapped= self.correctPhaseDomain(yPolarionCorrected)
	zPolrionmapped= self.correctPhaseDomain(zPolarionCorrected)
	self._mappedionic=[ xPolrionmapped, yPolrionmapped, zPolrionmapped ]
         

#	print DEFAULT_PREFIX + " New Polarion " + str((xPolarionCorrected,yPolarionCorrected,zPolarionCorrected))
        #lattice constants were converted from bohr
        xPolrionmapped *= ELEC_BY_VOL_CONST * bohrToMeters(latticeConstants[0])
#        print DEFAULT_PREFIX + "(eV//V, Lattice Constant X, Lat_x in Meters) - " + str((ELEC_BY_VOL_CONST, latticeConstants[0], bohrToMeters(latticeConstants[0])))
        yPolrionmapped *= ELEC_BY_VOL_CONST * bohrToMeters(latticeConstants[1])
#        print DEFAULT_PREFIX + "(eV//V, Lattice Constant Y, Lat_y in Meters)  - " + str((ELEC_BY_VOL_CONST, latticeConstants[1], bohrToMeters(latticeConstants[1])))
        zPolrionmapped *= ELEC_BY_VOL_CONST * bohrToMeters(latticeConstants[2])
 #       print DEFAULT_PREFIX + "(eV//V, Lattice Constant Z, Lat_z in Meters)  - " + str((ELEC_BY_VOL_CONST, latticeConstants[2], bohrToMeters(latticeConstants[2])))
	self._ionPolarization = [ xPolrionmapped, yPolrionmapped, zPolrionmapped ]
        ######## END ########
        return self._ionPolarization

    def ionicphase(self):
	return self._ionicphase
    def mappedionic(self):
	return self._mappedionic
    def ionPolarization(self):
        return self._ionPolarization

    def correctPhaseDomain(self,phaseValue):
        '''
        Corrects the values phase so that it resides 
        between topDomain and bottomDomain
        '''
        topDomain = 1.
        bottomDomain = -1.

        domainRange = topDomain - bottomDomain

	phaseValue %= domainRange
        if phaseValue >= topDomain or phaseValue <= bottomDomain:
	        if phaseValue > 0:
		    phaseValue -= domainRange
	        elif phaseValue <= 0:
	            phaseValue += domainRange
        return phaseValue	

    def calculateNetPolarizationEnergy(self):
        '''
	Need to correct the Berryphase so that it resides in the
	-pi to +pi domain (-1 to 1)
        '''
        elecPolar = self.electronPolarization()
        ionPolar = self.ionPolarization()
	ionicphase = self.ionicphase()
	ionicremapped=self.mappedionic()
	electronicphase=self.value_phaseMeanValues
	electronicphaseremapped=self.remappedberryphase()

	print DEFAULT_PREFIX + "Ionic Phase in the unit of 2*pi [2*pi modulo]:\n           "+str( ionicphase)+"\n"
	self._calculationValues['Ionic Phase - Units of 2*pi [2*pi modulo]'] = ionicphase
	print DEFAULT_PREFIX + "Ionic Phase remapped in the unit of 2*pi [-pi to +pi]:\n           "+str(ionicremapped)+"\n"
	self._calculationValues['Ionic Phase - Units of 2*pi domain[-pi to +pi]'] = ionicremapped
	print DEFAULT_PREFIX + "Ionic Polarizaion in C/m^2:\n           "+str( ionPolar)+"\n"
	self._calculationValues['Ionic Polrization in C/m^2'] = ionPolar


	print DEFAULT_PREFIX + "Electronic Phase in the unit of 2*pi[2pi modulo]:\n            "+str(electronicphase)+"\n"
	self._calculationValues['Electronic Phase - Units of 2*pi in the domain [0 to 2pi]'] = electronicphase

	print DEFAULT_PREFIX + "Electronic Phase remapped in the init of 2*pi [-pi to +pi]:\n           "+str(electronicphaseremapped)+"\n"
	self._calculationValues['Electronic Phase - Units of 2*Pi domain[-pi to +pi]'] = electronicphaseremapped

	print DEFAULT_PREFIX + "Electronic Polarization in C/m^2:\n           "+str(elecPolar)+"\n"
	self._calculationValues['Electronic Polrization in C/m^2'] = elecPolar

	#Zipping  values together and summing them
	ionicphase = [ i * 2 * math.pi for i in ionicphase ]
	electronicphase = [ i * 2 * math.pi for i in electronicphase ]
        self._netPolarizationEnergy = zip(ionicphase, electronicphase)
	self._netPolarizationEnergy = [sum(i) for i in self._netPolarizationEnergy ]
	self._netPolarizationEnergy= [i / ( 2 * math.pi) for i in self._netPolarizationEnergy ]	
	self._netPolarizationEnergy= [i % 2 for i in self._netPolarizationEnergy ]
	print DEFAULT_PREFIX + "Total Phase in the unit of 2*pi[2pi modulo]:\n           "+str(self._netPolarizationEnergy)+"\n"
	self._calculationValues['Total Phase - Units of 2*pi in the domain [0 to 2pi]'] = self._netPolarizationEnergy

	#polrization in 2pi modulo

	self._netPolarizationEnergy1=self._netPolarizationEnergy
	calcValues = self.calculationValues()
        latticeConstants = calcValues['Lattice Constants in bohr']

        ELEC_BY_VOL_CONST = self.ELEC_BY_VOL_CONST
        self._netPolarizationEnergy1 = [ELEC_BY_VOL_CONST * bohrToMeters(i[0]) * i[1] for i in zip(latticeConstants, self._netPolarizationEnergy1) ]
	print DEFAULT_PREFIX + "Total Polarization in C/m^2 [2pi modulo]:\n           "+str(self._netPolarizationEnergy1)+"\n"
	self._calculationValues['Total Polarization in  C/m^2 in the domain[0 to 2pi]'] = self._netPolarizationEnergy1

	#Correcting the phase domain between -pi and pi

	self._netPolarizationEnergy = [ self.correctPhaseDomain(i) for i in self._netPolarizationEnergy ]
	print DEFAULT_PREFIX + "Total Phase Remapped in the unit of 2*pi [-pi to +pi]:\n           "+str(self._netPolarizationEnergy)+"\n"
	self._calculationValues['Total Phase in units of 2*pi in the domain[-pi to +pi]'] = self._netPolarizationEnergy

	#grab the calculation values
	calcValues = self.calculationValues()
	latticeConstants = calcValues['Lattice Constants in bohr']
	
	ELEC_BY_VOL_CONST = self.ELEC_BY_VOL_CONST
 	self._netPolarizationEnergy = [ELEC_BY_VOL_CONST * bohrToMeters(i[0]) * i[1] for i in zip(latticeConstants, self._netPolarizationEnergy) ]

        print DEFAULT_PREFIX + "Total Polarization in C/m^2[-pi to +pi]:\n           "+str(self._netPolarizationEnergy)+"\n"
	self._calculationValues['Total Polarization in C/m^2 in the domain[-pi to +pi]'] = self._netPolarizationEnergy
        return self._netPolarizationEnergy

    def netPolarizationEnergy(self):
        return self._netPolarizationEnergy

# local functions
def bohrToMeters(value, dimension = 1):
    return value * ((BOHR_CONSTANT )) ** dimension

        
if __name__ == "__main__":

    mainCalculation = MainCalculationContainer(
        file_pathphase_x = './tests/testStruct-x.pathphase',
        file_pathphase_y = './tests/testStruct-x.pathphase',
        file_pathphase_z = './tests/testStruct-x.pathphase',
        file_struct = './tests/testStruct.struct',
        file_scf = './tests/testStruct.scf',
        file_outputd = './tests/testStruct.outputd',
        file_outputst = './tests/testStruct.outputst',
        )
    mainCalculation.prettyPrintCalculationValues()
    print mainCalculation.electronPolarization()
    print mainCalculation.ionPolarization()
    print mainCalculation()
    blochBandCalculation = CalculateNumberOfBands('./tests/testStruct.scf')
