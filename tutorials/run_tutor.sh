#!/bin/bash 
#
# execution:
#   $ source run_tutor
# or
#   $ for f in {7..20}; do echo $f | source run_tutor.sh | tee -a tests.out ; done
#
#
# Developed by Anton Bokhanchuk
# revised and expanded by Oleg Rubel

clear
echo "######################################################"
echo "Type the test number and press ENTER to run that test:"
echo "1 - Tutorial 1: Lambda1 and Lambda0"
echo "2 - Tutorial 2: Lambda1 and Lambda2"
echo "3 - Tutorial 3: GaAs1 and GaAs2"
echo "4 - Tutorial 4: GaN-W and GaN-ZB"
echo "5 - All Tests (7-20, 101, 102)"
echo "6 - Clean All"
echo ""
echo "T E S T S (serial):"
echo "7 - Test BaTiO3: Lambda1"
echo "8 - Test BaTiO3: Lambda1 (-s) spin polarization"
echo "9 - Test BaTiO3: Lambda1 (-j) spin orbit"
echo "10 - Test BaTiO3: Lambda1 (-o) orb. potential + U=0.1 Ry (spin polarization implied)"
echo "11 - Test BaTiO3: Lambda1 (-s -j) spin polarization & SOC"
echo "12 - Test BaTiO3: Lambda1 (-o -j) SOC & orb. potential + U=0.1 Ry (spin polarization implied)"
echo "101 - Test TaAs: Weyl point charge (single Wilson loop)"
echo "102 - Test TaAs: Weyl point charge (series of Wilson loops via WloopPHI.py)"
echo ""
echo "T E S T S (parallel):"
echo "13 - Test BaTiO3: Lambda1 (-p) spin polarization (parallel 2 cores)"
echo "14 - Test BaTiO3: Lambda1 (-s -p) spin polarization (parallel 2 cores)"
echo "15 - Test BaTiO3: Lambda1 (-j) spin orbit (parallel 2 cores)"
echo "16 - Test BaTiO3: Lambda1 (-o) orb. potential + U=0.1 Ry (spin polarization implied) (parallel 2 cores)"
echo "17 - Test BaTiO3: Lambda1 (-s -j) spin polarization & SOC (parallel 2 cores)"
echo "18 - Test BaTiO3: Lambda1 (-o -j) SOC & orb. potential + U=0.1 Ry (spin polarization implied) (parallel 2 cores)"
echo "19 - Test BaTiO3: Lambda1 (--sp_c) spin polar. constrained (non-magnetic, up=dn) (parallel 2 cores)"
echo "20 - Test BaTiO3: Lambda1 (--sp_c -o) spin polar. constrained (non-magnetic, up=dn) + orb. potential + U=0.1 Ry (parallel 2 cores)"
echo "######################################################"
read choice

