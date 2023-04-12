#!/bin/sh

set -e


echo "#######################"
echo "Connecting DB"
echo "#######################"

python ./prestart/check_connection.py


# Evaluating passed command:
exec "$@"
