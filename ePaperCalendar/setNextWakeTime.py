import json
from datetime import timezone
from datetime import timedelta
from datetime import datetime
from dateutil import parser

def main():
    with open('/etc/pisugar-server/config.json', 'r') as file:
        content = file.read()
        data = json.loads(content)
    
    oldWakeTime = parser.parse(data['auto_wake_time'])
    now = datetime.now()
    nextDay = now+timedelta(days=1)
    

    if oldWakeTime.hour==12:
        newWakeTime = datetime(nextDay.year, nextDay.month, nextDay.day, 0, 0, 0, 0, nextDay.tzinfo))
    else:
        newWakeTime = datetime(now.year, now.month, now.day, 12, 0, 0, 0, now.tzinfo)

    data['auto_wake_time'] = newWakeTime.isoformat()

    with open('/etc/pisugar-server/config.json', 'w') as file:
        file.write(json.dumps(data))


if __name__=='__main__':
    main()
