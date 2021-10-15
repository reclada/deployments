#!/bin/bash
pushd "$(dirname ${BASH_SOURCE:0})"
python3 install.py $1

