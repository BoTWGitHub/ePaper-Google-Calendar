#!/bin/bash

python -m pip install arrow
python -m pip install ics
python -m pip install pisugar

echo "sync the time..."
echo "rtc_web" | nc -q 0 127.0.0.1 8423

echo "update wakeup time..."
python /home/k2345777/ePaper-Google-Calendar/ePaperCalendar/setNextWakeTime.py
systemctl restart pisugar-server

echo "update calendar..."
python /home/k2345777/ePaper-Google-Calendar/ePaperCalendar/updateCalendar.py

echo "get battery level..."
python /home/k2345777/ePaper-Google-Calendar/ePaperCalendar/getPiSugarBatteryLevel.py

sudo shutdown 1
