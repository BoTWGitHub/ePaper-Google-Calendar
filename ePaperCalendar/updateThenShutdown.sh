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
# Pisugar server 的 URL
pisugar_server_url="http://localhost:8421"
# 最大重試次數
retry=18
# 間隔時間（秒）
interval=10
serverReady=0

while [ $retry -gt 0 ]; do
    # 嘗試訪問 Pisugar server
    response=$(curl -s -o /dev/null -w "%{http_code}" "${pisugar_server_url}")

    # 檢查響應代碼，200 表示 Pisugar server 已經初始化完成
    if [ "$response" -eq 200 ]; then
        echo "Pisugar server 已初始化完成"
        serverReady=1
        break
    else
        retry=$((retry - 1))
    fi

    # 等待一段時間後重試
    echo "等待 ${interval} 秒後再次嘗試..."
    sleep "$interval"
done

if [ $serverReady == 1 ]; then
    echo "$(date)" >> /home/k2345777/batteryLog.txt
    ret="get battery" | nc -q 0 127.0.0.1 8423
    echo "get battery" | nc -q 0 127.0.0.1 8423 >> /home/k2345777/batteryLog.txt
    echo "rtc_web" | nc -q 0 127.0.0.1 8423
fi

sudo shutdown 1