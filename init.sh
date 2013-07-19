#!/bin/bash


#Intialization

#Global Variables
BERRYPIDIR=""
PYTHONDIR= "/local/bin/python2.7"
SOURCE=""
DIR=""
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
echo "Python Version: $PYTHONVER"
echo "######################################################################"
#

#Procedures
get_berrypi_path()
{
	loopvar=1
	BERRYPIDIR="$DIR/berrypi" #Check to see if this is the default directory
	if [ -f $BERRYPIDIR ]; then
		echo "BerryPI directory found"
		echo "Continuing..."
		loopvar=0
	else
		echo "Where is your BerryPI Path?"

		while [ $loopvar == 1 ]; do 
			echo "Enter the directory where file berrypi resides: "
			read USERPATH
	
			BERRYPIDIR="$USERPATH/berrypi"
			if [ -f $BERRYPIDIR ]; then 
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
	pyexist=false
	#linux command type
	# >/dev/null 2>&1 to mask the string that type echos 
	type python2.7 >/dev/null 2>&1 || { local pyexist=false; echo >&2 "I require python 2.7 but it's not installed.";}
	
	if [ $pyexist == true ]; then
		loopvar=1
		if [ -f "/usr/bin/python2.7" ]; then
			echo "Python 2.7 directory found"
			echo "Continuing..."
		else
			while [ $loopvar == 1 ]; do 
				echo "Enter the directory where python2.7 resides: "
				read USERPATH
	
				PYTHONDIR="$USERPATH/python2.7"
				if [ -f $PYTHONDIR ]; then 
					echo "Python 2.7 directory provided is correct" 
					echo "Continuing..."
					loopvar=0 
				else
					echo "Python 2.7 directory specified is incorrect"
					echo "Format(/subdir/pythondir) ex: /home/user/Desktop"
		
				fi
			done	
		fi
	else
		echo "Would you like to attempt to install Python 2.7?"
		
		read -p "(Y/n)?" choice
  		case "$choice" in
  		y|Y) 
			sudo apt-get install python2.7 #May not work on all linux distros but hopefully all debian distros
			if [ -f "/usr/bin/python2.7" ]; then
				echo "Python 2.7 directory found"
				echo "Continuing..."
			else
				echo "Python 2.7 directory not found"
				#TODO allow user to look and provide path if their system installed python else where
			fi
		else	
		;;
		n|N)
			echo "BerryPI initialization can not continue"
			echo "Aborted"
			exit 1	
		;;
		esac
	fi 
}

#

#Main
get_berrypi_path
get_python_path












