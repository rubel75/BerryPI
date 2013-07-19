#!/bin/bash


#Intialization

#Global Variables
BERRYPIDIR=""
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
#

#Main
get_berrypi_path













