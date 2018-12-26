#!/bin/bash
source plugin_vars.sh
./auto_update.py
status=`echo $?`
if [[ "$status" != 0 ]]
then
	echo "exiting"
	exit 1
fi
cat globalmanifest.json | python -m json.tool
