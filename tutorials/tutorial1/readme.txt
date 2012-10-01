For Spontaneous polarization calculation


1. Change the current directory to ~/Help/BaTiO3/lambda1 

2. Run init_lapw -b -vxc 13 -ecut -6 -numk 230

This will initialize the calculation where "-vxc 13" stands for PBE-GGA as exchange correlation function."-ecut -6" means the separation  energy of -6 Ry has been chosen to separate core electron from valance electron. -numk 230" means that 230 k points has been chosen in Brillouion zone which generates 6*6*6 size k-mesh in the symmetric Brillouin zone

3. Run “run_lapw” command which will run a standard self consistency field cycle(SCF) in order to optimize electron density.

Note: Do not use iterative diagonalization (-it switch) durinf standard SCF cycle. This will give incorrect polarization value.

4. Run BerryPI using python with 
“python ~/SheikhProjects/BerryPI/berrypi –p$(pwd) –k6:6:6” command.

Here “–p$(pwd)” means that BerryPI program is running for all the file in the current directory.
“–k6:6:6” means the calculation is being done using 6*6*6 k-mesh in the full Brillouin zone (non symmetric) with a total of 216 k points.

5. Once the calculation is completed the result will be printed like this
:[ BerryPi ] Total Polarization in C/m^2 [2pi modulo]: [1.4055711762420265e-11, 1.3912588500369445e-11, 0.31140111708550217]
 [ BerryPi ] Total Polarization in C/m^2[-pi to +pi ] :[1.4055711762420265e-11, 1.3912588500369445e-11, 0.31140111708550217]

Note: In the result 2 values of Total polarization is reported. This is to avoid pi warping complications. This will be explained in detail in the second example file as here the final result is same in both the cases and will not affect the calculation of total polarization.3 values of polarization in both the cases represent polarization in X, Y and Z direction respectively.

6. Copy all file from lambda1 to lambda0 directory by “cp * ../lambda0” command

7. Change the current directory to lamda0 “cd ../lambda0”

8. Remove the lamdbda1.struct file. “rm lambda1.struct”

9. Rename all lambda1. files to lambda0. Files with 
“rename_files lambda1 lambda0” command

10. Run “x kgen” with 230 k points with shift of k mesh allowed to restore the original k-mesh taking into account the symmetry.
Or
“echo ”230
1” | x kgen” command can be run to do this in a single step.

11. Run “x dstart” again to calculate new charge density according to the new strucrure.

12. Run standard scf cycle again with “run_lapw” command.

13. Run BerryPI again with 
“python ~/SheikhProjects/BerryPI/berrypi –p$(pwd) –k6:6:6” command.
14. Once the calculation is completed the result will be printed like this

[ BerryPi ] Total Polarization in C/m^2 [2pi modulo]: :[1.390378584176154e-11, 1.3821906276378503e-11, 1.4486341471349937e-11]
[ BerryPi ] Total Polarization in C/m^2[-pi to +pi domain] :[1.390378584176154e-11, 1.3821906276378503e-11, 1.4486341471349937e-11]] 

15. The spontaneous polarization which is the difference in polarization between the centriosymmetric (lambda0) and non-centriosymmetric structure can be calculated as the difference in Z direction polarization in between lambda1 and lambda0 structure which will be ~0.31 C/m2.