menu() {

case "$choice" in
	1)
      CleanTut_1
	  Tutorial_1
	  ;;
	2)
	  echo "Running Tutorial 2"
      CleanTut_2
	  Tutorial_2
	  ;;
	3)
	  echo "Running Tutorial 3"
      CleanTut_3
	  Tutorial_3
	  ;;
	4)
	  echo "Running Tutorial 4"
      CleanTut_4
	  Tutorial_4
	  ;;
	5) 
	  echo "Running ALL test"
      CleanTut_1
      Tutorial_7
      CleanTut_1
      Tutorial_8
      CleanTut_1
      Tutorial_9
      CleanTut_1
      Tutorial_10
      CleanTut_1
      Tutorial_11
      CleanTut_1
      Tutorial_12
      CleanTut_1
      Tutorial_13
      CleanTut_1
      Tutorial_14
      CleanTut_1
      Tutorial_15
      CleanTut_1
      Tutorial_16
      CleanTut_1
      Tutorial_17
      CleanTut_1
      Tutorial_18
      CleanTut_1
      Tutorial_19
      CleanTut_1
      Tutorial_20
      CleanTut_5
      Tutorial_101
      CleanTut_5
      Tutorial_102
	  ;;
	6)
	  echo "Cleaning up all files"
	  CleanTut_1
	  CleanTut_2
	  CleanTut_3
	  CleanTut_4
      CleanTut_5
	  rm -rf *.out
	  ;;
	7)
      CleanTut_1
	  Tutorial_7
	  ;;
    8)
      CleanTut_1
	  Tutorial_8
	  ;;
    9)
      CleanTut_1
	  Tutorial_9
	  ;;
    10)
      CleanTut_1
	  Tutorial_10
	  ;;
    11)
      CleanTut_1
	  Tutorial_11
	  ;;
    12)
      CleanTut_1
	  Tutorial_12
	  ;;
    101)
      CleanTut_5
	  Tutorial_101
	  ;;
    102)
      CleanTut_5
	  Tutorial_102
	  ;;
    13)
      CleanTut_1
	  Tutorial_13
	  ;;
    14)
      CleanTut_1
	  Tutorial_14
	  ;;
    15)
      CleanTut_1
	  Tutorial_15
	  ;;
    16)
      CleanTut_1
	  Tutorial_16
	  ;;
    17)
      CleanTut_1
	  Tutorial_17
	  ;;
    18)
      CleanTut_1
	  Tutorial_18
	  ;;
    19)
      CleanTut_1
	  Tutorial_19
	  ;;
    20)
      CleanTut_1
	  Tutorial_20
	  ;;
	*)
	  echo "Unknown option"
esac
}

CleanTut_1 () {
	cd tutorial1
	rm -rf *.out
	cd lambda1
	ls -1 | grep -v 'lambda1.struct$' | xargs rm -f
       cd ../lambda0
	ls -1 | grep -v 'lambda0.struct$' | xargs rm -f
	cd ../../
	echo "dir tutorial1: All files but lambda1.struct and lambda0.struct were removed!"
}

CleanTut_2 () {
	cd tutorial2
	rm -rf Tutorial2_1.out Tutorial2_2.out
	cd lambda1
	ls -1 | grep -v 'lambda1.struct$' | xargs rm -f
       cd ../lambda2
	ls -1 | grep -v 'lambda2.struct$' | xargs rm -f
	cd ../../
	echo "dir tutorial2: All files but lambda1.struct and lambda2.struct were removed!"
}

CleanTut_3 () {
	cd tutorial3
	rm -rf Tutorial3_1.out Tutorial3_2.out
	cd GaAs1
	ls -1 | grep -v 'GaAs1.struct$' | xargs rm -f
       cd ../GaAs2
	ls -1 | grep -v 'GaAs2.struct$' | xargs rm -f
	cd ../../
	echo "dir tutorial3: All files but GaAs1.struct and GaAs2.struct were removed!"
}

CleanTut_4 () {
	cd tutorial4
	rm -rf Tutorial4_1.out Tutorial4_2.out
	cd GaN-W
	ls -1 | grep -v 'GaN-W.struct$' | xargs rm -f
       cd ../GaN-ZB
	ls -1 | grep -v 'GaN-ZB.struct$' | xargs rm -f
	cd ../../
	echo "dir tutorial4: All files but GaN-W.struct and GaN-ZB.struct were removed!"
}

CleanTut_5 () {
	cd tutorial5
    echo $PWD
    ls -1a | grep -v -e 'TaAs.struct$' -e 'TaAs.klist_band$' -e 'readme.txt$' -e '^\.$' -e '^\.\.$' | xargs rm -f # remove all files/dir except "TaAs.struct", "TaAs.klist_band", and "readme.txt"
	cd ../
	echo "dir tutorial5: All files but TaAs.struct, TaAs.klist_band, and readme.txt were removed!"
}

