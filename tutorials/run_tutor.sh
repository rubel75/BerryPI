#!/bin/bash 
#
# execution: $ source run_tutor
#
# Developed by Anton Bokhanchuk

clear
echo "######################################################"
echo "Type the test number and press ENTER to run that test:"
echo "1 - Tutorial 1: Lambda1 and Lambda0"
echo "2 - Tutorial 2: Lambda1 and Lambda2"
echo "3 - Tutorial 3: GaAs1 and GaAs2"
echo "4 - Tutorial 4: GaN-W and GaN-ZB"
echo "5 - All Tests"
echo "6 - Clean All"
echo ""
echo "T E S T S (serial):"
echo "7 - Test BaTiO3: Lambda1"
echo "8 - Test BaTiO3: Lambda1 (-s) spin polarization"
echo "9 - Test BaTiO3: Lambda1 (-j) spin orbit"
echo "10 - Test BaTiO3: Lambda1 (-o) orb. potential + U=0.1 Ry (spin polarization implied)"
echo "11 - Test BaTiO3: Lambda1 (-s -j) spin polarization & SOC"
echo "12 - Test BaTiO3: Lambda1 (-o -j) SOC & orb. potential + U=0.1 Ry (spin polarization implied) DOES NOT WORK!"
echo ""
echo "T E S T S (parallel):"
echo "13 - Test BaTiO3: Lambda1 (-p) spin polarization (parallel 2 cores)"
echo "14 - Test BaTiO3: Lambda1 (-s -p) spin polarization (parallel 2 cores)"
echo "15 - Test BaTiO3: Lambda1 (-j) spin orbit (parallel 2 cores)"
echo "16 - Test BaTiO3: Lambda1 (-o) orb. potential + U=0.1 Ry (spin polarization implied) (parallel 2 cores)"
echo "17 - Test BaTiO3: Lambda1 (-s -j) spin polarization & SOC (parallel 2 cores)"
echo "18 - Test BaTiO3: Lambda1 (-o -j) SOC & orb. potential + U=0.1 Ry (spin polarization implied) (parallel 2 cores) DOES NOT WORK!"
echo "######################################################"
read choice

menu() {

case "$choice" in
	1)
	  echo "Running Tutorial 1"
	  flag=0
	  while [ "$flag" == "0" ]; do
	  echo "Would you like to clean the tutotial directory (y/n)?"
	  read opt
	    if [ "$opt" == "y" ] || [ "$opt" == "Y" ]; then
		  CleanTut_1
		  flag=1
	    elif [ "$opt" == "n" ] || [ "$opt" == "N" ]; then
	         echo "No files were removed!"
		  flag=1
	    else
		  echo "Unknown option!"
	    fi
	  done
	  Tutorial_1
	  ;;
	2)
	  echo "Running Tutorial 2"
	  flag=0
	  while [ "$flag" == "0" ]; do
	  echo "Would you like to clean the tutotial directory (y/n)?"
	  read opt
	    if [ "$opt" == "y" ] || [ "$opt" == "Y" ]; then
		  CleanTut_2
		  flag=1
	    elif [ "$opt" == "n" ] || [ "$opt" == "N" ]; then
	         echo "No files were removed!"
		  flag=1
	    else
		  echo "Unknown option!"
	    fi
	  done
	  Tutorial_2
	  ;;
	3)
	  echo "Running Tutorial 3"
	  flag=0
	  while [ "$flag" == "0" ]; do
	  echo "Would you like to clean the tutotial directory (y/n)?"
	  read opt
	    if [ "$opt" == "y" ] || [ "$opt" == "Y" ]; then
		  CleanTut_3
		  flag=1
	    elif [ "$opt" == "n" ] || [ "$opt" == "N" ]; then
	         echo "No files were removed!"
		  flag=1
	    else
		  echo "Unknown option!"
	    fi
	  done
	  Tutorial_3
	  ;;
	4)
	  echo "Running Tutorial 4"
	  flag=0
	  while [ "$flag" == "0" ]; do
	  echo "Would you like to clean the tutotial directory (y/n)?"
	  read opt
	    if [ "$opt" == "y" ] || [ "$opt" == "Y" ]; then
		  CleanTut_4
		  flag=1
	    elif [ "$opt" == "n" ] || [ "$opt" == "N" ]; then
	         echo "No files were removed!"
		  flag=1
	    else
		  echo "Unknown option!"
	    fi
	  done
	  Tutorial_4
	  ;;
	5) 
	  echo "Running ALL test"
	  flag=0
	  while [ "$flag" == "0" ]; do
	  echo "Would you like to clean the tutotial directory (y/n)?"
	  read opt
	    if [ "$opt" == "y" ] || [ "$opt" == "Y" ]; then
		  CleanTut_1
		  CleanTut_2
		  CleanTut_3
		  CleanTut_4
		  flag=1
	    elif [ "$opt" == "n" ] || [ "$opt" == "N" ]; then
	         echo "No files were removed!"
		  flag=1
	    else
		  echo "Unknown option!"
	    fi
	  done
	  Tutorial_1
	  Tutorial_2
	  Tutorial_3
	  Tutorial_4
	  ;;
	6)
	  echo "Cleaning up all files"
	  CleanTut_1
	  CleanTut_2
	  CleanTut_3
	  CleanTut_4
	  rm -rf Summary.out
	  ;;
	7)
	  echo "Running test 7"
      CleanTut_1
	  Tutorial_7
	  ;;
    8)
	  echo "Running test 8"
      CleanTut_1
	  Tutorial_8
	  ;;
    9)
	  echo "Running test 9"
      CleanTut_1
	  Tutorial_9
	  ;;
    10)
	  echo "Running test 10"
      CleanTut_1
	  Tutorial_10
	  ;;
    11)
	  echo "Running test 11"
      CleanTut_1
	  Tutorial_11
	  ;;
    12)
	  echo "Running test 12"
      CleanTut_1
	  Tutorial_12
	  ;;
    13)
	  echo "Running test 13"
      CleanTut_1
	  Tutorial_13
	  ;;
    14)
	  echo "Running test 14"
      CleanTut_1
	  Tutorial_14
	  ;;
    15)
	  echo "Running test 15"
      CleanTut_1
	  Tutorial_15
	  ;;
    16)
	  echo "Running test 16"
      CleanTut_1
	  Tutorial_16
	  ;;
    17)
	  echo "Running test 17"
      CleanTut_1
	  Tutorial_17
	  ;;
    18)
	  echo "Running test 18"
      CleanTut_1
	  Tutorial_18
	  ;;
	*)
	  echo "Unknown option"
