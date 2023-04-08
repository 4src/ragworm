#!/bin/bash
if [ "$#" -ne 1 ]
then python3 -B tests.py $1.py
else python3 -B tests.py $*
fi