Tutorial_1 () {
echo "Running Tutorial 1"
cd tutorial1/lambda1
init_lapw -b -rkmax 4 -vxc 13 -ecut -6 -numk 230
run_lapw
berrypi -k6:6:6
echo "EXPECTED LAMBDA1:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [-8.711747e-12, -8.368475e-13,  4.803326e-01]
Ionic polarization (C/m2)          sp(1)  [ 1.365657e-11,  1.365657e-11, -1.760570e-01]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [ 4.944823e-12,  1.281972e-11,  3.042756e-01]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [ 4.944823e-12,  1.281972e-11,  3.042756e-01]
======================================================================================="
cp * ../lambda0
cd ../lambda0
rm lambda1.struct
rename_files lambda1 lambda0
echo -e "230\n1\n" | x kgen
x dstart
run_lapw
berrypi -k6:6:6
echo "EXPECTED LAMBDA0:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [ 1.164531e-13,  1.338068e-13, -2.574002e-13]
Ionic polarization (C/m2)          sp(1)  [ 1.365657e-11,  1.365657e-11,  1.380018e-11]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [ 1.377302e-11,  1.379038e-11,  1.354278e-11]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [ 1.377302e-11,  1.379038e-11,  1.354278e-11]
======================================================================================="
cd ../../
}

Tutorial_2 () {
echo "Running Tutorial 2"
cd tutorial2/lambda1
init_lapw -b -rkmax 4 -vxc 13 -ecut -6 -numk 230
run_lapw
berrypi -k6:6:6
echo "EXPECTED LAMBDA1:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [-4.863642e-11,  3.049161e-10, -8.357582e-02]
Ionic polarization (C/m2)          sp(1)  [ 2.855857e-10,  2.855857e-10,  7.301465e-02]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [ 2.369493e-10,  5.905018e-10, -1.056116e-02]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [ 2.369493e-10,  5.905018e-10, -1.056116e-02]
======================================================================================="
cp * ../lambda2
cd ../lambda2
rm lambda1.struct
rename_files lambda1 lambda2
echo -e "230\n1\n" | x kgen
x dstart
run_lapw
berrypi -k6:6:6
echo "EXPECTED LAMBDA2:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [ 1.870846e-10,  2.625904e-10,  8.357696e-02]
Ionic polarization (C/m2)          sp(1)  [ 2.855857e-10,  2.855857e-10, -7.301465e-02]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [ 4.726703e-10,  5.481761e-10,  1.056231e-02]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [ 4.726703e-10,  5.481761e-10,  1.056231e-02]
======================================================================================="
cd ../../
}

Tutorial_3 () {
echo "Running Tutorial 3"
cd tutorial3/GaAs1
linenr=$(grep -n -m 1 "ATOM  -2: X=0.25000000 Y=0.25000000 Z=0.25100000" GaAs1.struct | cut -d':' -f1)
sed -i "${linenr}d" GaAs1.struct
sed -i "${linenr}i\ATOM  -2: X=0.25100000 Y=0.25200000 Z=0.25300000" GaAs1.struct
init_lapw -b -vxc 5 -rkmax 4 -numk 800
linenr=$(grep -n -m 1 "ATOM  -2: X=0.25100000 Y=0.25200000 Z=0.25300000" GaAs1.struct | cut -d':' -f1)
sed -i "${linenr}d" GaAs1.struct
sed -i "${linenr}i\ATOM  -2: X=0.25000000 Y=0.25000000 Z=0.25100000" GaAs1.struct
x dstart
run_lapw
berrypi -k 6:6:6
echo "EXPECTED GaAs1:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [ 9.769755e-01,  9.769755e-01, -9.593836e-01]
Ionic polarization (C/m2)          sp(1)  [-5.013188e-01, -5.013188e-01, -4.712397e-01]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [ 4.756567e-01,  4.756567e-01, -1.430623e+00]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [ 4.756567e-01,  4.756567e-01, -1.430623e+00]
======================================================================================="
cp * ../GaAs2
cd ../GaAs2
rename_files GaAs1 GaAs2
linenr=$(grep -n -m 1 "ATOM  -2: X=0.25000000 Y=0.25000000 Z=0.25100000" GaAs2.struct | cut -d':' -f1)
sed -i "${linenr}d" GaAs2.struct
sed -i "${linenr}i\ATOM  -2: X=0.25000000 Y=0.25000000 Z=0.24900000" GaAs2.struct
echo -e "800\n1\n" | x kgen
x dstart
rm *scf
run_lapw
berrypi -k 6:6:6
echo "EXPECTED GaAs2:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [-9.593715e-01, -9.593715e-01,  9.769706e-01]
Ionic polarization (C/m2)          sp(1)  [-5.013188e-01, -5.013188e-01, -5.313979e-01]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [-1.460690e+00, -1.460690e+00,  4.455726e-01]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [-1.460690e+00, -1.460690e+00,  4.455726e-01]
======================================================================================="
cd ../../
}

