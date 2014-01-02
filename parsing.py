'''
This module will include all of the required parsing for each
individiual file type that plays a role in how the entire process runs

going to try and write the code such that it can be easy to understand
and easily changed for later use
'''

import os.path, os, pprint
import re

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
        print 'parsing stuff'

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
    def parse(self):
        theText = self.getFileContent()
        #split up file into individual atom listings
        atomLineIndex = []
	atomLineNumber = []
        #fix for ATOM being used with MULT > 1
        re_atomListing = re.compile(r'ATOM +(?P<atomNumber>-?[0-9]+):')
        for num, line in enumerate(theText):
            atomListingMatch = re_atomListing.search(line)
            if atomListingMatch:
                atomLineIndex.append(num)
                atomLineNumber.append(atomListingMatch.group('atomNumber'))
            if 'NUMBER OF SYMMETRY OPERATIONS' in line:
                indexSymmetryEnding = num
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

        ############################
        #######################

        #parse each individual atom into a list
        self['Atom Listing'] = []
        re_coordinates = re.compile(r'X= ?(?P<xCoordinate>[0-9.]+) +Y= ?(?P<yCoordinate>[0-9.]+) +Z= ?(?P<zCoordinate>[0-9.]+)')
        re_mult = re.compile(r'MULT= *(?P<multValue>[0-9]+)')
        re_element = re.compile(r'(?P<elementName>[A-Z][a-z]{0,2}) ?(?P<elementNumber>[0-9]*) +NPT')
        for atom in atomListing:
            theAtom = {}
            for line in atom:
                #find coordinates on line
                coordinateMatches = re_coordinates.search(line)
                if coordinateMatches:
                    #check to see if the coordinate keys and exist
                    #and create them if necessary
                    if not theAtom.has_key('X-Coord'):
                        theAtom['X-Coord'] = []
                    if not theAtom.has_key('Y-Coord'):
                        theAtom['Y-Coord'] = []
                    if not theAtom.has_key('Z-Coord'):
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

            #issue -- if it contains no values, it doesn't return an exception
            if theAtom:
                #before appending, check to see if it has all of the required values
                MissingTags = checkForTags(theAtom, [
                                                'X-Coord', 'Y-Coord', 'Z-Coord',
                                                'MULT',
                                                'Element Name',
                                                'Element Number',
                                                ])
                
                if MissingTags:
                    print "Error in: " + str(theAtom)
                    raise ParseError('ERROR: Missing data in atom', MissingTags)

                #append to the atom listing
                self['Atom Listing'].append(theAtom)
            

class MainOutputDParser(AbstractParser):
    def parse(self):
        theText = self.getFileContent()


        re_lattice_type = re.compile(r'LATTICE += ?(?P<latticeType>[A-Za-z]+)')
        re_lattice_constants = re.compile(r'LATTICE CONSTANTS ARE += +(?P<xLattice>[0-9.]+) +(?P<yLattice>[0-9.]+) +(?P<zLattice>[0-9.]+)')
        re_numAtoms = re.compile(r'NUMBER OF ATOMS IN UNITCELL += +(?P<numAtoms>[0-9]+)')
        BR2_matrices = []
        for num, line in enumerate(theText):
            #lattice type
            latticeTypeMatches = re_lattice_type.search(line)
            if latticeTypeMatches:
                self['Lattice Type'] = latticeTypeMatches.group('latticeType')

            #lattice constants
            latticeConstantMatches = re_lattice_constants.search(line)
            if latticeConstantMatches:
                self['Lattice Constants'] = [
                    float(latticeConstantMatches.group('xLattice')),
                    float(latticeConstantMatches.group('yLattice')),
                    float(latticeConstantMatches.group('zLattice'))
                    ]

            #grabbing BR2_DIR and slicing out text for matrix
            if 'BR2_DIR' in line:
                BR2_matrices = theText[num+1:num+4]

            #num atoms in unit cell
            numAtomsMatches = re_numAtoms.search(line)
            if numAtomsMatches:
                self['Number of Atoms in Unit Cell'] = int(numAtomsMatches.group('numAtoms'))
            
        #clean up BR2_matrices
        BR2_matrices = [ [float(i.strip().strip('\n')) for i in line.split()]
                         for line in BR2_matrices ]
        self['BR2_DIR Matrix'] = BR2_matrices

        #exception handling
        MissingTags = checkForTags(self, [
            'Lattice Type',
            'Lattice Constants',
            'BR2_DIR Matrix',
            'Number of Atoms in Unit Cell',
            ])
        if MissingTags:
            raise ParseError("ERROR: Missing data in *.outputd file", MissingTags)


