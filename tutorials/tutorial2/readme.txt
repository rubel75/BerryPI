2.Calculation of Born effective charge of GaAs (Gallium Arsenide)

For the calculation of Born effective charge of As in GaAs one of the 4 As atoms has been displaced form it’s equilibrium position by +0.01(lambda1) and -0.01(lambda2) where they both represents fractional coordinates.

2.1 lambda1
Calculation of polarization for state where the As atom has been displaced by +0.01(fractional coordinates) from its equilibrium position.

2.1.1 Change the current directory to ~/tutorial/tutorial2/lambda1 

2.1.2 Run the following command

$init_lapw -b -vxc 13 -ecut -8 -numk 230

This will initialize the calculation where "-vxc 13" stands for PBE-GGA as exchange correlation function."-ecut -8" means the separation  energy of -8 Ry has been chosen to separate core electron from valance electron. -numk 230" means that 230 k points has been chosen in Brillouion zone which generates 6*6*6 size k-mesh in the symmetric Brillouion zone

2.1.3 Run the command
 
$run_lapw

This will run a standard self consistency field cycle(SCF) in order to optimize electron density.

Note: Do not use iterative diagonalization (-it switch) during standard SCF cycle. This will give incorrect polarization value.

2.1.4 Run BerryPI using python with 
 
$python ~/BerryPI/berrypi –p$(pwd) –k6:6:6

Here “–p$(pwd)” means that BerryPI program is running for all the file in the current directory.
“–k6:6:6” means the calculation is being done using 6*6*6 k-mesh in the full Brillouin zone (non symmetric) with a total of 216 k points.

Note: k-mesh in BerryPI should not necessarily be identical to the oen that has been used in the SCF cycle

2.1.5 Once the calculation is completed the result will be printed like this
[ BerryPi ] Total Polarization in C/m^2 [2pi modulo]
:[0.7098546974245026, 0.7098547017401123, 0.4807039231832056]]
[ BerryPi ] Total Polarization in C/m^2[-pi to +pi ] 
:[-0.27302103729537935, -0.2730210329797696, 0.4807039231832056] 

Here three total polarization value corresponds to X,Y and Z component of polarization respectively. As the structure has just been perturbed in Z direction, only Z component of polarization has to be considered.  

Note: Here, the total polarization has been reported twice. This is to avoid pi wrapping complications. But in this particular case both the polarization value is same. This will be discussed later for the particular case where two polarization values are different and only one of them needs to be considered while using polarization value for calculation.


2.2 lambda2
Calculation of polarization for state where the As atom has been displaced by -0.01(fractional coordinates) from its equilibrium position.

2.2.1 Copy all file from lambda1 to lambda2 directory
 
$cp * ../lambda2

2.2.2 Change the current directory to lambda2 

$cd ../lambda2

2.2.3 Remove the lambda1.struct file. 

$rm lambda1.struct

2.2.4 Rename all lambda1. files to lambda2. files with

$rename_files lambda1 lambda2


2.2.5 Run 

$x kgen

with 230 k points with shift of k mesh allowed to restore the original k-mesh taking into account the symmetry.
Or
$echo ”230
1” | x kgen
command can be run to do this in a single step.

2.2.6 Run
 
$x dstart 

to calculate new charge density according to the new strucrure.

2.2.7 Run standard scf cycle again with 

$run_lapw

2.2.8 Run BerryPI again with 

$python ~/BerryPI/berrypi –p$(pwd) –k6:6:6

2.2.9 Once the calculation is completed the result will be printed like this

[ BerryPi ] Total Polarization in C/m^2 [2pi modulo]
:[0.7098546978024558, 0.7098547017207987, 0.5021718070520651] 
[ BerryPi ] Total Polarization in C/m^2[-pi to +pi ] 
:[-0.27302103691742624, -0.2730210329990833, -0.4807039276678169] 

Note: Here too, the total polarization has been reported twice to avoid pi wrapping complications. But this time the two reported polarizations are different from each other and only one of them needs to be considered which has been discussed in the following section (2.3.1)

2.3 Calculation of Born effective charge with the obtained Z component polarizations for lambda1 and lambda2 state.

2.3.1 The Born effective charge can be calculated using the following formula,

Z*_zz=V/e * dP/du
Where,
Z*_zz is the born effective charge in Z direction for applied perturbation in Z direction.
V is the simulation cell volume [in m^3]= 1.863369880984677e-28 m^3.
e is the electronic charge [in C]= 1.60217646e-19 C
dP is the difference in polarization between 2 structures[in C/m^2] 
=-0.021467883868859505 C/m^2
du is displacement of atoms due to perturbation[in m]= 1.1423425476e-11 m
Note: Here 2 values of polarization for both the cases are reported. When calculating difference in polarization has to be taken the difference in polarization which corresponds to smallest difference in phase which means smallest difference in polarization [see “BerryPI: A software for studying polarization of crystalline solids with WIEN2k density functional all-electron package” for more details].

In this case two values of dP, -0.021467883868859505 C/m^2and 0.9614078508510224 C/m^2 can be found.But the smallest one is -0.021467883868859505 which corresponds to smallest different in total phase. Taking that value and putting those in the formula mentioned above will yield a Z*_zz of 
~-2.18.



