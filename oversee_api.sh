#!/bin/bash 

while true
do
        procid3="`ps -ef|grep "python3 /home/osboxes/script/api5.py"|grep -v grep|awk '{print $2}'`"
        echo $procid3
        if [ -z "$procid3" ];
        then
                python3 /home/osboxes/script/api5.py
                echo "python3 api5 started"
        fi
        sleep 0.5
done