Tutorial_4 () {
echo "Running Tutorial 4"
cd tutorial4/GaN-W
init_lapw -b -vxc 5 -rkmax 7 -numk 300
run_lapw
berrypi -k 8:8:8
echo "EXPECTED GaN-W:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [ 2.223396e-10,  1.205149e-07, -5.612307e-02]
Ionic polarization (C/m2)          sp(1)  [ 1.750356e-10, -2.049427e-07, -4.386009e-01]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [ 3.973752e-10, -8.442784e-08, -4.947239e-01]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [ 3.973752e-10, -8.442784e-08, -4.947239e-01]
======================================================================================="
cd ../GaN-ZB
init_lapw -b -vxc 5 -rkmax 7 -numk 200
run_lapw
berrypi -k 8:8:8
echo "EXPECTED GaN-ZB:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [-1.219101e-03,  1.219101e-03, -1.727041e-04]
Ionic polarization (C/m2)          sp(1)  [ 1.165061e-10,  1.165088e-10, -4.644818e-01]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [-1.219101e-03,  1.219101e-03, -4.646545e-01]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [-1.219101e-03,  1.219101e-03, -4.646545e-01]
======================================================================================="
cd ../../
}

######################################################################################
#                                                                                    #
#                                 T E S T S                                          #
#                                                                                    #
######################################################################################

######################################################################################
# simplest test
######################################################################################
Tutorial_7 () {
echo "Running test 7"
cd tutorial1/lambda1
init_lapw -b -rkmax 4 -vxc 13 -ecut -6 -numk 100
run_lapw -ec 0.0001 -cc 0.001
berrypi -k4:4:4
echo "EXPECTED LAMBDA1:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [-1.923689e-13, -1.887044e-14,  4.775890e-01]
Ionic polarization (C/m2)          sp(1)  [ 0.000000e+00,  0.000000e+00, -1.760570e-01]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [-1.923689e-13, -1.887044e-14,  3.015320e-01]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [-1.923689e-13, -1.887044e-14,  3.015320e-01]
======================================================================================="
cd ../../
}

######################################################################################
# spin polarized test
######################################################################################
Tutorial_8 () {
echo "Running test 8"
cd tutorial1/lambda1
init_lapw -b -rkmax 4 -vxc 13 -ecut -6 -numk 100 -sp
runsp_lapw -ec 0.0001 -cc 0.001
berrypi -k4:4:4 -s
echo "EXPECTED LAMBDA1:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [ 8.750656e-14, -1.187667e-13,  2.387163e-01]
Ionic polarization (C/m2)          sp(1)  [ 0.000000e+00,  0.000000e+00, -8.802849e-02]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [ 8.750656e-14, -1.187667e-13,  1.506878e-01]
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(2)  [ 2.304258e-14,  7.144456e-14,  2.387355e-01]
Ionic polarization (C/m2)          sp(2)  [ 0.000000e+00,  0.000000e+00, -8.802849e-02]
Tot. spin polariz.=Pion+Pel (C/m2) sp(2)  [ 2.304258e-14,  7.144456e-14,  1.507070e-01]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [ 1.105491e-13, -4.732215e-14,  3.013949e-01]
======================================================================================="
cd ../../
}

