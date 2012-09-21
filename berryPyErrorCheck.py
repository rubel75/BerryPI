'''
File includes useful functionality for file checking, errorhandling,
path checking, etc
'''

import os, os.path

def fileExists(filename):
    chk = os.path.exists(filename)
    return chk


class ParseError(Exception):
    def __init__(self, message, errorTags):
        Exception.__init__(self, message)

        self.errorTags = errorTags
        


if __name__ == "__main__":
    print(fileExists('./tests/testStruct.struct'))
    print(fileExists('./tests/testStruct.poop'))
