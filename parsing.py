'''
This module will include all of the required parsing for each
individiual file type that plays a role in how the entire process runs

going to try and write the code such that it can be easy to understand
and easily changed for later use
'''

from __future__ import print_function # Python 2 & 3 compatible print function
import os.path, os, pprint
import re
import numpy as np

from errorCheck import ParseError

class AbstractParser(dict):
    '''
    basic parsing methods to provide a basis for each parser class to
    derive from.
    '''
    def __init__(self, text, **options):
        dict.__init__(self, {})
        self.mainText = text

    def __call__(self):
        return self.parse()

    def __getattr__(self, name):
        """Maps values to attributes.
        Only called if there *isn't* an attribute with this name
        """
        try:
            return self.__getitem__(name)
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self.__dict__[name] = value
                
    def prettyPrint(self):
        pprint.pprint(self)
        
    def getDictionaryKeysString(self, dictionary=None, prefix=None):
        if dictionary is None:
            dictionary = self
        if prefix is None:
            prefix = '-'
        string = ''
        for key in dictionary.keys():
            string += prefix + ' ' + str(key) + '\n'
            if type(dictionary[key]) == type({}):
                string += self.getDictionaryKeysString(dictionary[key], prefix=prefix+'-')
        return string
            

    def parse(self):
        '''
        main parser function to implement in each parser
        '''
        print('parsing stuff')

    def getFilename(self):
        return self.filename

    def getFileContent(self):
        return self.mainText

    def textToList(self):
        theList = []
        for line in self.getFileContent():
            spacedList = [ i for i in line.strip().split(' ') if not i == '']
            theList.append(spacedList)
        return theList


