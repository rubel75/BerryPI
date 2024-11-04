#!/usr/bin/env python
import os
import sys
import numpy

pathphase_filename = lambda casename : os.path.join(casename, casename + '.pathphase')

def parse_pathphase(line):
    parts = [x.strip() for x in line.split(' ') if x]

    return int(parts[0]), float(parts[1])

if __name__ == "__main__":
    
    if (len(sys.argv) != 3):
        print(f'Usage: {sys.argv[0]} case1.pathphase case2.pathphase')
        print('Computes the phase difference between case2 and case1 '
                'taking into account 2*pi wrapping.')
        raise RuntimeError(f'Number of arguments is {len(sys.argv)}, while 3 is expected.')

    phase_delta = {}

    # Open input .pathphase files
    f_unperturbed = open(sys.argv[1], 'r')
    f_perturbed = open(sys.argv[2], 'r')

    # First line tells us how many paths there are 
    n1 = int(f_unperturbed.readline().strip())
    n2 = int(f_perturbed.readline().strip())

    if n1 != n2:
        raise RuntimeError('Number of paths in pathphase files differ.')

    # Second line gives us the direction vector -- we can ignore this..
    f_unperturbed.readline()
    f_perturbed.readline()

    # Take the difference for each path 
    for i in range(n1):
        line_unperturbed = f_unperturbed.readline()
        line_perturbed = f_perturbed.readline()

        k1_u, phase_u = parse_pathphase(line_unperturbed)
        k1_p, phase_p = parse_pathphase(line_perturbed)

        if (k1_u != k1_p):
            raise RuntimeError('Order of paths is not the same between two pathphase files.')

        # Put phases on [0, 2pi)
        phase_u += 2*numpy.pi
        phase_p += 2*numpy.pi

        # Unwrap phases
        phase_u, phase_p = numpy.unwrap([phase_u, phase_p])

        # Get phase difference of unwrapped phases
        phase_delta[k1_u] = phase_p - phase_u

    print phase_delta

    # TODO print results to file

    # Close input files
    f_unperturbed.close()
    f_perturbed.close()
