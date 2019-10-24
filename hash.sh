#!/bin/bash


## Argument reference:
# $# --> number of arguments in our script
# $0 --> the filename of our script
# $1..$n --> scripts argumens

# example: echo "We have ${#} number of arguments"


## Program:

sha=`curl -s $1 | sha256sum`
echo $sha:$1