class MainStructParser(AbstractParser):
# Parse case.struct file and extract the following info:
# - lattice type
# - number of atoms
# - atomic positions
# - multiplicity of atoms
# - element name
# - nuclear charge
# - cell volume
# - real and reciprocal lattice vectors
    def parse(self):
        def lattVec(lattic,aa,bb,cc,alphadeg):
            # calculate real and reciprocal lattice vectors; cell volume
            # lattic - lattice type
            # aa,bb,cc - lattice parameters
            # alpha[0:2] - lattice angles
            # NOTE: calculations are based on WIEN2k_19.2/SRC_dstart/module.F
            #       SUBROUTINE latgen_struct
            sqrt3=np.sqrt(3)
            test=1e-5 # small
            # convert deg -> rad
            alpha = np.zeros(3) # allocate
            alpha[0] = alphadeg[0]*np.pi/180
            alpha[1] = alphadeg[1]*np.pi/180
            alpha[2] = alphadeg[2]*np.pi/180
            pia = np.zeros(3) # allocate
            pia[0] = 2*np.pi/aa
            pia[1] = 2*np.pi/bb
            pia[2] = 2*np.pi/cc
            cosab = np.cos(alpha[2])
            cosac = np.cos(alpha[1])
            cosbc = np.cos(alpha[0])
            sinab = np.sin(alpha[2])
            sinbc = np.sin(alpha[0])
            # allocate reciprocal lattice vectors
            br1_rec = np.zeros((3,3))
            br2_rec = np.zeros((3,3))
            # select proper lattice type
            if lattic == "H": # hexagonal lattice
                br1_rec[0,0] = 2/sqrt3*pia[0]
                br1_rec[0,1] = 1/sqrt3*pia[0]
                br1_rec[1,1] = pia[1]
                br1_rec[2,2] = pia[2]
                br2_rec = br1_rec
                rvfac = 2/sqrt3
                ortho = False
            elif lattic == "S" or lattic == "P": # primitive lattice
                wurzel = np.sqrt(sinbc**2-cosac**2-cosab**2+2*cosbc*cosac*cosab)
                br1_rec[0,0] = sinbc/wurzel*pia[0]
                br1_rec[0,1] = (-cosab+cosbc*cosac)/(sinbc*wurzel)*pia[1]
                br1_rec[0,2] = (cosbc*cosab-cosac)/(sinbc*wurzel)*pia[2]
                br1_rec[1,1] = pia[1]/sinbc
                br1_rec[1,2] = -pia[2]*cosbc/sinbc
                br1_rec[2,2] = pia[2]
                br2_rec = br1_rec
                rvfac = 1/wurzel
                ortho = True
                if abs(alpha[0]-np.pi/2) > test:
                    ortho= False
                if abs(alpha[1]-np.pi/2) > test:
                    ortho= False
                if abs(alpha[2]-np.pi/2) > test:
                    ortho= False
            elif lattic == "F": # FCC lattice
                br1_rec[0,0] = pia[0]
                br1_rec[1,1] = pia[1]
                br1_rec[2,2] = pia[2]
                # definitions according to column, rows convention for br2_rec
                br2_rec[0,0] = -pia[0]
                br2_rec[0,1] = pia[0]
                br2_rec[0,2] = pia[0]
                br2_rec[1,0] = pia[1]
                br2_rec[1,1] = -pia[1]
                br2_rec[1,2] = pia[1]
                br2_rec[2,0] = pia[2]
                br2_rec[2,1] = pia[2]
                br2_rec[2,2] = -pia[2]
                rvfac = 4
                ortho = True
            elif lattic == "B": # BCC lattice
                br1_rec[0,0] = pia[0]
                br1_rec[1,1] = pia[1]
                br1_rec[2,2] = pia[2]
                br2_rec[0,0] = 0
                br2_rec[0,1] = pia[0]
                br2_rec[0,2] = pia[0]
                br2_rec[1,0] = pia[1]
                br2_rec[1,1] = 0
                br2_rec[1,2] = pia[1]
                br2_rec[2,0] = pia[2]
                br2_rec[2,1] = pia[2]
                br2_rec[2,2] = 0
                rvfac = 2
                ortho = True
            elif lattic == "CXY": # C-base-centered (orthorhombic only)
                br1_rec[0,0] = pia[0]
                br1_rec[1,1] = pia[1]
                br1_rec[2,2] = pia[2]
                br2_rec[0,0] = pia[0]
                br2_rec[0,1] = pia[0]
                br2_rec[0,2] = 0
                br2_rec[1,0] =-pia[1]
                br2_rec[1,1] = pia[1]
                br2_rec[1,2] = 0
                br2_rec[2,0] = 0
                br2_rec[2,1] = 0
                br2_rec[2,2] = pia[2]
                rvfac = 2
                ortho= True
            elif lattic == "CXZ": # B-base-centered (orthorh. and monoclinic
                                  # symmetry)
                if abs(alpha[2]-np.pi/2) < 0:
                    br1_rec[0,0]=pia[0]
                    br1_rec[1,1]=pia[1]
                    br1_rec[2,2]=pia[2]
                    br2_rec[0,0]= pia[0]
                    br2_rec[0,1]= 0
                    br2_rec[0,2]= pia[0]
                    br2_rec[1,0]= 0
                    br2_rec[1,1]= pia[1]
                    br2_rec[1,2]= 0
                    br2_rec[2,0]=-pia[2]
                    br2_rec[2,1]= 0
                    br2_rec[2,2]= pia[2]
                    rvfac=2
                    ortho=True
                else:
                    print("  gamma not equal 90") # CXZ monoclinic case
                    br1_rec[0,0]= pia[0]/sinab
                    br1_rec[0,1]= -pia[1]*cosab/sinab
                    br1_rec[1,1]= pia[1]
                    br1_rec[2,2]= pia[2]
                    br2_rec[0,0]= pia[0]/sinab
                    br2_rec[0,1]= -pia[1]*cosab/sinab
                    br2_rec[0,2]= pia[0]/sinab
                    br2_rec[1,0]= 0
                    br2_rec[1,1]= pia[1]
                    br2_rec[1,2]= 0
                    br2_rec[2,0]=-pia[2]
                    br2_rec[2,1]= 0
                    br2_rec[2,2]= pia[2]
                    rvfac=2.0/sinab
                    ortho=False
            elif lattic == "CYZ": # A-base-centered (orthorhombic only)
                br1_rec[0,0]=pia[0]
                br1_rec[1,1]=pia[1]
                br1_rec[2,2]=pia[2]
                br2_rec[0,0]= pia[0]
                br2_rec[0,1]= 0
                br2_rec[0,2]= 0
                br2_rec[1,0]= 0
                br2_rec[1,1]= pia[1]
                br2_rec[1,2]= pia[1]
                br2_rec[2,0]= 0
                br2_rec[2,1]=-pia[2]
                br2_rec[2,2]= pia[2]
                rvfac=2
                ortho=True
            elif lattic == "R": # rhombohedral
                br1_rec[0,0]=1/sqrt3*pia[0]
                br1_rec[0,1]=1/sqrt3*pia[0]
                br1_rec[0,2]=-2/sqrt3*pia[0]
                br1_rec[1,0]=-1*pia[1]
                br1_rec[1,1]=1*pia[1]
                br1_rec[1,2]=0
                br1_rec[2,0]=pia[2]
                br1_rec[2,1]=pia[2]
                br1_rec[2,2]=pia[2]
                br2_rec=br1_rec
                rvfac=6/sqrt3
                ortho=False
            else: # error
                raise Exception("Lattice type is not known")
            # cell volume
            vol=aa*bb*cc/rvfac
            # real space lattice vectors from reciprocal once by matrix invers.
            br1_dir = np.linalg.inv(br1_rec)
            br2_dir = np.linalg.inv(br2_rec)
            det = 0
            for i in range(0, 2):
                det = det + br1_dir[i,0]*br1_rec[i,0]
            br1_dir = br1_dir*2*np.pi/det
            det = 0
            for i in range(0, 2):
                det = det + br2_dir[i,0]*br2_rec[i,0]
            br2_dir = br2_dir*2*np.pi/det
            # return function output lattice vectors and cell volume
            return (br1_dir,br2_dir,br1_rec,br2_rec,vol)
            # END lattVec
        print("Reading case.struct file")
        theText = self.getFileContent()
        #split up file into individual atom listings
        atomLineIndex = []
        atomLineNumber = []
        # go through case.struct file line-by-line
        for num, line in enumerate(theText):
            if num == 1: # 2nd line case.struct file
                # read lattice type and number of atoms using FORMAT(A4,23X,I3)
                lattic = line[0:4]
                lattic = lattic.strip() # rm white spaces
                nat = int(line[28:30])
                print("  Lattice type:", lattic)
                print("  Number of inequivalent atoms:", nat)
            if num == 3: # 4th line case.struct file
                # read lattice parameters using FORMAT(6F10.7)
                aa = float(line[0:10])
                bb = float(line[11:20])
                cc = float(line[21:30])
                alpha = np.zeros(3)
                alpha[0] = float(line[31:40])
                alpha[1] = float(line[41:50])
                alpha[2] = float(line[51:60])
                print(" "*1, "a =", aa, "bohr")
                print(" "*1, "b =", bb, "bohr")
                print(" "*1, "c =", cc, "bohr")
                print(" "*1, "alpha =", alpha[0], "deg")
                print(" "*1, "beta  =", alpha[1], "deg")
                print(" "*1, "gamma =", alpha[2], "deg")
                # determine real and reciprocal lattice vectors based on 
                # the lattice type and lattice parameters
                (br1_dir,br2_dir,br1_rec,br2_rec,vol) = \
                    lattVec(lattic,aa,bb,cc,alpha)
                self['cell volume'] = vol
                self['lattice constants'] = [aa,bb,cc]
                self['real space lattice vectors'] = br2_dir
                self['reciprocal lattice vectors'] = br2_rec
                print(" "*1, "Reciprocal lattice vectors br1_rec (rad/bohr):")
                print(" "*3, br1_rec[0,:])
                print(" "*3, br1_rec[1,:])
                print(" "*3, br1_rec[2,:])
                print(" "*1, "Reciprocal lattice vectors br2_rec (rad/bohr):")
                print(" "*3, br2_rec[0,:])
                print(" "*3, br2_rec[1,:])
                print(" "*3, br2_rec[2,:])
                print(" "*1, "Real space lattice vectors br1_dir (bohr):")
                print(" "*3, br1_dir[0,:])
                print(" "*3, br1_dir[1,:])
                print(" "*3, br1_dir[2,:])
                print(" "*1, "Real space lattice vectors br2_dir (bohr):")
                print(" "*3, br2_dir[0,:])
                print(" "*3, br2_dir[1,:])
                print(" "*3, br2_dir[2,:])
                print(" "*1, "Unit cell volume:", vol, "bohr3")
            # find ATOM line
            re_atomListing = re.compile(r'ATOM *(?P<atomNumber>-?[0-9]+):')
            atomListingMatch = re_atomListing.search(line)
            if atomListingMatch:
                atomLineIndex.append(num)
                atomLineNumber.append(atomListingMatch.group('atomNumber'))
            if 'NUMBER OF SYMMETRY OPERATIONS' in line:
                indexSymmetryEnding = num
        # check the number of ATOM instances matches 
        # "nat" in the 2nd line of case.struct
        if len(atomLineIndex) != nat:
            print("Number of ATOM instances in case.struct:", len(atomLineIndex))
            print("Number of atoms in 2nd line case.struct:", nat)
            raise Exception("The number of ATOM instances does not matche "+\
                "the number of atoms in case.struct")
        atomListing = []
        for startSlice, endSlice in zip(atomLineIndex[:-1], atomLineIndex[1:]):
            atomListing.append(theText[startSlice:endSlice])
        else:
            atomListing.append(theText[atomLineIndex[-1]:indexSymmetryEnding])

        ###########################
        #make sure our MULT atom listings are included with the previous division
        ############################
        while True:
            for num, atomNumber in enumerate(atomLineNumber[:-1]):
                if atomNumber == atomLineNumber[num+1]:
                    atomListing[num] += atomListing[num+1]
                    atomLineNumber.remove(atomLineNumber[num+1])
                    atomListing.remove(atomListing[num+1])
                    break
            else:
                break

        #parse each individual atom into a list
        self['Atom Listing'] = []
        re_coordinates = re.compile(r'X= ?(?P<xCoordinate>[0-9.]+) +Y= ?(?P<yCoordinate>[0-9.]+) +Z= ?(?P<zCoordinate>[0-9.]+)')
        re_mult = re.compile(r'MULT= *(?P<multValue>[0-9]+)')
        re_element = re.compile(r'(?P<elementName>[A-Z][a-z]{0,2}) ?(?P<elementNumber>[0-9]*) +NPT')
        re_zatom = re.compile(r'.*RMT=.*Z:\s*(?P<Znucl>[0-9.]+)') 
        for atom in atomListing:
            theAtom = {}
            for line in atom:
                #find coordinates on line
                coordinateMatches = re_coordinates.search(line)
                if coordinateMatches:
                    #check to see if the coordinate keys and exist
                    #and create them if necessary
                    if 'X-Coord' not in theAtom:
                        theAtom['X-Coord'] = []
                    if 'Y-Coord' not in theAtom:
                        theAtom['Y-Coord'] = []
                    if 'Z-Coord' not in theAtom:
                        theAtom['Z-Coord'] = []
                    
                    theCoordinates = coordinateMatches.groups()

                    theAtom['X-Coord'].append(float(theCoordinates[0]))
                    theAtom['Y-Coord'].append(float(theCoordinates[1]))
                    theAtom['Z-Coord'].append(float(theCoordinates[2]))
                #determine if MULT value on line
                multMatches = re_mult.search(line)
                if multMatches:
                    theAtom['MULT'] = int(multMatches.group('multValue'))

                elementMatches = re_element.search(line)
                if elementMatches:
                    theAtom['Element Name'] = elementMatches.group('elementName')
                    if elementMatches.group('elementNumber'):
                        theAtom['Element Number'] = int(elementMatches.group('elementNumber'))
                    else:
                        theAtom['Element Number'] = 1

                zatomMatches = re_zatom.search(line)
                if zatomMatches:
                    theAtom['Znucl'] = float(zatomMatches.group('Znucl'))
            #issue -- if it contains no values, it doesn't return an exception
            if theAtom:
                #before appending, check to see if it has all of the required values
                MissingTags = checkForTags(theAtom, [
                                                'X-Coord', 'Y-Coord', 'Z-Coord',
                                                'MULT',
                                                'Element Name',
                                                'Element Number',
                                                'Znucl',
                                                ])
                
                if MissingTags:
                    print("Error in: " + str(theAtom))
                    raise ParseError('ERROR: Missing data in atom', MissingTags)

                #append to the atom listing
                self['Atom Listing'].append(theAtom)


