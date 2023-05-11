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
# Pisugar server �� URL
pisugar_server_url="http://localhost:8421"
# �̤j���զ���
retry=18
# ���j�ɶ��]��^
interval=10
serverReady=0

while [ $retry -gt 0 ]; do
    # ���ճX�� Pisugar server
    response=$(curl -s -o /dev/null -w "%{http_code}" "${pisugar_server_url}")

    # �ˬd�T���N�X�A200 ��� Pisugar server �w�g��l�Ƨ���
    if [ "$response" -eq 200 ]; then
        echo "Pisugar server �w��l�Ƨ���"
        serverReady=1
        break
    else
        retry=$((retry - 1))
    fi

    # ���ݤ@�q�ɶ��᭫��
    echo "���� ${interval} ���A������..."
    sleep "$interval"
done

if [ $serverReady == 1 ]; then
    echo "$(date)" >> /home/k2345777/batteryLog.txt
    ret="get battery" | nc -q 0 127.0.0.1 8423
    echo "get battery" | nc -q 0 127.0.0.1 8423 >> /home/k2345777/batteryLog.txt
    echo "rtc_web" | nc -q 0 127.0.0.1 8423
fi

sudo shutdown 1