######################################################################################
# SOC test
######################################################################################
Tutorial_9 () {
echo "Running test 9"
cd tutorial1/lambda1
export EDITOR=cat
init_lapw -b -rkmax 4 -vxc 13 -ecut -6 -numk 100
echo -e "0 0 1\n\n\n\nN\n" | init_so_lapw
run_lapw -so -ec 0.0001 -cc 0.001
berrypi -k4:4:4 -j
echo "EXPECTED LAMBDA1:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [-6.280788e-13,  3.212734e-13,  4.776611e-01]
Ionic polarization (C/m2)          sp(1)  [ 0.000000e+00,  0.000000e+00, -1.760570e-01]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [-6.280788e-13,  3.212734e-13,  3.016041e-01]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [-6.280788e-13,  3.212734e-13,  3.016041e-01]
======================================================================================="
cd ../../
}

######################################################################################
# ORB test
######################################################################################
Tutorial_10 () {
echo "Running test 10"
cd tutorial1/lambda1
export EDITOR=cat
init_lapw -b -rkmax 4 -vxc 13 -ecut -6 -numk 100 -sp
echo -e "Ti 2 0.1 0.0\n" | init_orb_lapw -orb # Ti d U=0.1Ry J=0
runsp_lapw -orb -ec 0.0001 -cc 0.001
berrypi -k4:4:4 -o
echo "EXPECTED LAMBDA1:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [ 7.114637e-14, -9.577591e-14,  2.366018e-01]
Ionic polarization (C/m2)          sp(1)  [ 0.000000e+00,  0.000000e+00, -8.802849e-02]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [ 7.114637e-14, -9.577591e-14,  1.485733e-01]
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(2)  [-9.326347e-15,  8.590123e-14,  2.366149e-01]
Ionic polarization (C/m2)          sp(2)  [ 0.000000e+00,  0.000000e+00, -8.802849e-02]
Tot. spin polariz.=Pion+Pel (C/m2) sp(2)  [-9.326347e-15,  8.590123e-14,  1.485864e-01]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [ 6.182002e-14, -9.874680e-15,  2.971597e-01]
======================================================================================="
cd ../../
}

######################################################################################
# spin polarization + SOC test
######################################################################################
Tutorial_11 () {
echo "Running test 11"
cd tutorial1/lambda1
export EDITOR=cat
init_lapw -b -rkmax 4 -vxc 13 -ecut -6 -numk 100 -sp
echo -e "0 0 1\n\n\n\ny\ny\n100\nN\n" | init_so_lapw
runsp_lapw -so -ec 0.0001 -cc 0.001
berrypi -k4:4:4 -s -j
echo "EXPECTED LAMBDA1:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [-1.249460e-12,  2.728865e-13,  4.775250e-01]
Ionic polarization (C/m2)          sp(1)  [ 0.000000e+00,  0.000000e+00, -1.760570e-01]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [-1.249460e-12,  2.728865e-13,  3.014681e-01]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [-1.249460e-12,  2.728865e-13,  3.014681e-01]
======================================================================================="
cd ../../
}

######################################################################################
# SOC + ORB test
######################################################################################
Tutorial_12 () {
echo "Running test 12"
cd tutorial1/lambda1
export EDITOR=cat
init_lapw -b -rkmax 4 -vxc 13 -ecut -6 -numk 100 -sp
echo -e "Ti 2 0.1 0.0\n" | init_orb_lapw -orb # Ti d U=0.1Ry J=0
echo -e "0 0 1\n\n\n\ny\ny\n100\nN\n" | init_so_lapw
runsp_lapw -so -orb -ec 0.0001 -cc 0.001
berrypi -k4:4:4 -j -o
echo "EXPECTED LAMBDA1:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [-3.539321e-10, -1.062987e-09,  4.637736e-01]
Ionic polarization (C/m2)          sp(1)  [ 0.000000e+00,  0.000000e+00, -1.760570e-01]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [-3.539321e-10, -1.062987e-09,  2.877166e-01]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [-3.539321e-10, -1.062987e-09,  2.877166e-01]
======================================================================================="
cd ../../
}