class MainIncParser(AbstractParser):
# Parse case.inc file and extract the following info:
# - number of core electrons per non-equivalent atom type
    def parse(self):
        print("Reading case.inc file")
        theText = self.getFileContent()
        nlines = len(theText) # number of lines in the file
        fileEnd = False
        iline = 0 # 1st line
        coreCharges = [] # list of core charge for each atom in case.inc
        while not fileEnd:
            line = theText[iline]
            line = line.split()
            nrorb = line[0] # number of core orbitals
            nrorb = int(nrorb)
            Zcore = 0
            for i in range(iline+1, iline+nrorb+1):
                line = theText[i] # "1,-1,2               ( N,KAPPA,OCCUP)"
                line = line.split(",") # split line at commas
                line = line[2] # get "2               ( N"
                line = line.split() # split line at apsces
                occup = line[0]
                occup = int(occup)
                Zcore = Zcore + occup
            coreCharges.append(Zcore) # append the list with core charge
            iline = iline+nrorb+1 # next block of data starts at this line
            line = theText[iline]
            if line.strip() == "0" or iline >= nlines-1: # end of file?
                fileEnd = True
                break # exit while loop
        print(" "*1, "Core charge for individual non-equivalent atoms:", coreCharges)
        if len(coreCharges) == 0: # for some reason unable to find any atoms
            raise Exception("Error reading case.inc file. "+ \
                "For some reason unable to find any atoms.")
        self['core charges'] = coreCharges # pass data to the main code
