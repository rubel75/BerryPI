        Calculation of Spontaneous Polarization in BaTiO3

For the calculation of spontaneous polarization of BaTiO3 two reference structures has been chosen. One is tetragonal non-centrosymmetric (lambda1) where the atoms has moved from the equilibrium centrosymmetric positions in Z direction and another structure is centrosymmetric structure where the atoms are all positioned in centrosymmetric positions.


1 Case lambda1 (Non-centrosymmetric)
The atoms are in a non-centrosymmetric arrangement due to their movement in Z direction

1.1 Change the current directory to ~/tutorial/tutorial2/lambda1 

1.2 Perform WIEN2k initialization

$ init_lapw -b -vxc 13 -ecut -6 -numk 230

Here "-vxc 13" stands for PBE-GGA as exchange correlation function."-ecut -6" means the separation  energy of -6 Ry has been chosen to separate core electron from valance electron. �-numk 230" means that 230 k points has been chosen in Brillouin zone which generates 6*6*6 size k-mesh in the symmetric Brillouin zone

1.3 Execute WIEN2k scf calculation
 
$ run_lapw

in order to optimize the electron density.

Important: Do not use iterative diagonalization (-it switch) during standard SCF cycle. This will lead to incorrect polarization value.

1.4 Run BerryPI
 
$ berrypi

Enter 6:6:6 at the prompt


6:6:6 means the calculation is being done using 6*6*6 k-mesh in the full Brillouin zone (non symmetric) with a total of 216 k points.

Note: k-mesh in BerryPI should not necessarily be identical to that used in the SCF cycle

1.5 Once the calculation is completed the result will be printed like this

               ---POLARIZATION IN C/m^2 FOR [0 to 2] PHASE/2PI RANGE---

TOTAL POLARIZATION:  [1.4055711762420265e-11, 1.3912588500369445e-11, 0.31140111708550217]

              ---POLARIZATION IN C/m^2 FOR [-1 to +1] PHASE/2PI RANGE---

TOTAL POLARIZATION:  [1.4055711762420265e-11, 1.3912588500369445e-11, 0.31140111708550217]

Here three total polarization values corresponds to X,Y and Z components of polarization,respectively.

Note: The total polarization has been reported twice for different pi wrapping appraches. In this particular case both the polarization values are the identical which is generally may not be the case. Such case will be discussed in tutorial 2.


2 Case lambda0
The atoms are brought in centrosymmetric arrangement in order to compare its polarization with the non-centrosymmetric structure. 


2.1 Copy all files from lambda1 to lambda0 directory
 
$ cp * ../lambda0

2.2 Change the current directory to lambda0 

$ cd ../lambda0

2.3 Remove the lambda1.struct file. 

$ rm lambda1.struct

2.4 Rename all lambda1.* files to lambda0.* files with

$ rename_files lambda1 lambda0

2.5 Restore original k-mesh taking into account the symmetry 

$ x kgen

with 230 k-points (Shifted)

2.6 Initialize the electron density according to new structure
 
$ x dstart 

2.7 Run standard scf cycle.

$ run_lapw

2.8 Run BerryPI 

$ berrypi

Enter 6:6:6 at the prompt

2.9 Once the calculation is completed the results will be printed like this

               ---POLARIZATION IN C/m^2 FOR [0 to 2] PHASE/2PI RANGE---

  TOTAL POLARIZATION:        [1.390378584176154e-11, 1.3821906276378503e-11, 1.4486341471349937e-11]

              ---POLARIZATION IN C/m^2 FOR [-1 to +1] PHASE/2PI RANGE---

  TOTAL POLARIZATION:        [1.390378584176154e-11, 1.3821906276378503e-11, 1.4486341471349937e-11]]

Note: Different pi wrapping doesn�t affect the result in this case 


3 Spontaneous polarization 
Calculation of Spontaneous Polarization using the Z components of polarizations obtained in lambda1 and lambda0.The spontaneous polarization can be defined as the difference in Z component of polarization between the centrosymmetric P_z(lambda1). and non-centrosymmetric structure P_z(lambda0).

P_s= P_z(lambda1)- P_z(lambda0)= 0.31140111708550217-1.4486341471349937e-11= 0.3114011170710158 C/m^2

Here only Z components of polarization is considered because the atoms in non-centrosymmetric structure are displaced only in Z direction relative to the centrosymmetric structure
