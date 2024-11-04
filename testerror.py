'''
Test for the presence of files "*corename*.error" in the current directory.
Generate an error and exit if found a match file with non-zero file size.
'''

import os
import sys
import glob # pathnames matching a specified pattern

def testerror(corename):
    pattern = f'*{corename}*.error'
    for errfilename in glob.glob(pattern):
        errfilesize = os.path.getsize(errfilename)
        if errfilesize != 0:
            print(f'ERROR detected in {corename}')
            raise RuntimeError(f'The following error file {errfilename} '
                    'has nonzero lenth. Please check the content.')