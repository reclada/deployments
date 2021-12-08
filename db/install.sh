#!/bin/bash
pushd "$(dirname ${BASH_SOURCE:0})"

if test "$1" = "install"
then
    python3 install_db.py $2
elif test "$1" = "update"
    python3 update_db.py
else
    echo "unknown command"
fi