#!/bin/bash

#python -m pip install arrow
#python -m pip install ics
#python -m pip install pisugar

echo "Check network..."
while ! ping -c 1 -W 1 www.google.com; do
    sleep 1
done
echo "Network ok!"

sleep 1

echo "sync the time..."
echo "rtc_web" | nc -q 0 127.0.0.1 8423

echo "update wakeup time..."
python /home/k2345777/ePaper-Google-Calendar/ePaperCalendar/setNextWakeTime.py
systemctl restart pisugar-server

echo "update calendar..."
python /home/k2345777/ePaper-Google-Calendar/ePaperCalendar/updateCalendar.py

sleep 10

sudo shutdown now
