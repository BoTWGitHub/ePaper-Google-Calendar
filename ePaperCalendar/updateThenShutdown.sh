#!/bin/bash

while ! ping -c 1 -W 1 www.google.com; do
    sleep 1
done

echo "$(date)" >> /home/k2345777/batteryLog.txt
echo "get battery" | nc -q 0 127.0.0.1 8423 >> /home/k2345777/batteryLog.txt

python /home/k2345777/ePaper-Google-Calendar/ePaperCalendar/setNextWakeTime.py
systemctl restart pisugar-server

#python -m pip install arrow
#python -m pip install ics

python /home/k2345777/ePaper-Google-Calendar/ePaperCalendar/updateCalendar.py

#sudo shutdown -h 5