#! /bin/bash

if [ -f ./.db-pid ]; then
	db_pid=$(cat ./.db-pid)
	echo "Database pid: ${db_pid} "
	kill $db_pid
	echo 'Stopped!'
else
	echo 'No working db found'
fi

rm ./.db-pid