esac
}

CleanTut_1 () {
	cd tutorial1
	rm -rf Tutorial1_1.out Tutorial1_2.out
	cd lambda1
	ls -1 | grep -v 'lambda1.struct$' | xargs rm -f
       cd ../lambda0
	ls -1 | grep -v 'lambda0.struct$' | xargs rm -f
	cd ../../
	echo "All files but lambda1.struct and lambda0.struct were removed!"
}

CleanTut_2 () {
	cd tutorial2
	rm -rf Tutorial2_1.out Tutorial2_2.out
	cd lambda1
	ls -1 | grep -v 'lambda1.struct$' | xargs rm -f
       cd ../lambda2
	ls -1 | grep -v 'lambda2.struct$' | xargs rm -f
	cd ../../
	echo "All files but lambda1.struct and lambda2.struct were removed!"
}

CleanTut_3 () {
	cd tutorial3
	rm -rf Tutorial3_1.out Tutorial3_2.out
	cd GaAs1
	ls -1 | grep -v 'GaAs1.struct$' | xargs rm -f
       cd ../GaAs2
	ls -1 | grep -v 'GaAs2.struct$' | xargs rm -f
	cd ../../
	echo "All files but GaAs1.struct and GaAs2.struct were removed!"
}

CleanTut_4 () {
	cd tutorial4
	rm -rf Tutorial4_1.out Tutorial4_2.out
	cd GaN-W
	ls -1 | grep -v 'GaN-W.struct$' | xargs rm -f
       cd ../GaN-ZB
	ls -1 | grep -v 'GaN-ZB.struct$' | xargs rm -f
	cd ../../
	echo "All files but GaN-W.struct and GaN-ZB.struct were removed!"
}

