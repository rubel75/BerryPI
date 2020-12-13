# -*- coding: utf-8 -*-
import numpy as np

def vec2cart(v, u):
    '''
    Convert vector (v -> v') from a general coordinate systrem (u) to
    Cartesian (u')

    Parameters
    ----------
    v : real array(3x1)
        Components of a vector along general, non-orthogonal coordinate system
        given by u(0,:), u(1,:), u(2,:).
    u : real array(3x3)
        Direct cosines that define a general, non-orthogonal coordinate system
        u(0,:), u(1,:), u(2,:).

    Returns
    -------
    vecpr : real array(3x1)
        Vector in Cartisian coordinates.

    '''

    # Check input
    if len(v) != 3: # vector should be in 3D
        print("ERROR vector length =", len(v))
        print("vec =", v)
        print("expected length = 3")
        sys.exit(1)
    if len(u.shape) != 2: # [u] should be 2D array
        print("ERROR array shape =", u.shape)
        print("u =", u)
        print("expected shape = (3,3)")
        sys.exit(1)
    if u.shape[0] != 3 or u.shape[1] != 3: # [u] should be 3x3
        print("ERROR array size =", u.shape)
        print("u =", u)
        print("expected shape = (3,3)")
        sys.exit(1)

    # Set up direct cosines of Cartesian coordinate system
    upr = np.zeros((3,3))
    upr[0,:] = [1, 0, 0]
    upr[1,:] = [0, 1, 0]
    upr[2,:] = [0, 0, 1]

    # Renormalize unit vectors [u] and [u']
    for i in range(3):
        u[i,:] = u[i,:]/np.linalg.norm(u[i,:])
        upr[i,:] = upr[i,:]/np.linalg.norm(upr[i,:])

    # Vector [v] in the new coord. system
    vpr = np.zeros(v.shape)
    for i in range(3):
        vpr[i] = v[0]*np.dot(upr[i],u[0]) + v[1]*np.dot(upr[i],u[1]) + v[2]*np.dot(upr[i],u[2])

    return vpr
