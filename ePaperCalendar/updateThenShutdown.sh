#!/bin/bash

while ! ping -c 1 -W 1 www.google.com; do
    sleep 1
done

python /home/k2345777/ePaper-Google-Calendar/ePaperCalendar/updateCalendar.py

#sudo shutdown -h 5