######################################################################################
# TaAs: Weyl point charge
######################################################################################
Tutorial_101 () {
echo "Running test 101"
cd tutorial5
export EDITOR=cat
cp TaAs.struct tutorial5.struct
init_lapw -b -rkmax 7 -vxc 13 -ecut -6 -numk 300
echo -e "0 0 1\n\n\n\nN\n" | init_so_lapw
run_lapw -so -ec 0.0001 -cc 0.001
cp TaAs.klist_band tutorial5.klist
berrypi -j -w -b 1:84
echo "EXPECTED OUTPUT:
'Berry phase sum (rad) =', -9.424777984529948
======================================================================================="
cd ../
}

######################################################################################
# TaAs: Weyl point charge (Wloop)
######################################################################################
Tutorial_102 () {
echo "Running test 102"
cd tutorial5
export EDITOR=cat
cp TaAs.struct tutorial5.struct
init_lapw -b -rkmax 7 -vxc 13 -ecut -6 -numk 300
echo -e "0 0 1\n\n\n\nN\n" | init_so_lapw
run_lapw -so -ec 0.0001 -cc 0.001
echo $PWD > Wloop.in
echo "91" >> Wloop.in
echo "1:84" >> Wloop.in
echo "&WloopCoordinate" >> Wloop.in
echo "0.2500 0.0000 1.0000 ; 0.2500 0.0000 0.0000" >> Wloop.in
echo "0.3000 0.0000 1.0000 ; 0.3000 0.0000 0.0000" >> Wloop.in
echo "0.2800 0.1500 1.0000 ; 0.2800 0.1500 0.0000" >> Wloop.in
echo "END" >> Wloop.in
python $BERRYPI_PATH/WloopPHI.py Wloop.in
echo "EXPECTED OUTPUT:
...
======================================================================================="
cd ../
}

######################################################################################
# BaTiO3 tutorial 1 (parallel)
######################################################################################
Tutorial_13 () {
echo "Running test 13"
cd tutorial1/lambda1
echo "1:localhost" > .machines
echo "1:localhost" >> .machines
init_lapw -b -rkmax 4 -vxc 13 -ecut -6 -numk 100
run_lapw -ec 0.0001 -cc 0.001 -p
berrypi -k4:4:4 -p
echo "EXPECTED LAMBDA1:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [-1.501550e-13, -2.089861e-13,  4.775890e-01]
Ionic polarization (C/m2)          sp(1)  [ 0.000000e+00,  0.000000e+00, -1.760570e-01]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [-1.501550e-13, -2.089861e-13,  3.015320e-01]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [-1.501550e-13, -2.089861e-13,  3.015320e-01]
======================================================================================="
cd ../../
}

######################################################################################
# spin polarized test (parallel)
######################################################################################
Tutorial_14 () {
echo "Running test 14"
cd tutorial1/lambda1
echo "1:localhost" > .machines
echo "1:localhost" >> .machines
init_lapw -b -rkmax 4 -vxc 13 -ecut -6 -numk 100 -sp
runsp_lapw -ec 0.0001 -cc 0.001 -p
berrypi -k4:4:4 -s -p
echo "EXPECTED LAMBDA1:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [ 8.750656e-14, -1.187667e-13,  2.387163e-01]
Ionic polarization (C/m2)          sp(1)  [ 0.000000e+00,  0.000000e+00, -8.802849e-02]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [ 8.750656e-14, -1.187667e-13,  1.506878e-01]
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(2)  [ 2.304258e-14,  7.144456e-14,  2.387355e-01]
Ionic polarization (C/m2)          sp(2)  [ 0.000000e+00,  0.000000e+00, -8.802849e-02]
Tot. spin polariz.=Pion+Pel (C/m2) sp(2)  [ 2.304258e-14,  7.144456e-14,  1.507070e-01]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [ 1.105491e-13, -4.732215e-14,  3.013949e-01]
======================================================================================="
cd ../../
}

