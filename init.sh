#!/bin/bash

#TODO figure out how to install missing packages across multiple platforms (e.g apt-get, yum, ...)

#Intialization

#Global Variables
BERRYPIDIR=""
PYTHONDIR= "/local/bin/python2.7"
SOURCE=""
DIR=""
iswget=true
iscurl=true			
#
clear
echo "######################################################################"
PYTHONVER=$(python -c 'import sys; print ".".join(map(str,sys.version_info[:3]))')
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
	TARGET="$(readlink "$SOURCE")"
	if [[ $SOURCE == /* ]]; then
		echo "SOURCE '$SOURCE' is an absolute symlink to '$TARGET'"
		SOURCE="$TARGET"
	else
		DIR="$( dirname "$SOURCE" )"
		echo "SOURCE '$SOURCE' is a relative symlink to '$TARGET' (relative to '$DIR')"
		SOURCE="$DIR/$TARGET" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
	fi
done

echo "SOURCE: '$SOURCE'"
RDIR="$( dirname "$SOURCE" )"
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
if [ "$DIR" != "$RDIR" ]; then
	echo "DIR: '$RDIR' resolves to '$DIR'"
fi
echo "DIR: '$DIR'"
echo "Python Version initially found: $PYTHONVER"

WIENVAR=1
W2WVAR=1


$WIENROOT >/dev/null 2>&1
WIENVAR=$?
$W2WROOT >/dev/null 2>&1
W2WVAR=$?


if [ $WIENVAR == 126 ]; then
	echo "WIEN2k detected"
else
	which WIEN2K >/dev/null 2>&1 #second attempt to atleast find any aknowledgement of WEIN2K
	if [ $? == 0 ]; then
		echo "WIEN2k detected"
	else
		echo "WIEN2K not detected. BerryPI will not run without WIEN2K."
		echo "Initialization aborted"
		exit 1
	fi
	
fi

if [ $W2WVAR == 126 ]; then
	echo "W2WANNIER detected"
else
	which w2w 
	if [ $? == 0 ]; then
		echo "w2w detected"
	else
		echo "w2w not detected. BerryPI will not run without W2WANNIER."
		echo "Initialization aborted"
		exit 1
	fi
fi

type wget >/dev/null 2>&1 ||{ iswget=false; }
type curl >/dev/null 2>&1 ||{ iscurl=false; }

if [ $iswget ]; then
	echo "Installation via wget available"
elif [ $iscurl  ]; then
	echo "Installation via curl available"
else
	echo "wget and curl not available."
	echo "If missing Python2.7 or NumPy 1.6.2."
	echo "This script will be unable to download and install them" 
fi
echo "######################################################################"
#

#Functions
get_berrypi_path()
{
	loopvar=1
	BERRYPIDIR="$DIR" #Check to see if this is the default directory
	if [ -f "$BERRYPIDIR/berrypi" ]; then
		echo "BerryPI directory found"
		echo "Continuing..."
		loopvar=0
	else
		echo "Where is your BerryPI Path?"

		while [ $loopvar == 1 ]; do 
			echo "Enter the directory where file berrypi resides: "
			read USERPATH
	
			BERRYPIDIR="$USERPATH"
			if [ -f "$BERRYPIDIR/berrypi" ]; then 
				echo "BerryPI directory provided is correct" 
				echo "Continuing..."
				loopvar=0 
			else
				echo "BerryPI directory specified is incorrect"
				echo "Format(/subdir/berrydir) ex: /home/user/Desktop"
			fi
		done	
	fi
}

get_python_path()
{
	pyexist=true
	islocal=true
	isbin=true
	# >/dev/null 2>&1 to mask the string that type echos 
	type python2.7 >/dev/null 2>&1 || { pyexist=false;}
	
	if ! [  -f "$HOME/.local/bin/python2.7" ]; then
		islocal=false	
	fi

	if ! [ -f "/usr/bin/python2.7" ]; then
		isbin=false
	fi
	
	if $pyexist || $islocal || $isbin ;then
		loopvar=1
		
		if [ -f "$HOME/.local/bin/python2.7" ]; then
			PYTHONDIR="$HOME/.local/bin/python2.7"
			echo "Python 2.7 directory found"
			echo "Continuing..."
		elif [ -f "/usr/bin/python2.7" ];then
			PYTHONDIR="/usr/bin/python2.7"
			echo "Python 2.7 directory found"
			echo "Continuing..."
		else
			while [ $loopvar == 1 ]; do 
				echo "Enter the directory where python2.7 resides: "
				which python
				read USERPATH
	
				PYTHONDIR="$USERPATH/python2.7"
				if [ -f $PYTHONDIR ]; then 
					echo "Python 2.7 directory provided is correct" 
					echo "Continuing..."
					loopvar=0 
				else
					echo "Python 2.7 directory specified is incorrect"
					echo "Format(/subdir/pythondir/python) ex: /usr/bin/python2.7"
		
				fi
			done	
		fi
	else
		echo "Would you like to attempt to install Python 2.7?"
		
		read -p "(Y/n)?" choice
  		case "$choice" in
  		y|Y) 
			
			isinstall=true
			mkdir ''$HOME'/.local/' >/dev/null 2>&1
			cd ''$HOME'/.local/'
			
			if [ $iswget ]; then
				wget 'http://www.python.org/ftp/python/2.7.4/Python-2.7.4.tar.bz2'
			elif [ $iscurl ]; then
				curl -O 'http://www.python.org/ftp/python/2.7.4/Python-2.7.4.tar.bz2'
			else
				isinstall=false
			fi
			
			if [ $isinstall ]; then
				tar -xjf 'Python-2.7.4.tar.bz2'
				cd 'Python-2.7.4'
				make clean
				./configure --prefix=''$HOME'/.local'
				make
				make install
				cd ..
				rm 'Python-2.7.4.tar.bz2'
				rm -R 'Python-2.7.4'
			fi
			

			if [ -f "$HOME/.local/bin/python2.7" ];then
				PYTHONDIR="$HOME/.local/bin/python2.7"
				echo "Python 2.7 directory found"
				echo "Continuing..."
			else
				echo "Python 2.7 directory not found"
				echo "BerryPI initialization can not continue"
				echo "Aborted"
				exit 1	
			fi
		;;
		n|N)
			echo "BerryPI initialization can not continue"
			echo "Aborted"
			exit 1	
		;;
		esac
	fi 
}

check_numpy_exists()
{
	numpyver=$($PYTHONDIR -c 'import numpy; print numpy.__version__')  
	if [ "$numpyver" == "1.6.2" ];then
		echo "A NumPy 1.6.2 directory exists"
		echo "Continuing..."
	else
		echo "No NumPy directory found"
		echo "BerryPI will fail to run without NumPy"
		echo "Would you like to attempt to install NumPy?"
	
		read -p "(Y/n)?" choice
  		case "$choice" in
  		y|Y) 
			
			isinstall=true
			mkdir ''$HOME'/.local/' >/dev/null 2>&1
			cd ''$HOME'/.local/'

			if [ $iswget ]; then
				wget 'sourceforge.net/projects/numpy/files/NumPy/1.6.2/numpy-1.6.2.tar.gz/download'
			elif [ $iscurl ]; then
				curl -O 'sourceforge.net/projects/numpy/files/NumPy/1.6.2/numpy-1.6.2.tar.gz/download'
			else
				isinstall=false
			fi
			
			if [ $isinstall ]; then
				tar -xzvf 'numpy-1.6.2.tar.gz'
				cd 'numpy-1.6.2'
				$PYTHONDIR 'setup.py' install --prefix=''$HOME'/.local/'
				cd ..
				rm 'numpy-1.6.2.tar.gz'
				rm -R 'numpy-1.6.2'
			fi
			
			numpyver=$($PYTHONDIR -c 'import numpy; print numpy.__version__' ) 
			if [ '$numpyver' == '1.6.2' ];then
				echo "A NumPy 1.6.2 directory exists"
				echo "Continuing..."
			else
				echo "NumPy was unable to be intalled"
				#Restart script as numPy sometimes doesn't want to be detected until the script restarts
				cd "$DIR"
				bash 'init.sh'
				exit 1
				
			fi
		;;
		n|N)
			echo "BerryPI initialization can not continue"
			echo "Aborted"
			exit 1	
		;;
		esac

	fi
}
#END FUNCTIONS

#Main
get_berrypi_path
get_python_path
check_numpy_exists

echo "Initialization finished"
echo "Updating Config.py"

file="$BERRYPIDIR/config.py"

if [ -f "$file" ]; then
	loopvar=1
	linenum=0
	incval=1
	while IFS= read -r line
	do	
		linenum=$(( $linenum + $incval ))

		if [[ "$line" == *"DEFAULT_BIN_PATH="* ]];then
			NEW="DEFAULT_BIN_PATH='$BERRYPIDIR/'"
			sed -i ''$linenum' c\'$NEW'' $file
			
		fi

		if [[ "$line" == *"DEFAULT_PYTHON_PATH="* ]];then
			NEW="DEFAULT_PYTHON_PATH='$PYTHONDIR'"
			sed -i ''$linenum' c\'$NEW'' $file
			
		fi
	done <"$file"
fi

file="$HOME/.bashrc"
echo "Updating '$file'"
ispaths=0
if [ -f "$file" ]; then
	loopvar=1
	linenum=0
	incval=1
	while IFS= read -r line
	do	
		linenum=$(( $linenum + $incval ))

		if [[ "$line" == *"# --- BERRYPI START ---"* ]];then
			ispaths=1
			sed -i ''$(( $linenum + $incval ))' c\''export BERRYPI_PATH='$BERRYPIDIR'' $file
			sed -i ''$(( $linenum + $incval + $incval ))' c\''export BERRYPI_PYTHON='$PYTHONDIR'' $file
			sed -i ''$(( $linenum + $incval + $incval + $incval ))' c\''alias berrypi="${BERRYPI_PYTHON} ${BERRYPI_PATH}/berrypi"' $file
		fi

	done <"$file"
fi


if [ $ispaths == 0 ]; then
	echo '# --- BERRYPI START ---' >> $file
	echo 'export BERRYPI_PATH='$BERRYPIDIR'' >> $file
	echo 'export BERRYPI_PYTHON='$PYTHONDIR'' >> $file
	echo 'alias berrypi="${BERRYPI_PYTHON} ${BERRYPI_PATH}/berrypi"' >> $file
	echo '# --- BERRYPI END ---' >> $file
fi 

source "$HOME/.bashrc"