# END MainIncParser


# Modified by OR (Sat 09 Nov 2013 06:37:11 PM CST)
# it is restricted to determining the band range and cell volume only
class MainSCFParser(AbstractParser):

    def parse(self):
        tempText = self.getFileContent()

        tagList = [
            re.compile(r':BAN[0-9]+'),
            re.compile(r':VOL'),
        ]
        #strip out all of the iterations, volume and band lines
        theText = []
        for line in tempText:
            for tag in tagList:
                if tag.search(line):
                    theText.append(line)

        # determine occupied bands
        re_bandListing = re.compile(r':BAN[0-9]+: +(?P<bandNum>[0-9]+) +[0-9.-]+ +[0-9.-]+ +(?P<occupancy>[0-9.]+)')
        self['Band List'] = []
        for line in theText:
            #band listings
            result_bandListing = re_bandListing.search(line)
            if result_bandListing:
                theDict = {
                    'band range' : int(result_bandListing.group('bandNum')),
                    'occupancy' : int(float(result_bandListing.group('occupancy'))),
                    }
                self['Band List'].append(theDict)
        # if have nothing within the band list
        if not self['Band List']:
            raise ParseError('ERROR: Missing band list in SCF* file', ())
# END MainSCFParser (Sat 09 Nov 2013 06:36:44 PM CST)