Tutorial_1 () {
starttime=$(date +%s)
cd tutorial1/lambda1
init_lapw -b -rkmax 4 -vxc 13 -ecut -6 -numk 230 2>&1 | tee ../Tutorial1_1.out
run_lapw 2>&1 | tee -a ../Tutorial1_1.out
echo "TUTORIAL 1 SUMMARY: " >> ../../Summary.out
echo "" >> ../../Summary.out
echo "EXPECTED LAMBDA1:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [-8.711747e-12, -8.368475e-13,  4.803326e-01]
Ionic polarization (C/m2)          sp(1)  [ 1.365657e-11,  1.365657e-11, -1.760570e-01]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [ 4.944823e-12,  1.281972e-11,  3.042756e-01]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [ 4.944823e-12,  1.281972e-11,  3.042756e-01]
=======================================================================================" >> ../../Summary.out
berrypi -k6:6:6 2>&1 | tee -a ../Tutorial1_1.out
endtime=$(date +%s)
echo "Time elapsed: $((endtime-starttime))sec" >> ../Tutorial1_1.out 
echo ""  >> ../../Summary.out
echo "OBTAINED LAMBDA1:" >> ../../Summary.out
while read line 
do
    if [ "$line" == "SUMMARY OF POLARIZATION CALCULATION" ]; then
        for i in {1..9}
        do
            read line
            echo "$line" >> ../../Summary.out
        done
        break
    fi
done < ../Tutorial1_1.out
echo ""  >> ../../Summary.out
starttime=$(date +%s)
cp * ../lambda0
cd ../lambda0
rm lambda1.struct
rename_files lambda1 lambda0
x kgen <<EOF 2>&1 | tee ../Tutorial1_2.out
  230
  1
EOF
x dstart 2>&1 | tee -a ../Tutorial1_2.out
run_lapw 2>&1 | tee -a ../Tutorial1_2.out
echo "EXPECTED LAMBDA0:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [ 1.164531e-13,  1.338068e-13, -2.574002e-13]
Ionic polarization (C/m2)          sp(1)  [ 1.365657e-11,  1.365657e-11,  1.380018e-11]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [ 1.377302e-11,  1.379038e-11,  1.354278e-11]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [ 1.377302e-11,  1.379038e-11,  1.354278e-11]
=======================================================================================" >> ../../Summary.out
berrypi -k6:6:6 2>&1 | tee -a ../Tutorial1_2.out
echo ""  >> ../../Summary.out
echo "OBTAINED LAMBDA0:"  >> ../../Summary.out
while read line 
do
    if [ "$line" == "SUMMARY OF POLARIZATION CALCULATION" ]; then
        for i in {1..9}
        do
            read line
            echo "$line" >> ../../Summary.out
        done
        break
    fi
done < ../Tutorial1_2.out
echo ""  >> ../../Summary.out
endtime=$(date +%s)
echo "Time elapsed: $((endtime-starttime))sec" >> ../Tutorial1_2.out
cd ../../
}

Tutorial_2 () {
starttime=$(date +%s)
cd tutorial2/lambda1
init_lapw -b -rkmax 4 -vxc 13 -ecut -6 -numk 230 2>&1 | tee ../Tutorial2_1.out
run_lapw 2>&1 | tee -a ../Tutorial2_1.out
echo "TUTORIAL 2 SUMMARY: " >> ../../Summary.out
echo "" >> ../../Summary.out
echo "EXPECTED LAMBDA1:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [-4.863642e-11,  3.049161e-10, -8.357582e-02]
Ionic polarization (C/m2)          sp(1)  [ 2.855857e-10,  2.855857e-10,  7.301465e-02]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [ 2.369493e-10,  5.905018e-10, -1.056116e-02]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [ 2.369493e-10,  5.905018e-10, -1.056116e-02]
=======================================================================================" >> ../../Summary.out
echo "" >> ../../Summary.out
berrypi -k6:6:6 2>&1 | tee -a ../Tutorial2_1.out
echo ""  >> ../../Summary.out
echo "OBTAINED LAMBDA1:"  >> ../../Summary.out
while read line 
do
    if [ "$line" == "SUMMARY OF POLARIZATION CALCULATION" ]; then
        for i in {1..9}
        do
            read line
            echo "$line" >> ../../Summary.out
        done
        break
    fi
done < ../Tutorial2_1.out
echo ""  >> ../../Summary.out
endtime=$(date +%s)
echo "Time elapsed: $((endtime-starttime))sec" >> ../Tutorial2_1.out
starttime=$(date +%s)
cp * ../lambda2
cd ../lambda2
rm lambda1.struct
rename_files lambda1 lambda2
x kgen <<EOF 2>&1 | tee ../Tutorial2_2.out
  230
  1
EOF
x dstart 2>&1 | tee -a ../Tutorial2_2.out
run_lapw 2>&1 | tee -a ../Tutorial2_2.out
echo "EXPECTED LAMBDA2:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [ 1.870846e-10,  2.625904e-10,  8.357696e-02]
Ionic polarization (C/m2)          sp(1)  [ 2.855857e-10,  2.855857e-10, -7.301465e-02]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [ 4.726703e-10,  5.481761e-10,  1.056231e-02]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [ 4.726703e-10,  5.481761e-10,  1.056231e-02]
=======================================================================================" >> ../../Summary.out
echo "" >> ../../Summary.out
berrypi -k6:6:6 2>&1 | tee -a ../Tutorial2_2.out
echo ""  >> ../../Summary.out
echo "OBTAINED LAMBDA2:"  >> ../../Summary.out
while read line 
do
    if [ "$line" == "SUMMARY OF POLARIZATION CALCULATION" ]; then
        for i in {1..9}
        do
            read line
            echo "$line" >> ../../Summary.out
        done
        break
    fi
done < ../Tutorial2_2.out
echo ""  >> ../../Summary.out
endtime=$(date +%s)
echo "Time elapsed: $((endtime-starttime))sec" >> ../Tutorial2_2.out
cd ../../
}

