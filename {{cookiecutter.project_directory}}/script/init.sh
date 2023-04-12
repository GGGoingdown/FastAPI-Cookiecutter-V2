#!/bin/sh

set -e


echo "#######################"
echo "Connecting DB"
echo "#######################"

python ./prestart/check_connection.py

# Environment
echo "###########################################################"
echo "MIGRATION: ${MIGRATION}"
echo "CREATE_INIT_DATA: ${CREATE_INIT_DATA}"
echo "###########################################################"

if [ "$MIGRATION" = "true" ]; then
    echo "Doing db migration"
    aerich upgrade
fi

if [ "$CREATE_INIT_DATA" = "true" ]; then
    echo "Create initialize data"
    python ./prestart/init_data.py
fi
