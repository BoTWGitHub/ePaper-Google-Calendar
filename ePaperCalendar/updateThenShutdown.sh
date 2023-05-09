max_wait = 180
count = 0

while ! ping -c 1 -W 1 www.google.com; do
    count = $((count+1))
    if [ $count -ge $max_wait ]; then
        break
    fi
    sleep 1
done

python /home/k2345777/ePaper-Google-Calendar/ePaperCalendar/updateCalendar.py

sudo shutdown now