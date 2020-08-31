#!/usr/bin/env python
import sys
import numpy
import struct


def parse_win_mp_grid(f):
    parse_line_list = lambda line, delimiter, T : [T(y) for y in [x.strip() for x in line.strip().split(delimiter)] if y]
    for line in f.xreadlines():
        if 'mp_grid' in line:
            # mp_grid :         A     B     C
            # Split in two by :, take second half
            return parse_line_list(line.split(':')[1], ' ', int)


### Read file case.nnkp between lines "begin nnkpts" and "end nnkpts"
def parse_nnkp_nnkpts(f):
    nnkpts = []
    with f as input_data:
        for line in input_data:
            if line.strip() == 'begin nnkpts':
                break
        for line in input_data:
            if line.strip() == 'end nnkpts':
                break
            line1 = line.strip()
            line2 = line1.split()
            line3 = map(int, line2)
            line4 = tuple(line3) # change type for compatibility
            if len(line2) == 5: # fits to format (kp1, kp2, G1, G2, G3)
                nnkpts.append(line4)
    return nnkpts


### case.mmn parsing
def parse_pair_info_line(line):
    '''Converts a pair-info line into k1, k2, and a G vector
    '''
    # expected format(5i8)
    parts = struct.unpack("8s8s8s8s8s", line[0:40])
    if len(parts) != 5:
        raise RuntimeError('Incorrect number of values while parsing pair-info line:\n\t' + line.strip())

    k1 = float(parts[0])
    k2 = float(parts[1])
    G = (float(parts[2]), float(parts[3]), float(parts[4]))

    return k1, k2, G

def parse_matrix_element_line(line):
    '''Converts a matrix element line into a value
    '''

    # expected format(32f18.12)
    (real_part,imaginary_part) = struct.unpack("18s18s", line[0:36])
    real_part = float(real_part)
    imaginary_part = float(imaginary_part)

    return real_part + imaginary_part * 1j

def parse_mmn_info_line(line):

    # expected format: write(unit_mmn,'(3I12)') Nb, Nk, Nntot
    (n_energy,n_pairs,n_neighbours) = struct.unpack("12s12s12s", line[0:36])
    n_energy = int(n_energy)
    n_pairs = int(n_pairs)
    n_neighbours = int(n_neighbours)

    return n_energy, n_pairs, n_neighbours 

###

