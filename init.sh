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
	echo "Where is your BerryPI Path?"
	echo "Is this the path? $DIR"

	loopvar=1
	while [ $loopvar == 1 ]; do
		read -p "(Y/n)?" choice
		case "$choice" in
		y|Y)
			BERRYPIDIR="$DIR/berrypi"
			echo "Checking $BERRYPIDIR" 
			if [ -f $BERRYPIDIR ]; then 
				echo "BerryPI directory provided is correct" 
				echo "Continuing..."
				loopvar=0 
			else 
				echo "BerryPI directory specified is incorrect" 
			fi  
		;;
		n|N)
			while [ $loopvar == 1 ]; do 
				echo "Enter the directory where file berrypi resides: "
				read USERPATH
			

				#if [ "$USERPATH"=="q" || "$USERPATH" == "Q" ]; then #This doesn't work
				#	exit
				#fi

				BERRYPIDIR="$USERPATH/berrypi"
				if [ -f $BERRYPIDIR ]; then 
					echo "BerryPI directory provided is correct" 
					echo "Continuing..."
					loopvar=0 
				else
					echo "BerryPI directory specified is incorrect"
					echo "Format(/subdirs/berrydir) ex: /home/user/Desktop"
				
				fi

			done
		;;
		q|Q)
			exit 
		;;
		*) 
			echo "invalid command \"$choice\""
		;;
		esac
	done
}
#

#Main
get_berrypi_path













