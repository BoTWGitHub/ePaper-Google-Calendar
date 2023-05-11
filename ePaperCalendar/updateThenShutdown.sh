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

#python -m pip install arrow
#python -m pip install ics
echo "update calendar..."
python /home/k2345777/ePaper-Google-Calendar/ePaperCalendar/updateCalendar.py

echo "update wakeup time"
python /home/k2345777/ePaper-Google-Calendar/ePaperCalendar/setNextWakeTime.py
systemctl restart pisugar-server



sudo shutdown 1