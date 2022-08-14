#!/bin/bash

#-------- Initialisation  --------  --------  --------  --------  --------

#.. Parse arguments:
debug="false"
while getopts "d" opt; do
    case $opt in
	d) debug="true" ;;
    esac
done

#.. Set environment variables:
HOMEPATH=$PWD
if [ $debug == "true" ]; then
    echo "Bragg-peak code run from directory:"
    echo "    " $HOMEPATH
fi
export HOMEPATH

SOURCE=${BASH_SOURCE[0]}
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR=$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )
  SOURCE=$(readlink "$SOURCE")
  [[ $SOURCE != /* ]] && SOURCE=$DIR/$SOURCE 
done
SCRIPT_DIR=$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )

BraggPATH=$SCRIPT_DIR
if [ $debug == "true" ]; then
    echo "Bragg path set:"
    echo "    " $BraggPATH
fi
export BraggPATH

add="/01-Code"
dir="$BraggPATH$add"
if [ -z ${PYTHONPATH+x} ]; then
    PYTHONPATH=":$dir"
else
    PYTHONPATH="${PYTHONPATH}:$dir"
fi
if [ $debug == "true" ]; then
    echo "Python path set:"
    echo "    " $PYTHONPATH
fi
export PYTHONPATH

add="/99-Scratch"
REPORTPATH="$HOMEPATH$add"
if [ $debug == "true" ]; then
    echo "Reports path set:"
    echo "    " $REPORTPATH
fi
export REPORTPATH