######################################################################################
# SOC test (parallel)
######################################################################################
Tutorial_15 () {
echo "Running test 15"
cd tutorial1/lambda1
echo "1:localhost" > .machines
echo "1:localhost" >> .machines
export EDITOR=cat
init_lapw -b -rkmax 4 -vxc 13 -ecut -6 -numk 100
echo -e "0 0 1\n\n\n\nN\n" | init_so_lapw
run_lapw -so -ec 0.0001 -cc 0.001 -p
berrypi -k4:4:4 -j -p
echo "EXPECTED LAMBDA1:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [-6.280788e-13,  3.212734e-13,  4.776611e-01]
Ionic polarization (C/m2)          sp(1)  [ 0.000000e+00,  0.000000e+00, -1.760570e-01]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [-6.280788e-13,  3.212734e-13,  3.016041e-01]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [-6.280788e-13,  3.212734e-13,  3.016041e-01]
======================================================================================="
cd ../../
}

######################################################################################
# ORB test (parallel)
######################################################################################
Tutorial_16 () {
echo "Running test 16"
cd tutorial1/lambda1
echo "1:localhost" > .machines
echo "1:localhost" >> .machines
export EDITOR=cat
init_lapw -b -rkmax 4 -vxc 13 -ecut -6 -numk 100 -sp
echo -e "Ti 2 0.1 0.0\n" | init_orb_lapw -orb # Ti d U=0.1Ry J=0
runsp_lapw -orb -ec 0.0001 -cc 0.001 -p
berrypi -k4:4:4 -o -p
echo "EXPECTED LAMBDA1:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [ 7.114637e-14, -9.577591e-14,  2.366018e-01]
Ionic polarization (C/m2)          sp(1)  [ 0.000000e+00,  0.000000e+00, -8.802849e-02]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [ 7.114637e-14, -9.577591e-14,  1.485733e-01]
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(2)  [-9.326347e-15,  8.590123e-14,  2.366149e-01]
Ionic polarization (C/m2)          sp(2)  [ 0.000000e+00,  0.000000e+00, -8.802849e-02]
Tot. spin polariz.=Pion+Pel (C/m2) sp(2)  [-9.326347e-15,  8.590123e-14,  1.485864e-01]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [ 6.182002e-14, -9.874680e-15,  2.971597e-01]
======================================================================================="
cd ../../
}

######################################################################################
# spin polarization + SOC test (parallel)
######################################################################################
Tutorial_17 () {
echo "Running test 17"
cd tutorial1/lambda1
echo "1:localhost" > .machines
echo "1:localhost" >> .machines
export EDITOR=cat
init_lapw -b -rkmax 4 -vxc 13 -ecut -6 -numk 100 -sp
echo -e "0 0 1\n\n\n\ny\ny\n100\nN\n" | init_so_lapw
runsp_lapw -so -ec 0.0001 -cc 0.001 -p
berrypi -k4:4:4 -s -j -p
echo "EXPECTED LAMBDA1:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [-1.249460e-12,  2.728865e-13,  4.775250e-01]
Ionic polarization (C/m2)          sp(1)  [ 0.000000e+00,  0.000000e+00, -1.760570e-01]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [-1.249460e-12,  2.728865e-13,  3.014681e-01]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [-1.249460e-12,  2.728865e-13,  3.014681e-01]
======================================================================================="
cd ../../
}

