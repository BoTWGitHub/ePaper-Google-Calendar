import json
from datetime import timezone
from datetime import timedelta
from datetime import datetime
import logging

def main():
    logging.basicConfig(filename='logging.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
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
    logging.info("setting next wake up time " + data['auto_wake_time'])
    data['auto_wake_repeat'] = 127

    with open('/etc/pisugar-server/config.json', 'w') as file:
        file.write(json.dumps(data))
    
    logging.info("save config file done...")


if __name__=='__main__':
    main()
