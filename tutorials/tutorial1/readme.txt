1. 
For the calculation of spontaneous polarization of BaTiO3 two reference structures has been chosen. One is tetragonal non-centrosymmetric (lambda1) where the atoms has moved from the equilibrium centrosymmetric positions in Z direction and another structure is centrosymmetric structure where the atoms are all positioned in centrosymmetric positions.

1.1 lambda1(Non-centrosymmetric)
The atoms are in non-centrosymmetric arrangement due to their movement in Z direction

1.1.1 Change the current directory to ~/tutorial/tutorial2/lambda1 

1.1.2 Run the following command

      $init_lapw -b -vxc 13 -ecut -6 -numk 230

This will initialize the calculation where "-vxc 13" stands for PBE-GGA as exchange correlation function."-ecut -6" means the separation  energy of -8 Ry has been chosen to separate core electron from valance electron. -numk 230" means that 230 k points has been chosen in Brillouin zone which generates 6*6*6 size k-mesh in the symmetric Brillouin zone

1.1.3 Run the command
 
$run_lapw

This will run a standard self consistency field cycle(SCF) in order to optimize electron density.

Note: Do not use iterative diagonalization (-it switch) during standard SCF cycle. This will give incorrect polarization value.

1.1.4 Run BerryPI using python with 
 
$python ~/BerryPI/berrypi –p$(pwd) –k6:6:6

Here “–p$(pwd)” means that BerryPI program is running for all the file in the current directory.
“–k6:6:6” means the calculation is being done using 6*6*6 k-mesh in the full Brillouin zone (non symmetric) with a total of 216 k points.

Note: k-mesh in BerryPI should not necessarily be identical to the oen that has been used in the SCF cycle

1.1.5 Once the calculation is completed the result will be printed like this
 [ BerryPi ] Total Polarization in C/m^2 [2pi modulo]: [1.4055711762420265e-11, 1.3912588500369445e-11, 0.31140111708550217]
 [ BerryPi ] Total Polarization in C/m^2[-pi to +pi ] :[1.4055711762420265e-11, 1.3912588500369445e-11, 0.31140111708550217]
Here three total polarization value corresponds to X,Y and Z component of polarization respectively.

Note: Here, the total polarization has been reported twice. This is to avoid pi wrapping complications. But in this particular case both the polarization value is same, so this will not add any complication in choosing the right one. This will be discussed later(Section 2.3.1) for the particular case where two polarization values are different and only one of them needs to be considered while using polarization value for calculation.


1.2 lambda0
The atoms are in centrosymmetric arrangement. 


1.2.1 Copy all file from lambda1 to lambda0directory
 
$cp * ../lambda0

1.2.2 Change the current directory to lambda0 

$cd ../lambda0

1.2.3 Remove the lambda1.struct file. 

$rm lambda1.struct

1.2.4 Rename all lambda1. files to lambda0. files with

$rename_files lambda1 lambda0

1.2.5 Run 

$x kgen

with 230 k points with shift of k mesh allowed to restore the original k-mesh taking into account the symmetry.

Or

$echo ”230
1” | x kgen
command can be run to do this in a single step.

1.2.6 Run
 
$x dstart 

to calculate new charge density according to the new structure.

2.2.7 Run standard scf cycle again with 

$run_lapw

2.2.8 Run BerryPI again with 

$python ~/BerryPI/berrypi –p$(pwd) –k6:6:6

2.2.9 Once the calculation is completed the result will be printed like this

[ BerryPi ] Total Polarization in C/m^2 [2pi modulo]: :[1.390378584176154e-11, 1.3821906276378503e-11, 1.4486341471349937e-11]
[ BerryPi ] Total Polarization in C/m^2[-pi to +pi domain] :[1.390378584176154e-11, 1.3821906276378503e-11, 1.4486341471349937e-11]] 

Note: Here too, the total polarization has been reported twice to avoid pi wrapping complications. But as both are same here too, this will not add any complication in choosing the right one. 


2.3
Calculation of Spontaneous Polarization using the Z components of polarizations obtained in lambda1 and lambda0.

2.3.1 The spontaneous polarization can be defined the difference in Z 
component of polarization between the centrosymmetric(P_z(lambda1). and non-centrosymmetric structure(P_z(lambda0).

P_s=(P_z(lambda1)- (P_z(lambda0)= ~0.31 C/m2

Here only Z components of polarization is taken because the atoms in non-centrosymmetric structure are displaced only in Z direction relative to the centrosymmetric structure