# THIS IS THE ORIGINAL CLASS (Sat 09 Nov 2013 06:27:43 PM CST)
#class MainSCFParser(AbstractParser):
#    def parse(self):
#        tempText = self.getFileContent()
#
#        tagList = [
#            re.compile(r':BAN[0-9]+'),
#            re.compile(r':VOL'),
#            re.compile(r':ITE(?P<num>[0-9]+)'),
#        ]
#        #strip out all of the iterations, volume and band lines
#        theText = []
#        for line in tempText:
#            for tag in tagList:
#                if tag.search(line):
#                    theText.append(line)
#
#        #grab the last iteration
#        theIterationIndex, theIterationNumber = 0,0
#        for number, line in enumerate(theText):
#            result_theIterationNum = tagList[2].search(line) #ITE regex
#            if result_theIterationNum:
#                theIterationNumber = int(result_theIterationNum.group('num'))
#                theIterationIndex = number
#                #i'm assuming the last one it finds is the last iteration
#
#        #delete up to the last iteration
#        theText = theText[theIterationIndex:]
#
#        re_volumeSize = re.compile(r':VOL +: +UNIT CELL VOLUME = +(?P<cellVolume>[0-9.]+)')
#        re_bandListing = re.compile(r':BAN[0-9]+: +(?P<bandNum>[0-9]+) +[0-9.-]+ +[0-9.-]+ +(?P<occupancy>[0-9.]+)')
#
#        self['Band List'] = []
#        for line in theText:
#            #volume
#            result_volumeSize = re_volumeSize.search(line)
#            if result_volumeSize:
#                self['Cell Volume'] = float(result_volumeSize.group('cellVolume'))

#            #band listings
#            result_bandListing = re_bandListing.search(line)
#            if result_bandListing:
#                theDict = {
#                    'band range' : int(result_bandListing.group('bandNum')),
#                    'occupancy' : int(float(result_bandListing.group('occupancy'))),
#                    }
#                self['Band List'].append(theDict)
#        MissingTags = checkForTags(self, [
#            'Cell Volume',
#            ])
#        # if missing any tags, or have nothing within the band list
#        if MissingTags:
#            raise ParseError("ERROR: Missing data in *.scf file", MissingTags)
#        if not self['Band List']:
#            raise ParseError('ERROR: Missing band list in *.scf file', ())

#class MainSCFParser(AbstractParser):
#    def parse(self):
#        tempText = self.getFileContent()
#
#        tagList = [
#            re.compile(r':BAN[0-9]+'),
#            re.compile(r':VOL'),
#            re.compile(r':ITE(?P<num>[0-9]+)'),
#        ]
#        #strip out all of the iterations, volume and band lines
#        theText = []
#        for line in tempText:
#            for tag in tagList:
#                if tag.search(line):
#                    theText.append(line)
#
#        #grab the last iteration
#        theIterationIndex, theIterationNumber = 0,0
#        for number, line in enumerate(theText):
#            result_theIterationNum = tagList[2].search(line) #ITE regex
#            if result_theIterationNum:
#                theIterationNumber = int(result_theIterationNum.group('num'))
#                theIterationIndex = number
#                #i'm assuming the last one it finds is the last iteration
#
#        #delete up to the last iteration
#        theText = theText[theIterationIndex:]
#
#        re_volumeSize = re.compile(r':VOL +: +UNIT CELL VOLUME = +(?P<cellVolume>[0-9.]+)')
#        re_bandListing = re.compile(r':BAN[0-9]+: +(?P<bandNum>[0-9]+) +[0-9.-]+ +[0-9.-]+ +(?P<occupancy>[0-9.]+)')
#
#        self['Band List'] = []
#        for line in theText:
#            #volume
#            result_volumeSize = re_volumeSize.search(line)
#            if result_volumeSize:
#                self['Cell Volume'] = float(result_volumeSize.group('cellVolume'))

#            #band listings
#            result_bandListing = re_bandListing.search(line)
#            if result_bandListing:
#                theDict = {
#                    'band range' : int(result_bandListing.group('bandNum')),
#                    'occupancy' : int(float(result_bandListing.group('occupancy'))),
#                    }
#                self['Band List'].append(theDict)
#        MissingTags = checkForTags(self, [
#            'Cell Volume',
#            ])
#        # if missing any tags, or have nothing within the band list
#        if MissingTags:
#            raise ParseError("ERROR: Missing data in *.scf file", MissingTags)
#        if not self['Band List']:
#            raise ParseError('ERROR: Missing band list in *.scf file', ())
      

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

        # determine the volume of unit cell
        re_volumeSize = re.compile(r':VOL +: +UNIT CELL VOLUME = +(?P<cellVolume>[0-9.]+)')
        self['Cell Volume'] = []
        for line in theText:
            result_volumeSize = re_volumeSize.search(line)
            if result_volumeSize:
                self['Cell Volume'] = float(result_volumeSize.group('cellVolume'))
                # Last value :VOL in *scf will be stored and used in
                # calculations. No check for empty volume here,
                # since *.scf2 file does not contain volume info

