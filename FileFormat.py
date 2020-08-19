#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 11:42:31 2019

@author: enigma
"""

import sys
def Message():
    print ("Error: Use proper formated file")
    print ("""Example for file format:
/home/enigma/WIEN2k/case                              # Path of your WIEN2k working directory.
51                                                    # Wilson loop Z-minimum and Z-maximum value.     
1:84                                                  # Number of division in Z direction for wilson loop.  
&WloopCoordinate                                      # Wilson loop start (it is case sensitive)
0.4565 0.2000 0.5000 ; -0.4565 0.2000 0.5000          # Starting point 1 ; End point 1
0.4565 0.3000 0.5000 ; -0.4565 0.3000 0.5000          # Starting point 2 ; End point 2          
0.4565 0.2500 1.0000 ; -0.4565 0.2500 1.0000          # Starting point 3 ; End point 3
END                                                   # End of file (It is case sensitive)""")
    sys.exit()
    
#1000                                # Multipler for WIEN2k K-Points list.