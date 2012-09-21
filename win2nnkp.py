#!/usr/bin/env python
import sys
from datetime import datetime
import numpy

def write_date(f):
    t = datetime.now()
    f.write('File written on ')
    f.write(t.strftime('%d%b%Y at %H:%M:%S'))
    f.write('\n\n')

def write_calc_only_A(f): # TODO
    f.write('calc_only_A  :  F\n\n')

def write_real_lattice(f, real_lattice):
    f.write('begin real_lattice\n')
    for i in range(3):
        a = real_lattice[i]
        f.write(' {0:>11.7f} {1:>11.7f} {2:>11.7f}\n'.format(*a))
    f.write('end real_lattice\n\n')

def write_recip_lattice(f, recip_lattice):
    f.write('begin recip_lattice\n')
    for i in range(3):
        a = recip_lattice[i]
        f.write(' {0:>11.7f} {1:>11.7f} {2:>11.7f}\n'.format(*a))
    f.write('end recip_lattice\n\n')

def write_kpoints(f, kpoints):
    f.write('begin kpoints\n')
    f.write('{0:>6d}\n'.format(len(kpoints)))
    for p in kpoints:
        f.write(' {0:>13.8f} {1:>13.8f} {2:>13.8f}\n'.format(*p))

    f.write('end kpoints\n\n')

def write_projections(f): # TODO
    f.write('begin projections\n')
    f.write('end projections\n\n')

def write_nnkpts(f, nnkpts):
    neighbours_per_kpoint = 3 # x, y, z

    f.write('begin nnkpts\n')
    f.write('{0:4d}\n'.format(neighbours_per_kpoint))
    for p in nnkpts:
        f.write(' {0:5d} {1:5d}    {2:3d} {3:3d} {4:3d}\n'.format(*p))
    f.write('end nnkpts\n\n')

def write_exclude_bands(f): # TODO
    f.write('begin exclude_bands\n')
    f.write('{0:4d}\n'.format(0))
    f.write('end exclude_bands\n')

# Turn `line`, a string of a `delimiter` delimited list of `T`s, into a list of `T`s.
parse_line_list = lambda line, delimiter, T : [T(y) for y in [x.strip() for x in line.strip().split(delimiter)] if y] 

def calculate_nnkpts(D):
    '''Calculates neighbours pairs for all paths. 
    '''

    # Helper functions
    product = lambda l : reduce(lambda x,y : x*y, l, 1)
    vector_add = lambda v1,v2 : [x + y for x, y in zip(v1,v2)]
    permute = lambda v,P: [v[i] for i in P]
    linear_index = lambda v,D: sum(c*i for i,c in zip(v,[product(D[:i]) for i in range(len(D))]))
    
    def wrap_vector(v,d,D):
        # Put v in bounds of D
        # Return the new v and the G vector
    
        G = [0,0,0]
        for i, j in enumerate(d):
            # Wrap i at boundaries
            if j != 0:
                if v[i] < 0 or v[i] >= D[i]:
                    v[i] = v[i] % D[i]
                    G = d
    
        return v,G
    
    # Determine the neighbours defining each path in provided direction
    P = [2, 1, 0] # Permutation for index calculation
    directions = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    nnkpts = []

    for a in range(D[0]):
        for b in range(D[1]):
            for c in range(D[2]):
                for d in directions:
                    # Build k-point and neighbour vectors
                    v = [a, b, c]
                    v_neighbour, G = wrap_vector(vector_add(v, d), d, D);
    
                    # Get indices for vectors
                    i = linear_index(permute(v, P), permute(D, P)) + 1
                    i_neighbour = linear_index(permute(v_neighbour, P), permute(D, P)) + 1
    
                    # Remember neighbours
                    nnkpts.append((i, i_neighbour, G[0], G[1], G[2]));

    return nnkpts

def parse_win_kpoints(f):
    # Find the start of the kpoints list
    while 'begin kpoints' not in f.readline():
        pass
    
    kpoints = []
    for line in f.xreadlines():
        if 'end kpoints' in line:
            break
        kpoint = tuple(parse_line_list(line, ' ', float))
        kpoints.append(kpoint)

    return kpoints

def parse_win_mp_grid(f):
    for line in f.xreadlines():
        if 'mp_grid' in line:
            # mp_grid :         A     B     C
            # Split in two by :, take second half
            return parse_line_list(line.split(':')[1], ' ', int)

def parse_win_unit_cell_cart(f):
    reciprocal = lambda a: numpy.transpose(6.28318*numpy.linalg.inv(a)) # [b1 b2 b3]^T = 2*pi*[a1 a2 a3]^-1

    real_lattice = numpy.zeros(shape=(3,3))
     
    # Find start of block
    while 'begin unit_cell_cart' not in f.readline():
        pass

    f.readline() # TODO unit line 

    # Read in 3 vectors
    for i in range(3):
        real_lattice[i] = parse_line_list(f.readline(), ' ', float)

    # Convert from Bohr to Angstrom
    real_lattice = real_lattice * 0.52917720859

    return real_lattice, reciprocal(real_lattice) 

def parse_win(case_name):
    f = open(case_name + '.win', 'r')
    real_lattice, recip_lattice = parse_win_unit_cell_cart(f)
    f.close()

    f = open(case_name + '.win', 'r')
    dimensions = parse_win_mp_grid(f)
    f.close()

    f = open(case_name + '.win', 'r')
    kpoints = parse_win_kpoints(f)
    f.close()

    return real_lattice, recip_lattice, dimensions, kpoints


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print >> sys.stderr, "Error: no case provided"
        print >> sys.stderr, "Usage: {0} case".format(sys.argv[0])
        exit(1)

    # Parameters
    case_name = sys.argv[1]
    permutation = [2,1,0] # Permutation vector (changes "order" of dimensions)

    # Parse input
    real_lattice, recip_lattice, dimensions, kpoints = parse_win(case_name)

    # Calculate nnkpts
    nnkpts = calculate_nnkpts(dimensions)

    # Write output
    f = open(case_name + '.nnkp', 'w')

    write_date(f)
    write_calc_only_A(f) # TODO
    write_real_lattice(f, real_lattice)
    write_recip_lattice(f, recip_lattice)
    write_kpoints(f, kpoints)
    write_projections(f) # TODO
    write_nnkpts(f, nnkpts)
    write_exclude_bands(f) # TODO

    f.close()