# END MainSCFParser (Sat 09 Nov 2013 06:36:44 PM CST)


class MainOutputstParser(AbstractParser):
    def parse(self):
        theList = self.textToList()
        theMainString = self.getFileContent()

        #get specific parts of given file based on regular expressions
        regexTagsCompileList = [
            re.compile(r' +[A-Za-z]+ +RHFS'),
            re.compile(r' *TOTAL CHARGE FOR SPIN +[12] : +[0-9.]+'),
            re.compile(r' *TOTAL CORE-CHARGE: +[0-9.]+'),
            ]
        theMainString = [ i for i in theMainString for j in regexTagsCompileList if j.match(i) ]
        
        #remove repeating lines
        theMainStringTemp = []
        for element in theMainString:
            if re.match(r' +[A-Za-z]+ +RHFS',element) and element in theMainStringTemp:
                continue
            theMainStringTemp.append(element)
        theMainString = theMainStringTemp
        self['Element List'] = {}
        #some regular expression magic
        re_mainElementParse = re.compile(r'\s*(?P<elementName>[A-Za-z]+)\s+RHFS\s+')
        re_chargePerSpinOne = re.compile(
            r'^ TOTAL CHARGE FOR SPIN +1 : +(?P<spinValueOne>[0-9.]+ +$)')
        re_chargePerSpinTwo = re.compile(
            r'^ TOTAL CHARGE FOR SPIN +2 : +(?P<spinValueTwo>[0-9.]+ +$)')
        re_coreValue = re.compile(
            r'^ TOTAL CORE-CHARGE: +(?P<coreValue>[0-9.]+)')

        #begin iterating over each line finding the regex
        elementName = None
        for line in theMainString:
            result_elementName = re_mainElementParse.search(line)

            #When the element name is found, we append our dictionary,
            #assuming we have retrieved sufficient data for the
            #previous element. From there, we start a new element
            #dictionary.
            if result_elementName:
                if elementName:
                     self['Element List'][elementName] = elementDict
                elementName = result_elementName.group('elementName')
                elementDict = {}

            #find the first TOTAL CHARGE FOR SPIN:
            result_valueOne = re_chargePerSpinOne.search(line)
            if result_valueOne:
                valueOne = result_valueOne.group('spinValueOne')
                elementDict['Spin Value 1'] = float(valueOne.strip())

            #find the second TOTAL CHARGE FOR SPIN
            result_valueTwo = re_chargePerSpinTwo.search(line)
            if result_valueTwo:
                valueTwo = result_valueTwo.group('spinValueTwo')
                elementDict['Spin Value 2'] = float(valueTwo.strip())

            result_coreValue = re_coreValue.search(line)
            if result_coreValue:
                theCoreValue = result_coreValue.group('coreValue')
                elementDict['Core Value'] = float(theCoreValue.strip())

        #for the final element, we append outside of the for loop
        self['Element List'][elementName] = elementDict
        
        #exception handling
        #make sure all of the required values were found
        for atom in self['Element List']:
            missingTags = checkForTags(elementDict, [
                'Spin Value 1',
                'Spin Value 2',
                'Core Value',
                ])
            if missingTags:
                raise ParseError("ERROR: Missing data in *.outputst file", missingTags)
        
        

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
    print ".struct file"
    textString = open('./tests/testStruct.struct', 'r').readlines()
    testStruct2 = MainStructParser(textString)
    testStruct2.parse()
    print testStruct2.getDictionaryKeysString()

    print ".outputd file"
    textString = open('./tests/testStruct.outputd', 'r').readlines()
    testStruct = MainOutputDParser(textString)
    testStruct.parse()
    print testStruct.getDictionaryKeysString()

    print ".scf file"
    textString = open('./tests/testStruct.scf', 'r').readlines()
    testStruct = MainSCFParser(textString)
    testStruct.parse()
    print testStruct.getDictionaryKeysString()

    print ".outputst file"
    textString = open('./tests/testStruct.outputst', 'r').readlines()
    testStruct = MainOutputstParser(textString)
    testStruct.parse()
    print testStruct.getDictionaryKeysString()
    print testStruct.prettyPrint()

    print ".pathphase file"
    textString = open('/home/stud2/BaTiO3-berry/BaTiO3-tetra/experimentalBaTiO3/BaTiO3newwien2k/BaTiO3min/BaTiO3min-x.pathphase', 'r').readlines()
    testStruct = MainPathphaseParser(textString)
    testStruct.parse()
    print testStruct.getDictionaryKeysString()

    
