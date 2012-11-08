            Calculation of Born effective charge of GaAs 

For the calculation of Born effective charge of As in GaAs one of the 4 As atoms has been displaced along Z-axis form it’s equilibrium position by +0.01(lambda1) and -0.01(lambda2) in fractional coordinates.


1 Case lambda1
Calculation of total phase (sum of electronic and ionic phase) for state where the As atom has been displaced by +0.01 (fractional coordinate) from its equilibrium position.

1.1 Change the current directory to ~/tutorial/tutorial2/lambda1 

1.2 Perform WIEN2k initialization 

$ init_lapw -b -vxc 13 -ecut -6 -numk 230

Here "-vxc 13" stands for PBE-GGA as exchange correlation function."-ecut -6" means the separation  energy of -6 Ry has been chosen to separate core electron from valance electron. “-numk 230" means that 230 k points has been chosen in Brillouion zone which generates 6*6*6 size k-mesh in the symmetric Brillouion zone

1.3 Execute WIEN2k scf calculation
 
$ run_lapw

in order to optimize the electron density.

Important: Do not use iterative diagonalization (-it switch) during the standard SCF cycle. This will give lead to inappropriate phase value.

1.4 Run BerryPI using python 
 
$ python ~/BerryPI/berrypi –p$(pwd) –k6:6:6
 
Here “–p$(pwd)” means that BerryPI program is running for the case (GaAs) located in the current directory.
“–k6:6:6” means the calculation is being done using 6*6*6 k-mesh in the full Brillouin zone (non symmetric) with a total of 216 k points.

Note: k-mesh in BerryPI should not necessarily be identical to that used in the SCF cycle

1.5 Once the calculation is completed the result will be printed like this

               ---PHASES/2*PI IN [0 to 2]RANGE---

 TOTAL PHASE/(2*PI):       [1.4444444466908883, 1.4444444597055879, 0.9779037963902364]

              ---PHASES/2*PI IN [-1 to +1]RANGE---

TOTAL PHASE/(2*PI):        [-0.5555555533091117, -0.5555555402944121, 0.9779037963902364]

Here three total phase (sum of electronic and ionic phase)  values corresponds to X,Y and Z components of total phase, respectively. As the structure has only been perturbed in Z direction, only Z component of total phase has to be considered.  

Note: The total phase has been reported twice for different pi wrapping approaches. In this particular case both the phase values are the identical which is generally may not be the case. 


2 Case lambda2
Calculation of total phase (sum of electronic and ionic phase) for state where the As atom has been displaced by -0.01 (fractional coordinate) from its equilibrium position.

2.1 Copy all files from lambda1 to lambda2 directory
 
$ cp * ../lambda2

2.2 Change the current directory to lambda2 

$ cd ../lambda2

2.3 Remove the lambda1.struct file. 

$ rm lambda1.struct

2.4 Rename all lambda1.* files to lambda2.* files 

$ rename_files lambda1 lambda2


2.5 Restore original k-mesh taking into account the symmetry 

$ x kgen

with 230 k-points (Shifted) 

2.6 Initialize the electron density according to new structure
 
$ x dstart 

2.7 Run standard scf cycle 

$ run_lapw

2.8 Run BerryPI 

$ python ~/BerryPI/berrypi –p$(pwd) –k6:6:6

2.9 Once the calculation is completed the results will be printed like this
               ---PHASES/2*PI IN [0 to 2]RANGE---

 TOTAL PHASE/(2*PI):        [1.4444444467891686, 1.444444439721803, 1.0220961933526282]

              ---PHASES/2*PI IN [-1 to +1]RANGE---

TOTAL PHASE/(2*PI):        [-0.5555555532108314, -0.555555560278197, -0.9779038066473718]

Note: This time, the two reported phases (sum of electronic and ionic phase) are different from each other and only one of them needs to be considered as explained below.


3. Born effective charge
Calculation of Born effective charge using Z component of total phase value obtained for lambda1 and lambda2 case. The Born effective charge can be calculated using the following formula,

Z*_zz=(1/2*pi)*d_phi/d_rho 
Where,
Z*_zz is the born effective charge in Z direction for applied perturbation in Z direction.
d_phi is difference in total phase (sum of electronic and ionic phase) between the two structure(in the units of 2*pi)= 0.9779037963902364-1.0220961933526282= -0.044192396962391856 (in the units of 2*pi)
d_rho is the relative displacement of the particular atom(in fractional coordinate)= 0.01—(-0.01)= 0.02

So, 
Z*_zz=(1/2*pi)* (-0.044192396962391856*2*pi)/0.02= -2.2096198481195928

Note: Here 2 values of total phase (sum of electronic and ionic phase) for both the cases are reported. When calculating the difference in total phase between two structures, one has to be careful of pi wrapping artifact. For example in this current study if the difference in phase is taken from the 2*pi modulo values this will lead to a phase difference of -0.044192396962391856. On the other hand if the difference is taken from –pi to +pi domain values this lead to a phase difference of 1.9558076030376081. It has be realized that both this difference values represents the difference between both the cases but they just consider different paths when the phase difference is considered in a 2*pi(360 degree) circle[see “BerryPI: A software for studying polarization of crystalline solids with WIEN2k density functional all-electron package” for more details]. Taking the biggest difference (1.9558076030376081) in phase will lead to inappropriate results. So while taking the difference in phase one has to take the smallest number which is -0.044192396962391856 in this case. This should also be taken care of while calculating the difference in polarization. In this particular case putting the smallest difference will lead to a born effective charge of -2.2096198481195928 for As.