class MainPathphaseParser(AbstractParser):
    def parse(self):
        theList = self.textToList()
        self['size'] = int(theList[0][0])
        self['direction'] = [ float(i) for i in theList[1] ]
        del theList[:2]
        berryPhaseValues = [ float(i[1]) for i in theList ]
        self['values'] = berryPhaseValues


#local functions
def checkForTags(theDict, theTags):
    '''
    checks the provided dictionary and compares it to the given tag
    values. Returns a tuple with the list of missing tags, or an empty
    tuple
    '''
    theKeys = theDict.keys()
    for aKey in theKeys:
        if aKey in theTags:
            theTags.remove(aKey)
    return tuple(theTags)

if __name__ == "__main__":
    print(".struct file")
    textString = open('./tests/testStruct.struct', 'r').readlines()
    testStruct2 = MainStructParser(textString)
    testStruct2.parse()
    print(testStruct2.getDictionaryKeysString())

    print(".inc file")
    textString = open('./tests/testStruct.inc', 'r').readlines()
    testStruct = MainIncParser(textString)
    testStruct.parse()
    print(testStruct.getDictionaryKeysString())

    print(".scf2 file")
    textString = open('./tests/testStruct.scf2', 'r').readlines()
    testStruct = MainSCFParser(textString)
    testStruct.parse()
    print(testStruct.getDictionaryKeysString())

    print(".pathphase file")
    textString = open('/home/stud2/BaTiO3-berry/BaTiO3-tetra/experimentalBaTiO3/BaTiO3newwien2k/BaTiO3min/BaTiO3min-x.pathphase', 'r').readlines()
    testStruct = MainPathphaseParser(textString)
    testStruct.parse()
    print(testStruct.getDictionaryKeysString())

    