Tutorial_3 () {
starttime=$(date +%s)
cd tutorial3/GaAs1
linenr=$(grep -n -m 1 "ATOM  -2: X=0.25000000 Y=0.25000000 Z=0.25100000" GaAs1.struct | cut -d':' -f1)
sed -i "${linenr}d" GaAs1.struct
sed -i "${linenr}i\ATOM  -2: X=0.25100000 Y=0.25200000 Z=0.25300000" GaAs1.struct
init_lapw -b -vxc 5 -rkmax 4 -numk 800 2>&1 | tee ../Tutorial3_1.out
linenr=$(grep -n -m 1 "ATOM  -2: X=0.25100000 Y=0.25200000 Z=0.25300000" GaAs1.struct | cut -d':' -f1)
sed -i "${linenr}d" GaAs1.struct
sed -i "${linenr}i\ATOM  -2: X=0.25000000 Y=0.25000000 Z=0.25100000" GaAs1.struct
x dstart 2>&1 | tee -a ../Tutorial3_1.out
run_lapw 2>&1 | tee -a ../Tutorial3_1.out
echo "TUTORIAL 3 SUMMARY: " >> ../../Summary.out
echo "" >> ../../Summary.out
echo "EXPECTED GaAs1:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [ 9.769755e-01,  9.769755e-01, -9.593836e-01]
Ionic polarization (C/m2)          sp(1)  [-5.013188e-01, -5.013188e-01, -4.712397e-01]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [ 4.756567e-01,  4.756567e-01, -1.430623e+00]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [ 4.756567e-01,  4.756567e-01, -1.430623e+00]
=======================================================================================" >> ../../Summary.out
berrypi -k 6:6:6 2>&1 | tee -a ../Tutorial3_1.out
endtime=$(date +%s)
echo "Time elapsed: $((endtime-starttime))sec" >> ../Tutorial3_1.out 
echo ""  >> ../../Summary.out
echo "OBTAINED GaAs1:" >> ../../Summary.out
while read line 
do
    if [ "$line" == "SUMMARY OF POLARIZATION CALCULATION" ]; then
        for i in {1..9}
        do
            read line
            echo "$line" >> ../../Summary.out
        done
        break
    fi
done < ../Tutorial3_1.out
echo ""  >> ../../Summary.out
starttime=$(date +%s)
cp * ../GaAs2
cd ../GaAs2
rename_files GaAs1 GaAs2
linenr=$(grep -n -m 1 "ATOM  -2: X=0.25000000 Y=0.25000000 Z=0.25100000" GaAs2.struct | cut -d':' -f1)
sed -i "${linenr}d" GaAs2.struct
sed -i "${linenr}i\ATOM  -2: X=0.25000000 Y=0.25000000 Z=0.24900000" GaAs2.struct
x kgen <<EOF 2>&1 | tee ../Tutorial3_2.out
  800
  1
EOF
x dstart 2>&1 | tee -a ../Tutorial3_2.out
rm *scf
run_lapw 2>&1 | tee -a ../Tutorial3_2.out
echo "EXPECTED GaAs2:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [-9.593715e-01, -9.593715e-01,  9.769706e-01]
Ionic polarization (C/m2)          sp(1)  [-5.013188e-01, -5.013188e-01, -5.313979e-01]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [-1.460690e+00, -1.460690e+00,  4.455726e-01]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [-1.460690e+00, -1.460690e+00,  4.455726e-01]
=======================================================================================" >> ../../Summary.out
berrypi -k 6:6:6 2>&1 | tee -a ../Tutorial3_2.out
echo ""  >> ../../Summary.out
echo "OBTAINED GaAs2:"  >> ../../Summary.out
while read line 
do
    if [ "$line" == "SUMMARY OF POLARIZATION CALCULATION" ]; then
        for i in {1..9}
        do
            read line
            echo "$line" >> ../../Summary.out
        done
        break
    fi
done < ../Tutorial3_2.out
echo ""  >> ../../Summary.out
endtime=$(date +%s)
echo "Time elapsed: $((endtime-starttime))sec" >> ../Tutorial3_2.out
cd ../../
}

