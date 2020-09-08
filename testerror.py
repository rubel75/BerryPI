'''
Test for the presence of files "*corename*.error" in the current directory.
Generate an error and exit if found a match file with non-zero file size.
'''

from __future__ import print_function # Python 2 & 3 compatible print function
import os
import sys
import glob # pathnames matching a specified pattern

def testerror(corename):
    pattern = '*'+corename+'*.error'
    for errfilename in glob.glob(pattern):
        errfilesize = os.path.getsize(errfilename)
        if errfilesize != 0:
            print("ERROR detected in", corename)
            print("Please check the error file:",errfilename)
            sys.exit(1)