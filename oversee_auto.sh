#!/bin/bash 

pidfile=/tmp/mydaemon.pid 

while true 
do 
	procid="`cat /tmp/mydaemon.pid`" 
#	echo $procid
	process="`ps $procid |awk '{print $6}'|awk '{if(NR>1)print}'`"
#	echo $process

	if [ "$process" == "" ]; 
	then 
		procid2="`ps -ef|grep "python3 /home/osboxes/script/main.py"|grep -v grep|awk '{print $2}'`"
		if [ -z "$procid2" ]; 
		then
		       	rm "$pidfile" 	
			python3 /home/osboxes/script/main.py  
			echo "python3 main.py started"
		else 
			kill -9 $procid2
			python3 /home/osboxes/script/main.py
			echo "python3 main.py restarted"
		fi 
	else 
		echo "$process is running fine"
	fi

	sleep 0.5 
done 



