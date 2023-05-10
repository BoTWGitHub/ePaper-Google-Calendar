import json
from datetime import timedelta
from datetime import datetime
from dateutil import parser

def main():
    with open('/etc/pisugar-server/config.json', 'r') as file:
        content = file.read()
        data = json.loads(content)
    
    oldWakeTime = parser.parse(data['auto_wake_time'])
    now = datetime.now()
    print(newWakeTime)
    #if oldWakeTime.hour==11:
    now = now+timedelta(days=1)
    newWakeTime = datetime(now.year, now.month, now.day, 0, 0, 0, 0, now.timetz)
    print(newWakeTime)


if __name__=='__main__':
    main()
