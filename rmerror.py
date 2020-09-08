'''
Remove error files "*corename*.error" in the current directory.
'''

from __future__ import print_function # Python 2 & 3 compatible print function
import os
import glob # pathnames matching a specified pattern

import config
from config import BERRY_DEFAULT_CONSOLE_PREFIX as DEFAULT_PREFIX

def rmerror(corename):
    pattern = '*'+corename+'*.error'
    print(DEFAULT_PREFIX, "Cleaning error files:", pattern)
    for errfilename in glob.glob(pattern):
        os.remove(errfilename)