######################################################################################
# SOC + ORB test DOES NOT WORK!
######################################################################################
Tutorial_18 () {
echo "Running test 18"
cd tutorial1/lambda1
echo "1:localhost" > .machines
echo "1:localhost" >> .machines
export EDITOR=cat
init_lapw -b -rkmax 4 -vxc 13 -ecut -6 -numk 100 -sp
echo -e "Ti 2 0.1 0.0\n" | init_orb_lapw -orb # Ti d U=0.1Ry J=0
echo -e "0 0 1\n\n\n\ny\ny\n100\nN\n" | init_so_lapw
runsp_lapw -so -orb -ec 0.0001 -cc 0.001 -p
berrypi -k4:4:4 -j -o -p
echo "EXPECTED LAMBDA1:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [-4.142505e-10, -1.010819e-09,  4.637736e-01]
Ionic polarization (C/m2)          sp(1)  [ 0.000000e+00,  0.000000e+00, -1.760570e-01]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [-4.142505e-10, -1.010819e-09,  2.877166e-01]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [-4.142505e-10, -1.010819e-09,  2.877166e-01]
======================================================================================="
cd ../../
}

######################################################################################
# Test BaTiO3: Lambda1 (--sp_c) spin polar. constrained (non-magnetic, up=dn) (parallel 2 cores)
######################################################################################
Tutorial_19 () {
echo "Running test 19"
cd tutorial1/lambda1
echo "1:localhost" > .machines
echo "1:localhost" >> .machines
export EDITOR=cat
instgen -nm # generate non-magnetic starting electronic config.
init_lapw -b -rkmax 4 -vxc 13 -ecut -6 -numk 100 -sp
runsp_c_lapw -ec 0.0001 -cc 0.001 -p
berrypi -k4:4:4 --sp_c -p
echo "EXPECTED LAMBDA1:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [-7.384730e-15,  1.234515e-13,  2.387169e-01]
Ionic polarization (C/m2)          sp(1)  [ 0.000000e+00,  0.000000e+00, -8.802849e-02]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [-7.384730e-15,  1.234515e-13,  1.506884e-01]
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(2)  [-7.384730e-15,  1.234515e-13,  2.387169e-01]
Ionic polarization (C/m2)          sp(2)  [ 0.000000e+00,  0.000000e+00, -8.802849e-02]
Tot. spin polariz.=Pion+Pel (C/m2) sp(2)  [-7.384730e-15,  1.234515e-13,  1.506884e-01]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [-1.476946e-14,  2.469030e-13,  3.013769e-01]
======================================================================================="
cd ../../
}

######################################################################################
# Test BaTiO3: Lambda1 (--sp_c -o) spin polar. constrained (non-magnetic, up=dn) + orb. potential + U=0.1 Ry (parallel 2 cores)
######################################################################################
Tutorial_20 () {
echo "Running test 20"
cd tutorial1/lambda1
echo "1:localhost" > .machines
echo "1:localhost" >> .machines
export EDITOR=cat
instgen -nm # generate non-magnetic starting electronic config.
init_lapw -b -rkmax 4 -vxc 13 -ecut -6 -numk 100 -sp
echo -e "Ti 2 0.1 0.0\n" | init_orb_lapw -orb # Ti d U=0.1Ry J=0
runsp_c_lapw -ec 0.0001 -cc 0.001 -orb -p
berrypi -k4:4:4 --sp_c -o -p
echo "EXPECTED LAMBDA1:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [ 2.247081e-15,  6.592793e-14,  2.365919e-01]
Ionic polarization (C/m2)          sp(1)  [ 0.000000e+00,  0.000000e+00, -8.802849e-02]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [ 2.247081e-15,  6.592793e-14,  1.485634e-01]
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(2)  [ 2.247081e-15,  6.592793e-14,  2.365919e-01]
Ionic polarization (C/m2)          sp(2)  [ 0.000000e+00,  0.000000e+00, -8.802849e-02]
Tot. spin polariz.=Pion+Pel (C/m2) sp(2)  [ 2.247081e-15,  6.592793e-14,  1.485634e-01]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [ 4.494161e-15,  1.318559e-13,  2.971269e-01]
======================================================================================="
cd ../../
}




# ceep next last line
menu
