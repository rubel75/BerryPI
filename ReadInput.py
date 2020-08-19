#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 11:48:54 2019

@author: enigma
"""

import FileFormat
import numpy as np

def Values(content, WloopFileName):
    try:
        WorkingDir = str(content[0][:-1])
        KlistFileName = str("%s.klist" %(WorkingDir.split('/')[-1]))
        n = int(content[1].split()[0])
        #multiplier = int(content[2].split()[0]) # User dependent (make sure use proper array indexing)
        multiplier = 1000 # User independent
    except ValueError:
        print ("Error: Value Error")
        FileFormat.Message()
        
    K_Points = []
    wlcoordinate = 0
    with open(WloopFileName) as infile:
        copy = False
        for line in infile:
            if line.strip() == "&WloopCoordinate":
                wlcoordinate = "&WloopCoordinate"
                copy = True
                continue
            elif line.strip() == "END":
                copy = False
                continue
            elif copy:
                K_Points.append(line)
                
    StartBand = int(content[2].split(":")[0])
    EndBand = int(content[2].split(":")[1])
    S = [] # Staring Point
    E = [] # End Point
    for i in K_Points:
        temp = i.split(";")
        S.append(np.array(temp[0].split(), dtype="float"))
        E.append(np.array(temp[1].split(), dtype="float"))
        
    S = np.array(S)
    E = np.array(E)
    
        
    if(wlcoordinate == 0):
        print ("Error: ""&WloopCoordinate"" is not properly formatted. Notice it is case sensitive")
        FileFormat.Message()
        
    if (S.size == 0):
        print ("Error: Wilson loop points")
        FileFormat.Message()
        
    if (E.size == 0):
        print ("Error: Wilson loop points")
        FileFormat.Message()
        
    return (WorkingDir, KlistFileName, n, multiplier, StartBand, EndBand, S, E)
        