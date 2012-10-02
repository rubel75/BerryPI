    Calculation of Born effective charge of GaAs (Gallium Arsenide)

For the calculation of Born effective charge of As in GaAs one of the 4 As atoms has been displaced form it’s equilibrium position by +0.01(lambda1) and -0.01(lambda2) where they both represents fractional coordinates.

1 lambda1
Calculation of polarization for state where the As atom has been displaced by +0.01(fractional coordinate) from its equilibrium position.

1.1 Change the current directory to ~/tutorial/tutorial2/lambda1 

2.1.2 Perform WIEN2k initialization 

$ init_lapw -b -vxc 13 -ecut -8 -numk 230

Here "-vxc 13" stands for PBE-GGA as exchange correlation function."-ecut -8" means the separation  energy of -8 Ry has been chosen to separate core electron from valance electron. “-numk 230" means that 230 k points has been chosen in Brillouion zone which generates 6*6*6 size k-mesh in the symmetric Brillouion zone

1.3 Execute WIEN2k scf calculation
 
$ run_lapw

in order to optimize electron density.

Important: Do not use iterative diagonalization (-it switch) during standard SCF cycle. This will give incorrect polarization value.

1.4 Run BerryPI using python 
 
$ python ~/BerryPI/berrypi –p$(pwd) –k6:6:6
 
Here “–p$(pwd)” means that BerryPI program is running for the case (GaAs) preserved in the current directory.
“–k6:6:6” means the calculation is being done using 6*6*6 k-mesh in the full Brillouin zone (non symmetric) with a total of 216 k points.

Note: k-mesh in BerryPI should not necessarily be identical to that used in the SCF cycle

1.5 Once the calculation is completed the result will be printed like this
[ BerryPi ] Total Polarization in C/m^2 [2pi modulo]
:[0.7098546974245026, 0.7098547017401123, 0.4807039231832056]]
[ BerryPi ] Total Polarization in C/m^2[-pi to +pi ] 
:[-0.27302103729537935, -0.2730210329797696, 0.4807039231832056] 

Here three total polarization values corresponds to X,Y and Z components of polarization respectively. As the structure has just been perturbed in Z direction, only Z component of polarization has to be considered.  

Note: The total polarization has been reported twice for different pi wrapping complications. But in this particular case both the polarization values are the same which is generally may not be the case. This will be discussed later in this tutorial for the particular case where two polarization values are different and only one of them needs to be considered while using polarization value for further calculation.


2 lambda2
Calculation of polarization for state where the As atom has been displaced by -0.01(fractional coordinate) from its equilibrium position.

2.1 Copy all files from lambda1 to lambda2 directory
 
$ cp * ../lambda2

2.2 Change the current directory to lambda2 

$ cd ../lambda2

2.3 Remove the lambda1.struct file. 

$ rm lambda1.struct

2.4 Rename all lambda1.* files to lambda2.* files with

$rename_files lambda1 lambda2


2.5 Restore original k-mesh taking into account the symmetry 

$ x kgen

with 230 k points shifted 

2.6 Run
 
$ Initialize the electron density according to new structure.
 
$ x dstart 

2.7 Run standard scf cycle 

$ run_lapw

2.8 Run BerryPI 

$ python ~/BerryPI/berrypi –p$(pwd) –k6:6:6

2.9 Once the calculation is completed the results will be printed like this

[ BerryPi ] Total Polarization in C/m^2 [2pi modulo]
:[0.7098546978024558, 0.7098547017207987, 0.5021718070520651] 
[ BerryPi ] Total Polarization in C/m^2[-pi to +pi ] 
:[-0.27302103691742624, -0.2730210329990833, -0.4807039276678169] 

Note: Here too, the total polarization has been reported twice to avoid pi wrapping complications. But this time the two reported polarizations are different from each other and only one of them needs to be considered which is explained below.

Calculation of Born effective charge with the obtained Z component polarizations for lambda1 and lambda2 state.The Born effective charge can be calculated using the following formula,

Z*_zz=V/e * dP/du
Where,
Z*_zz is the born effective charge in Z direction for applied perturbation in Z direction.
V is the simulation cell volume [in m^3]= 1.863369880984677e-28 m^3.
e is the electronic charge [in C]= 1.60217646e-19 C
dP is the difference in polarization between 2 structures[in C/m^2] =-0.021467883868859505 C/m^2
du is displacement of atoms due to perturbation[in m]= 1.1423425476e-11 m
Note: Here 2 values of polarization for both the cases are reported. When calculating difference in polarization has to be taken the difference in polarization which corresponds to smallest difference in phase which means smallest difference in polarization [see “BerryPI: A software for studying polarization of crystalline solids with WIEN2k density functional all-electron package” for more details].

In this case two values of dP, -0.021467883868859505 C/m^2and 0.9614078508510224 C/m^2 can be found. But the smallest one is -0.021467883868859505 which corresponds to smallest different in total phase. Taking that value and putting those in the formula mentioned above will yield a Z*_zz of 
~-2.18.



