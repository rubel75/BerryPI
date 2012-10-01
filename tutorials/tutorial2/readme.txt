For Born Effective Charges 

1. Change the current directory to ./tutorial/tutorial2/lambda1 

2. Run init_lapw -b -vxc 13 -ecut -8 -numk 230

This will initialize the calculation where "-vxc 13" stands for PBE-GGA as exchange correlation function."-ecut -8" means the separation  energy of -8 Ry has been chosen to separate core electron from valance electron. -numk 230" means that 230 k points has been chosen in Brillouion zone which generates 6*6*6 size k-mesh in the symmetric Brillouin zone

3. Run “run_lapw” command which will run a standard self consistency field cycle(SCF) in order to optimize electron density.

Note: Do not use iterative diagonalization (-it switch) durinf standard SCF cycle. This will give incorrect polarization value.

4. Run BerryPI using python with 
“python ~/SheikhProjects/BerryPI/berrypi –p$(pwd) –k6:6:6” command.

Here “–p$(pwd)” means that BerryPI program is running for all the file in the current directory.
“–k6:6:6” means the calculation is being done using 6*6*6 k-mesh in the full Brillouin zone (non symmetric) with a total of 216 k points.

5. Once the calculation is completed the result will be printed like this
[ BerryPi ] Total Polarization in C/m^2 [2pi modulo]
:[0.7098546974245026, 0.7098547017401123, 0.4807039231832056]]
[ BerryPi ] Total Polarization in C/m^2[-pi to +pi ] 
:[-0.27302103729537935, -0.2730210329797696, 0.4807039231832056] 

Note: In the result 2 values of Total polarization is reported. This is to avoid pi warping complications. This will be explained later in this part of tutorial.

6. Copy all file from lambda1 to lambda2 directory by “cp * ../lambda2” command

7. Change the current directory to lambda2 “cd ../lambda2”

8. Remove the lambda1.struct file. “rm lambda1.struct”

9. Rename all lambda1. files to lambda2. files with
“rename_files lambda1 lambda2” command


10. Run “x kgen” with 230 k points with shift of k mesh allowed to restore the original k-mesh taking into account the symmetry.
Or
“echo ”230
1” | x kgen” command can be run to do this in a single step.

11. Run “x dstart” again to calculate new charge density according to the new strucrure.

12. Run standard scf cycle again with “run_lapw” command.

13. Run BerryPI again with 
“python berrypi –p$(pwd) –k6:6:6” command.

14. Once the calculation is completed the result will be printed like this

[ BerryPi ] Total Polarization in C/m^2 [2pi modulo]
:[0.7098546978024558, 0.7098547017207987, 0.5021718070520651] 
[ BerryPi ] Total Polarization in C/m^2[-pi to +pi ] 
:[-0.27302103691742624, -0.2730210329990833, -0.4807039276678169] 

15. The Born effective charge can be calculated using the following formula,

Z*_zz=V/e * dP/du
Where,
Z*_zz is the born effective charge in Z direction for applied perturbation in Z direction.
V is the simulation cell volume [in m^3].
e is the electronic charge [in C]
dP difference in polarization between 2 structures[in C/m^2]
du is displacement of atoms due to perturbation[in m]
Note that here 2 values of polarization for both the cases are reported. When calculating difference in polarization has to be taken the difference in polarization which corresponds to smallest difference in phase which means smallest difference in polarization[see “BerryPI: A software for studying polarization of crystalline solids with WIEN2k density functional all-electron package” for more details].

Here in this case we have 2 values of dP, -0.021467883868859505 C/m^2and 0.9614078508510224 C/m^2.But the smallest one is -0.021467883868859505 which corresponds to smallest different in total phase. Taking that value and putting those in the formula mentioned above will yield a Z*_zz of 
~-2.18.