def determine_neighbours(D, d, P = [0,1,2]):
    '''Computes a bidirectional graph of points who are adjacent in the
       grid of dimensions `D', in the forward direction given by `d'.

       The value at each node in the graph is a tuple containing the
       linear index of the neighbour in the direction `d' and another
       containing the linear index of the neighbour in the direction `-d'.

       The resulting graph will be acyclic. The end-points of each path
       are forward or backward values of None.

       The order of the dimensions for computing the linear index are
       given by P (C-style [0,1,2], FORTRAN-style [2,1,0])

       Additionally, a list of all tuples of pairs of points is generated.
       These tuples contain the linear index of the first point, the
       linear index of the second point, and the G vector of the second
       point.

       Returns: pair tuple list, neighbour graph
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
    nnkpts = []
    neighbour_graph = {}

    # We iterate through each point in the mesh deriving the linear index
    # for the point and its neighbour in the positive d direction.
    # We will keep track of the fact that the neighbours are neighbours
    # in two ways:
    # 1) a bidirectional graph (A will point forward to B and B
    #    will point backward to A)
    # 2) a list of pairs (A and B will become a tuple in this list)
    for a in range(D[0]):
        for b in range(D[1]):
            for c in range(D[2]):
                # Build k-point and neighbour vectors
                v = [a, b, c]
                v_neighbour, G = wrap_vector(vector_add(v, d), d, D)
    
                # Get indices for vectors
                i = linear_index(permute(v, P), permute(D, P)) + 1
                i_neighbour = linear_index(permute(v_neighbour, P), permute(D, P)) + 1

                # Add pair to graph of neighbours
                if not neighbour_graph.has_key(i):
                    neighbour_graph[i] = [None, None] # Create the node
        
                if not neighbour_graph.has_key(i_neighbour):
                    neighbour_graph[i_neighbour] = [None, None] # Create the neighbour node 
        
                # Save the pair in the graph (... if the pair doesn't extend
                # the volume boundaries)
                if G.count(0) == 3: 
                    neighbour_graph[i][1] = i_neighbour # A --> B (forward) 
                    neighbour_graph[i_neighbour][0] = i # A <-- B (backward)

                # Remember neighbours as a tuple
                nnkpts.append((i, i_neighbour, G[0], G[1], G[2]))

    return nnkpts, neighbour_graph

def print_usage():
    print >> sys.stderr, "Usage: mmn2pathphase case [direction] [-w]"
    print >> sys.stderr, " direction    x, y, or z; for <x, y, z> (default x)"
    print >> sys.stderr, " -w option is for Weyl k-path calculation"


###############################################################################
# Begin MAIN
###############################################################################

def main(args):

    #VERBOSE = True
    VERBOSE = False # Whether or not to print extra info

    ### case.win parsing
    parse_line_list = lambda line, delimiter, T : [T(y) for y in [x.strip() for x in line.strip().split(delimiter)] if y]

    if len(args) < 2:
        print >> sys.stderr, "Error: no case or direction provided"
        exit(1)

    spOption = '' # no spin polarization by default
    wCalc = False # no Weyl point path by default
    for arg in args: # check for spin polarization and Weyl path in arguments
        if '-up' in arg:
            spOption = 'up'
        elif '-dn' in arg:
            spOption = 'dn'
        elif '-w' in arg:
            wCalc = True

    # Get case name from arguments
    case_name = args[0]

    # Get direction from arguments
    direction_args = {'x': [1, 0, 0],
                      'y': [0, 1, 0],
                      'z': [0, 0, 1]}

    if len(args) > 2:
        if not direction_args.has_key(args[1]):
            print >> sys.stderr, "Error: unknown direction '{0}'".format(args[1])
            exit(1)

        direction = direction_args[args[1]]
    else:
        direction = direction_args['x']

    # Initialize some lists
    phases = {} # for index k, the phase between k and its neighbour along the specified direction
    phase_sums = [] # for index k, the accumulated phase along the path in the specified direction starting at k

    # Get k-mesh information from case.win
    f_win = open(case_name + '.win' + spOption, 'r')
    kmesh = parse_win_mp_grid(f_win)
    f_win.close()

    # Determine the k(i)-k(i+1) neighbours of interest
    if wCalc: # read from case.nnkp file
        f_nnkp = open(case_name + '.nnkp' + spOption, 'r')
        nnkpts = parse_nnkp_nnkpts(f_nnkp)
        f_nnkp.close()
    else: # Calculate the neighbours of interest
        nnkpts, neighbour_graph = determine_neighbours(kmesh, direction, [2, 1, 0])
        #  > we need the pairs list (nnkpts) to discriminate values found in the
        #    case.mmn file
        #  > we need the neighbour graph (neighbour_graph) in order to find the sum
        #    of the phase differences along each path in the given direction

    if VERBOSE:
        print nnkpts

    # Open file containing Mmn data (case.mmn[up/dn])
    f_mmn = open(case_name + '.mmn' + spOption, 'r')
    f_mmn.readline() # Ignore first line

    n_energy, n_pairs, n_neighbours = parse_mmn_info_line(f_mmn.readline())

    # Determine the phase from Mmn for each pair
    #  > the phase difference between points k1 and k2 in the direction provided
    #    will be stored in phases[k1]
    for i in range(n_pairs * n_neighbours):
        # Read pair info line
        k1, k2, G = parse_pair_info_line(f_mmn.readline())

        # Is this a pair in one of our paths?
        if (k1, k2, G[0], G[1], G[2]) in nnkpts:
            # Create empty square matrix for the pair
            pair_matrix = numpy.zeros(shape=(n_energy, n_energy), dtype=complex)

            # Read in the pair matrix
            for a in range(n_energy):
                for b in range(n_energy):
                    # Read matrix element line
                    element_value = parse_matrix_element_line(f_mmn.readline())

                    # Put value into matrix
                    pair_matrix[a, b] = element_value

            # Determine the phase between the pair from the matrix determinant
            det_Mmn = numpy.linalg.det(pair_matrix)
            phases[k1] = numpy.angle(det_Mmn)

            if VERBOSE:
                print "(k1, k2, G)=", (k1, k2, G)
                print "pair_matrix Mmn=", pair_matrix
                print "eig(pair_matrix)=", numpy.linalg.eig(pair_matrix)[0]
                print "det_Mmn=", det_Mmn
                print "numpy.angle(det_Mmn)=", numpy.angle(det_Mmn)
                print '---'
        else:
            if VERBOSE:
                print 'Discarding <{0},{1}> <{2},{3},{4}>'.format(k1, k2, G[0], G[1], G[2])
                print '---'

            # Read over and discard the data if it's not a pair of interest
            for a in range(n_energy):
                for b in range(n_energy):
                    parse_matrix_element_line(f_mmn.readline())

    f_mmn.close()

    if wCalc:
        print("Berry phase along the path (rad) =",phases.values())
        print("Berry phase sum (rad) =",sum(phases.values()))
        sys.exit()


    # Get the sum of phases for each path
    for k, neighbours in neighbour_graph.iteritems():
        k_prev = neighbours[0]
        k_next = neighbours[1]

        # We'll see if this node is an endpoint. If it is, we'll traverse
        # backwards summing the phase differences until we reach the start
        if k_next is None: # Graph ends at k with no k_next
            phase_sum = phases[k]

            # Propagate backward through graph, accumulating phase difference
            # at each pair (this _must_ be acyclic)
            while k_prev:
                # .. accumulate
                phase_sum = phase_sum + phases[k_prev]

                # .. move onto the next node
                k = k_prev
                neighbours = neighbour_graph[k_prev]
                k_prev = neighbours[0]

            # k should be the starting item in the graph.
            # Record starting k and the accumulated phase
            phase_sums.append((k, phase_sum))

    # Sort accumulated phases by ascending k
    phase_sums.sort(key=lambda x:x[0]) # TODO use sorted

    # Write out path phases
    f_pathphase = open(case_name + '.pathphase' + spOption, 'w')

    # Write out number of paths 
    f_pathphase.write('%4d\n' % len(phase_sums))

    # Write out path direction vector
    f_pathphase.write(' %2d %2d %2d\n' % (direction[0], direction[1], direction[2]))

    # Write out phases
    for k, phase_sum in phase_sums:
        f_pathphase.write(' %6d    %.12f\n' % (k, phase_sum))

    f_pathphase.close()

    return phase_sums

###############################################################################
# end MAIN
###############################################################################

if __name__ == "__main__":

    main(sys.argv[1:]) # path all arguments except for the first one

###############################################################################

###############################################################################