Tutorial_4 () {
starttime=$(date +%s)
cd tutorial4/GaN-W
init_lapw -b -vxc 5 -rkmax 7 -numk 300 2>&1 | tee ../Tutorial4_1.out
run_lapw 2>&1 | tee -a ../Tutorial4_1.out
echo "TUTORIAL 4 SUMMARY: " >> ../../Summary.out
echo "" >> ../../Summary.out
echo "EXPECTED GaN-W:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [ 2.223396e-10,  1.205149e-07, -5.612307e-02]
Ionic polarization (C/m2)          sp(1)  [ 1.750356e-10, -2.049427e-07, -4.386009e-01]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [ 3.973752e-10, -8.442784e-08, -4.947239e-01]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [ 3.973752e-10, -8.442784e-08, -4.947239e-01]
=======================================================================================" >> ../../Summary.out
berrypi -k 8:8:8 2>&1 | tee -a ../Tutorial4_1.out
endtime=$(date +%s)
echo "Time elapsed: $((endtime-starttime))sec" >> ../Tutorial4_1.out 
echo ""  >> ../../Summary.out
echo "OBTAINED GaN-W:" >> ../../Summary.out
while read line 
do
    if [ "$line" == "SUMMARY OF POLARIZATION CALCULATION" ]; then
        for i in {1..9}
        do
            read line
            echo "$line" >> ../../Summary.out
        done
        break
    fi
done < ../Tutorial4_1.out
echo ""  >> ../../Summary.out
starttime=$(date +%s)
cd ../GaN-ZB
init_lapw -b -vxc 5 -rkmax 7 -numk 200 2>&1 | tee -a ../Tutorial4_2.out
run_lapw 2>&1 | tee -a ../Tutorial4_2.out
echo "EXPECTED GaN-ZB:
=======================================================================================
Value                           |  spin   |    dir(1)    |    dir(2)    |    dir(3)
---------------------------------------------------------------------------------------
Electronic polarization (C/m2)     sp(1)  [-1.219101e-03,  1.219101e-03, -1.727041e-04]
Ionic polarization (C/m2)          sp(1)  [ 1.165061e-10,  1.165088e-10, -4.644818e-01]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [-1.219101e-03,  1.219101e-03, -4.646545e-01]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [-1.219101e-03,  1.219101e-03, -4.646545e-01]
=======================================================================================" >> ../../Summary.out
berrypi -k 8:8:8 2>&1 | tee -a ../Tutorial4_2.out
echo ""  >> ../../Summary.out
echo "OBTAINED GaN_ZB:"  >> ../../Summary.out
while read line 
do
    if [ "$line" == "SUMMARY OF POLARIZATION CALCULATION" ]; then
        for i in {1..9}
        do
            read line
            echo "$line" >> ../../Summary.out
        done
        break
    fi
done < ../Tutorial4_2.out
echo ""  >> ../../Summary.out
endtime=$(date +%s)
echo "Time elapsed: $((endtime-starttime))sec" >> ../Tutorial4_2.out
cd ../../
}

######################################################################################
# simplest test
######################################################################################
Tutorial_7 () {
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
# SOC + ORB test DOES NOT WORK!
######################################################################################
Tutorial_12 () {
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
Electronic polarization (C/m2)     sp(1)  [ 5.395795e-12,  8.790106e-12,  4.811830e-01]
Ionic polarization (C/m2)          sp(1)  [ 0.000000e+00,  0.000000e+00, -1.760570e-01]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [ 5.395795e-12,  8.790106e-12,  3.051260e-01]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [ 5.395795e-12,  8.790106e-12,  3.051260e-01]
======================================================================================="
cd ../../
}

######################################################################################
# BaTiO3 tutorial 1 (parallel)
######################################################################################
Tutorial_13 () {
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
Electronic polarization (C/m2)     sp(1)  [ 5.395795e-12,  8.790106e-12,  4.811830e-01]
Ionic polarization (C/m2)          sp(1)  [ 0.000000e+00,  0.000000e+00, -1.760570e-01]
Tot. spin polariz.=Pion+Pel (C/m2) sp(1)  [ 5.395795e-12,  8.790106e-12,  3.051260e-01]
---------------------------------------------------------------------------------------
TOTAL POLARIZATION (C/m2)          both   [ 5.395795e-12,  8.790106e-12,  3.051260e-01]
======================================================================================="
cd ../../
}

# ceep next last line
menu