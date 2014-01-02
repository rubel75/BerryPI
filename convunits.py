'''
File provide some usefull conversions for units, such as
[Bohr] => [m] and so on
'''

import math

# [Bohr] => [m]
def bohrToMeters(value, dimension = 1):
    BOHR_CONSTANT = 5.2917725e-11
    return value * ((BOHR_CONSTANT) ** dimension)


if __name__ == "__main__":
    print 'This program is not intended for execution'
    print 'Load it as a module instead'
    print 'import convunits'
