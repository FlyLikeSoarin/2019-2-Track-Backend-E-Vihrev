#! /bin/bash

if [ ! -f ./.db-pid ]; then 
	nohup postgres -D database > /dev/null 2>&1 &
	echo $! > .db-pid
	echo 'Started!'
else
	echo 'Already working or was not stopped correctly'
fi
