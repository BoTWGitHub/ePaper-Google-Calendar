import json
from datetime import timezone
from datetime import timedelta
from datetime import datetime

def main():
    with open('/etc/pisugar-server/config.json', 'r') as file:
        content = file.read()
        data = json.loads(content)
    
    now = datetime.now(timezone.utc).astimezone()
    nextDay = now+timedelta(days=1)

    if now.hour<18:
        if(now.hour<6):
            newWakeTime = datetime(now.year, now.month, now.day, 6, 0, 0, 0, nextDay.tzinfo)
        else:
            newWakeTime = datetime(now.year, now.month, now.day, 18, 0, 0, 0, nextDay.tzinfo)
    else:
        newWakeTime = datetime(nextDay.year, nextDay.month, nextDay.day, 6, 0, 0, 0, now.tzinfo)

    data['auto_wake_time'] = newWakeTime.isoformat()

    with open('/etc/pisugar-server/config.json', 'w') as file:
        file.write(json.dumps(data))


if __name__=='__main__':
    main()
