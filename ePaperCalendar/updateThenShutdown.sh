#!/bin/bash

#try 3min
retry=180
connect=0
while [ $retry -gt 0 ]; do
    if ping -c 1 -W 1 www.google.com; then
        connect=1
        break
    else
        sleep 1
        retry=$(($retry-1))
    fi
done

if [ $connect == 1]; then
    echo "$(date)" >> /home/k2345777/batteryLog.txt
    echo "get battery" | nc -q 0 127.0.0.1 8423 >> /home/k2345777/batteryLog.txt
    echo "rtc_web" | nc -q 0 127.0.0.1 8423
fi

#python /home/k2345777/ePaper-Google-Calendar/ePaperCalendar/setNextWakeTime.py
#systemctl restart pisugar-server

#python -m pip install arrow
#python -m pip install ics

python /home/k2345777/ePaper-Google-Calendar/ePaperCalendar/updateCalendar.py

sudo shutdown -h 3