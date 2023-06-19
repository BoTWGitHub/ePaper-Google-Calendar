import os
import arrow
import logging
import platform
import requests
from ics import Calendar

def collectEvents() -> list:
    logging.info("collecting events...")
    if platform.system() == "Windows":
        urlsFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config\\calUrls.cfg')
    else:
        urlsFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config/calUrls.cfg')

    if os.path.exists(urlsFile):
        with open(urlsFile, 'r') as urlsData:
            urls = urlsData.read().splitlines()
    else:
        logging.error(urlsFile + ' doesn\'t exist...')
        return []
    
    res = []
    currentTime = arrow.now()
    for url in urls:
        try:
            icsData = requests.get(url).text
            if icsData.find('PRODID')==-1:
                icsData = fixProdId(icsData)

            cal = Calendar(icsData)
            events = cal.events
            for event in events:
                eventTime = arrow.get(event.begin.astimezone(currentTime.tzinfo))
                if eventTime>=currentTime:
                    res.append([eventTime, event.name])
        except:
            logging.error('iCal parsing error...')
    
    return sorted(res)

def fixProdId(data: str) -> str:
    lines = data.splitlines()
    lines.insert(1, 'PRODID:-//Unknown//NONSGML v1.0//EN')
    return '\n'.join(lines)
