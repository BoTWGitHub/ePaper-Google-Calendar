#!/bin/bash

sudo python /home/k2345777/ePaper-Google-Calendar/ePaperCalendar/setNextWakeTime.py

sudo systemctl restart pisugar-server

while ! ping -c 1 -W 1 www.google.com; do
    sleep 1
done

python -m pip install arrow
python -m pip install ics

python /home/k2345777/ePaper-Google-Calendar/ePaperCalendar/updateCalendar.py

#sudo shutdown -h 5