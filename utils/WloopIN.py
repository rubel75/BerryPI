#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 17:11:01 2021

@author: enigma

It makes a Wloop.in the input file for WloopPHI code
"""
import numpy as np
import matplotlib.pyplot as plt

def WloopIN_Z(X1, X2, S, E):
    Data = np.append(X1, X2, axis=1)
    row, col = Data.shape
    ab = np.ones(row)
    ab.shape = 1, row
    Data = np.insert(Data, 2, S * ab, axis=1)
    Data = np.insert(Data, 3, X1.T, axis=1)
    Data = np.insert(Data, 4, X2.T, axis=1)
    Data = np.insert(Data, 5, E * ab, axis=1)

    return Data

def WloopIN_X(X1, X2, S, E):
    Data = np.append(X1, X2, axis=1)
    row, col = Data.shape
    ab = np.ones(row)
    ab.shape = 1, row
    Data = np.insert(Data, 0, S * ab, axis=1)
    Data = np.insert(Data, 3, E * ab, axis=1)
    Data = np.insert(Data, 4, X1.T, axis=1)
    Data = np.insert(Data, 5, X2.T, axis=1)

    return Data

def WloopIN_Y(X1, X2, S, E):
    Data = np.append(X1, X2, axis=1)
    row, col = Data.shape
    ab = np.ones(row)
    ab.shape = 1, row
    Data = np.insert(Data, 1, S * ab, axis=1)
    Data = np.insert(Data, 3, X1.T, axis=1)
    Data = np.insert(Data, 4, E * ab, axis=1)
    Data = np.insert(Data, 5, X2.T, axis=1)

    return Data

# Enter the precise location of Weyl point (x, y, z).
cx, cy, cz = 0, 0, 0
# Enter the radius of a loop
r = 0.01
# Trajectory direction.
direction = str('z')
# Starting point and End point.
S, E = -0.5, 0.5
# How many vertex points for Wilson loop
n = 16
theta = np.linspace(0, 2*np.pi*(1-1/n), n)

# compute x1 and x2
X1 = r*np.cos(theta)
X2 = r*np.sin(theta)
X1.shape = X1.shape[0], 1
X2.shape = X2.shape[0], 1

if (direction == 'z'):
    X1 = X1 + cx
    X2 = X2 + cy
    Data = WloopIN_Z(X1, X2, S, E)

elif (direction == 'x'):
    X1 = X1 + cy
    X2 = X2 + cz
    Data = WloopIN_X(X1, X2, S, E)

else:
    X1 = X1 + cx
    X2 = X2 + cz
    Data = WloopIN_Y(X1, X2, S, E)

np.savetxt("WloopCoordinate.dat", Data, delimiter = " ", comments = "#", fmt = "%.5f %.5f %.5f ; %.5f %.5f %.5f")

# create the figure for Wilson loop
fig, ax = plt.subplots(figsize=(6,6), dpi=300)
#fig, ax = plt.subplots(1)
ax.plot(X1, X2)
if (direction == 'z'):
    ax.set(xlabel = 'x', ylabel = 'y', title = 'Wilson loop in %s direction' %direction)
    ax.grid()
elif (direction == 'x'):
    ax.set(xlabel = 'y', ylabel = 'z', title = 'Wilson loop in %s direction' %direction)
    ax.grid()
else:
    ax.set(xlabel = 'x', ylabel = 'z', title = 'Wilson loop in %s direction' %direction)
    ax.grid()

plt.savefig("Wloop.png")
